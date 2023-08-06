import logging
from dataclasses import dataclass, field
from typing import List, Optional

from marshmallow import Schema, fields, post_load

logger = logging.getLogger(__name__)

from ..context import EntitiesProxy, RecognizedEntity
from ..scenarios import ExpressionField, ScenarioField
from ..schemas import BaseSchema, ConfigSchema
from ._base import FlowResult


class FoundCommands(BaseSchema):
    move_on = fields.Nested(Schema)
    prompt_again = fields.Nested(Schema)
    listen_again = fields.Nested(Schema)
    response = fields.Nested(Schema)


class NotFoundCommands(BaseSchema):
    prompt_again = fields.Nested(Schema)
    listen_again = fields.Nested(Schema)
    response = fields.Nested(Schema)


class PromptCommands(BaseSchema):
    listen_again = fields.Nested(Schema)
    response = fields.Nested(Schema)


class HandlerCommands(BaseSchema):
    move_on = fields.Nested(Schema)
    response = fields.Nested(Schema)


@dataclass(frozen=True)
class Slot:
    name: str
    check_for: callable
    condition: Optional[callable] = None
    value: Optional[callable] = None
    prompt: Optional[callable] = None
    found: Optional[callable] = None
    not_found: Optional[callable] = None


class SlotSchema(ConfigSchema):
    name = fields.Str(required=True)
    check_for = ExpressionField(required=True)
    value = ExpressionField()
    condition = ExpressionField()
    prompt = ScenarioField(PromptCommands, many=True)
    found = ScenarioField(FoundCommands, many=True)
    not_found = ScenarioField(NotFoundCommands, many=True)

    @post_load
    def create_object(self, data, **kwargs):
        return Slot(**data)


@dataclass(frozen=True)
class Handler:
    condition: callable
    response: callable


class HandlerSchema(ConfigSchema):
    condition = ExpressionField(required=True)
    response = ScenarioField(HandlerCommands, many=True, required=True)

    @post_load
    def create_object(self, data, **kwargs):
        return Handler(**data)


class SlotFilling:
    def __init__(self, slots, handlers):
        self.slots = slots
        self.handlers = handlers

    def __call__(self, ctx, state, returning=False):
        turn = Turn(self.slots, self.handlers, ctx, state, returning)
        return turn()


@dataclass
class Turn:
    slots: List[Slot]
    handlers: List[Handler]
    ctx: object
    state: dict
    returning: bool

    found_slots: list = field(default_factory=list)
    skip_prompt: list = field(default_factory=list)
    want_response: bool = False

    @property
    def enabled_slots(self):
        for slot in self.slots:
            if slot.condition is None or slot.condition(self.ctx):
                yield slot

    def elicit(self, slot):
        value = slot.check_for(
            self.ctx, slot_in_focus=(self.state.get("slot_in_focus") == slot.name)
        )
        if not value:
            return
        if slot.value:
            value = slot.value(self.ctx)
        if isinstance(value, (EntitiesProxy, RecognizedEntity)):
            value = value.value
        logger.debug(f"elicit slot {slot.name!r} value {value!r}")
        previous_value = self.ctx.state.slots.get(slot.name)
        self.ctx.state.slots[slot.name] = value
        self.found_slots.append((slot, {"previous_value": previous_value, "current_value": value}))

    def clear_slot(self, slot):
        self.ctx.state.slots.pop(slot.name, None)

    def listen_again(self, slot):
        self.skip_prompt.append(slot)

    def found(self, slot, params):
        for command in slot.found(self.ctx, **params):
            if "response" in command:
                self.want_response = True
                break
            if "prompt_again" in command:
                self.clear_slot(slot)
                break
            if "listen_again" in command:
                self.clear_slot(slot)
                self.listen_again(slot)
                break
            if "move_on" in command:
                break
            self.ctx.commands.append(command)

    def not_found(self, slot):
        for command in slot.not_found(self.ctx):
            if "response" in command:
                self.want_response = True
                break
            if "prompt_again" in command:
                break
            if "listen_again" in command:
                self.listen_again(slot)
                break
            self.ctx.commands.append(command)
        else:
            self.listen_again(slot)

    def prompt(self, slot):
        for command in slot.prompt(self.ctx):
            if "response" in command:
                self.want_response = True
                break
            if "listen_again" in command:
                self.listen_again(slot)
                break
            self.ctx.commands.append(command)
        else:
            self.listen_again(slot)

    def handler(self, handler):
        for command in handler.response(self.ctx):
            if "response" in command:
                self.want_response = True
                break
            if "move_on" in command:
                break
            self.ctx.commands.append(command)

    def __call__(self):
        # elicit
        for slot in self.enabled_slots:
            self.elicit(slot)
        # found
        for slot, params in self.found_slots:
            if slot.found:
                self.found(slot, params)
        if self.state.get("slot_in_focus") and not self.found_slots:
            # slot handlers
            for handler in self.handlers:
                if handler.condition(self.ctx):
                    self.handler(handler)
                    break
            else:
                if not self.returning:
                    return FlowResult.DIGRESS
                # not found
                catalog = {s.name: s for s in self.enabled_slots}
                slot = catalog[self.state.get("slot_in_focus")]
                if slot and slot.not_found:
                    self.not_found(slot)
        if not self.want_response:
            # prompt
            for slot in self.enabled_slots:
                if slot.prompt and self.ctx.state.slots.get(slot.name) is None:
                    self.state["slot_in_focus"] = slot.name
                    if slot not in self.skip_prompt:
                        self.prompt(slot)
                    break
            else:
                self.state["slot_in_focus"] = None
        # result
        if self.want_response:
            self.state["slot_in_focus"] = None
        if self.state.get("slot_in_focus") is None:
            return FlowResult.DONE
        else:
            return FlowResult.LISTEN
