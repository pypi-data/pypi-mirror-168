import logging
from dataclasses import dataclass, field, fields
from operator import attrgetter
from typing import Optional, Tuple, Union

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RecognizedIntent:
    name: str
    confidence: float


@dataclass(frozen=True)
class IntentsResult:
    @classmethod
    def resolve(cls, intents, top_threshold=0.5):
        ranking = tuple(sorted(intents, key=attrgetter("confidence"), reverse=True))
        for intent in ranking:
            logger.debug(f"{intent}")
        top = ranking[0] if ranking else None
        if top and top.confidence < top_threshold:
            top = None
        return cls(top, ranking)

    top: Optional[RecognizedIntent] = field(default=None)
    ranking: Tuple[RecognizedIntent] = field(default_factory=tuple)

    def __getattr__(self, name):
        if self.top and self.top.name == name:
            return self.top
        return None


@dataclass(frozen=True)
class RecognizedEntity:

    name: str
    value: Union[str, int]
    literal: str
    start_char: int
    end_char: int

    @classmethod
    def from_span(cls, span, name=None, value=None):
        if value is None:
            value = span.text
        return cls(name or span.label_, value, span.text, span.start_char, span.end_char)


@dataclass(frozen=True)
class EntitiesProxy:

    first: RecognizedEntity
    all_objects: Tuple[RecognizedEntity]

    @property
    def all_values(self):
        return tuple(e.value for e in self.all_objects)

    def __getattr__(self, name):
        """
        Convenient access in expressions
            entities.menu.value == entities.menu.first.value
            entities.menu.literal == entities.menu.first.literal
        and
            entities.menu.vegetarian == ('vegetarian' in entities.menu.all_values)
        """
        if hasattr(self.first, name):
            return getattr(self.first, name)
        return name in self.all_values


@dataclass(frozen=True)
class EntitiesResult:
    @classmethod
    def resolve(cls, entities):
        mapping = {}
        for entity in entities:
            logger.debug(f"{entity}")
            mapping.setdefault(entity.name, list()).append(entity)
        proxies = {}
        for name, objects in mapping.items():
            proxies[name] = EntitiesProxy(objects[0], tuple(objects))
        return cls(proxies, tuple(entities))

    proxies: dict[str, EntitiesProxy] = field(default_factory=dict)
    all_objects: Tuple[RecognizedEntity] = field(default_factory=tuple)

    def __getattr__(self, name):
        """
        Convenient access in expressions
            entities.menu == entities.proxies.get('menu')
        """
        return self.proxies.get(name)


@dataclass(frozen=True)
class StateVariables:

    user: dict = field(default_factory=dict)
    slots: dict = field(default_factory=dict)
    components: dict = field(default_factory=dict)

    @classmethod
    def from_kv_pairs(cls, kv_pairs):
        data = {f.name: {} for f in fields(cls)}
        for name, value in kv_pairs:
            ns, name = name.split(".", 1)
            if ns not in data:
                raise ValueError(f"Unknown ns {ns}")
            data[ns][name] = value
        return cls(**data)

    def to_kv_pairs(self):
        for f in fields(self):
            for name, value in getattr(self, f.name).items():
                name = f"{f.name}.{name}"
                yield name, value


@dataclass
class TurnContext:

    message: dict
    dialog: dict

    intents: IntentsResult = field(default_factory=IntentsResult)
    entities: EntitiesResult = field(default_factory=EntitiesResult)
    state: StateVariables = field(default_factory=StateVariables)

    scenario_context: dict = field(default_factory=dict, init=False)
    commands: list[dict] = field(default_factory=list, init=False)

    def get_state_variable(self, key):
        return self.state.components.get(key)

    def set_state_variable(self, key, value):
        self.state.components[key] = value

    def clear_state_variables(self):
        self.state.components.clear()

    def extend_scenario_context(self, **params):
        self.scenario_context.update(params)

    def create_scenario_context(self, params):
        rv = {}
        rv.update(self.scenario_context)
        rv.update(params)
        rv.update(
            {
                "message": self.message,
                "dialog": self.dialog,
                "intents": self.intents,
                "entities": self.entities,
                "user": self.state.user,
                "slots": self.state.slots,
            }
        )
        return rv
