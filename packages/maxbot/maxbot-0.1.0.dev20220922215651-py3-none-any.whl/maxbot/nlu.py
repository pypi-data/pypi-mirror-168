import logging
import re
import warnings
from itertools import chain
from operator import attrgetter

import spacy
import textdistance
from dateparser import parse
from dateparser.date import DateDataParser
from dateparser.search import search_dates
from marshmallow import fields
from number_parser import parse_number
from spacy.matcher import Matcher, PhraseMatcher

logger = logging.getLogger(__name__)

from .context import EntitiesResult, IntentsResult, RecognizedEntity, RecognizedIntent
from .schemas import ConfigSchema


class IntentSchema(ConfigSchema):
    name = fields.Str(required=True)
    examples = fields.List(fields.Str(), load_default=list)


class EntityValue(ConfigSchema):
    name = fields.Str(required=True)
    phrases = fields.List(fields.Str(), load_default=list)
    regexps = fields.List(fields.Str(), load_default=list)


class EntitySchema(ConfigSchema):
    name = fields.Str(required=True)
    values = fields.List(fields.Nested(EntityValue()), load_default=list)


class SimilarityRecognizer:

    similarity = textdistance.cosine.similarity
    default_threshold = 0.7  # seems to work good enough

    def __init__(self, spacy_nlp, threshold=None):
        self.spacy_nlp = spacy_nlp
        self.examples, self.labels = [], []
        self.threshold = threshold or self.default_threshold

    def load(self, intents):
        for intent in intents:
            self.examples.extend([self.spacy_nlp.make_doc(e) for e in intent["examples"]])
            self.labels.extend([intent["name"]] * len(intent["examples"]))

    def _preprocess(self, doc):
        return [t.lower_ for t in doc]

    def __call__(self, doc):
        tokens = self._preprocess(doc)
        scores = [self.similarity(tokens, self._preprocess(example)) for example in self.examples]

        max_scores = {}
        for score, label, example in zip(scores, self.labels, self.examples):
            if score > max_scores.get(label, self.threshold):
                max_scores[label] = score
                logger.debug(f"label {label!r} score {score} example {example.text!r}")

        result = []
        for label, score in max_scores.items():
            confidence = score / len(max_scores)
            result.append(RecognizedIntent(label, confidence))
        return result


class PhraseEntities:
    def __init__(self, spacy_nlp):
        self.spacy_nlp = spacy_nlp
        self.matcher = PhraseMatcher(spacy_nlp.vocab, attr="LOWER")
        self.ids = {}

    def load(self, entities):
        for entity in entities:
            for value in entity["values"]:
                key = f"{entity['name']}-{value['name']}"
                match_id = self.spacy_nlp.vocab.strings.add(key)
                self.ids[match_id] = (entity["name"], value["name"])
                patterns = list(self.spacy_nlp.pipe(value["phrases"]))
                self.matcher.add(key, patterns)

    def __call__(self, doc):
        for match_id, start, end in self.matcher(doc):
            name, value = self.ids[match_id]
            span = doc[start:end]
            # TODO deal with entities overlap
            yield RecognizedEntity.from_span(span, name, value)


class RegexpEntities:
    def __init__(self):
        self.regexps = []

    def load(self, entities):
        for entity in entities:
            for value in entity["values"]:
                for regexp in value["regexps"]:
                    self.regexps.append(
                        {
                            "label": entity["name"],
                            "id": value["name"],
                            "pattern": re.compile(regexp),
                        }
                    )

    def __call__(self, doc):
        for p in self.regexps:
            for match in re.finditer(p["pattern"], doc.text):
                start, end = match.span()
                if start == end:
                    continue
                yield RecognizedEntity(
                    name=p["label"],
                    value=p["id"],
                    literal=doc.text[start:end],
                    start_char=start,
                    end_char=end,
                )


class SpacyMatcherEntities:
    def __init__(self, spacy_nlp):
        self.matcher = Matcher(spacy_nlp.vocab)
        self.matcher.add("number", [[{"LIKE_NUM": True, "OP": "+"}]], greedy="LONGEST")
        self.matcher.add("email", [[{"LIKE_EMAIL": True}]])
        self.matcher.add("url", [[{"LIKE_URL": True}]])

    def __call__(self, doc):
        matches = self.matcher(doc, as_spans=True)
        # does spacy reverse the order while matching greedly?
        matches = sorted(matches, key=attrgetter("start"))
        for span in matches:
            if span.label_ == "number":
                number = parse_number(span.text)
                yield RecognizedEntity.from_span(span, "number", number)
            else:
                yield RecognizedEntity.from_span(span)


class DateParserEntities:
    """
    Date/Time parsing just for pet projects.
    Use duckling for full featured date/time recognition support.
    """

    # language autodetection slows down the parser
    # provide language explicitly

    ddp = DateDataParser(languages=["en"], settings={"RETURN_TIME_AS_PERIOD": True})

    def __call__(self, doc):
        # suppress known PytzUsageWarning from dateparser
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            shift = 0
            results = search_dates(doc.text, languages=["en"])
            if results is None:
                return
            for literal, dt in results:
                start_char = doc.text.index(literal, shift)
                end_char = start_char + len(literal)
                shift = end_char
                # a bit tricky way to split date and time parts
                dd = self.ddp.get_date_data(literal)
                if dd.period == "time":
                    if parse(literal, languages=["en"], settings={"REQUIRE_PARTS": ["day"]}):
                        yield RecognizedEntity(
                            "date", dt.date().isoformat(), literal, start_char, end_char
                        )
                    yield RecognizedEntity(
                        "time", dt.time().isoformat(), literal, start_char, end_char
                    )
                else:
                    yield RecognizedEntity(
                        "date", dt.date().isoformat(), literal, start_char, end_char
                    )


class RuleBasedEntities:
    def __init__(self, spacy_nlp):
        """
        FIXME: need some generic way to resolve overlaps
        Need to manually compose because date/time entities could not overlap with number entities
        """
        self.dateparser_entities = DateParserEntities()
        self.spacy_matcher_entities = SpacyMatcherEntities(spacy_nlp)

    def __call__(self, doc):
        seen_chars = set()
        for entity in self.dateparser_entities(doc):
            seen_chars.update(range(entity.start_char, entity.end_char))
            yield entity
        for entity in self.spacy_matcher_entities(doc):
            if entity.name == "number" and (
                entity.start_char in seen_chars or entity.end_char - 1 in seen_chars
            ):
                continue
            yield entity


class Nlu:

    default_threshold = 0.5  # standard probability threshold

    def __init__(self, spacy_nlp=None, threshold=None):
        self.spacy_nlp = spacy_nlp or spacy.blank("en")
        self._intent_recognizer = None
        self._entity_recognizers = None
        self.threshold = threshold or self.default_threshold

    @property
    def intent_recognizer(self):
        if self._intent_recognizer is None:
            self._intent_recognizer = SimilarityRecognizer(self.spacy_nlp)
        return self._intent_recognizer

    @intent_recognizer.setter
    def intent_recognizer(self, value):
        self._intent_recognizer = value

    @property
    def entity_recognizers(self):
        if self._entity_recognizers is None:
            self._entity_recognizers = [
                PhraseEntities(self.spacy_nlp),
                RegexpEntities(),
                RuleBasedEntities(self.spacy_nlp),
            ]
        return self._entity_recognizers

    @entity_recognizers.setter
    def entity_recognizers(self, value):
        self._entity_recognizers = value

    def load(self, intents, entities):
        self.intent_recognizer.load(intents)
        for entity_recognizer in self.entity_recognizers:
            if hasattr(entity_recognizer, "load"):
                entity_recognizer.load(entities)

    def __call__(self, message):
        intents, entities = IntentsResult(), EntitiesResult()
        if "text" in message:
            doc = self.spacy_nlp(message["text"])
            intents = IntentsResult.resolve(self.intent_recognizer(doc))
            entities = EntitiesResult.resolve(
                list(
                    chain.from_iterable(
                        recognizer(doc=doc) for recognizer in self.entity_recognizers
                    )
                )
            )
        return intents, entities
