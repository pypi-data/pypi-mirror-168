import logging
from functools import cached_property

from marshmallow import Schema, fields, validate

logger = logging.getLogger(__name__)

from ..errors import BotError, YamlSnippet
from ..scenarios import ExpressionField, ScenarioField
from ..schemas import BaseSchema, ConfigSchema
from ._base import FlowComponent, FlowResult
from .slot_filling import HandlerSchema, SlotFilling, SlotSchema


class JumpTo(Schema):
    node = fields.Str(required=True)
    transition = fields.Str(required=True, validate=validate.OneOf(["condition", "response"]))


class NodeCommands(BaseSchema):
    end = fields.Nested(Schema)
    listen = fields.Nested(Schema)
    followup = fields.Nested(Schema)
    jump_to = fields.Nested(JumpTo)


class NodeSettings(ConfigSchema):
    after_digression_followup = fields.Str(
        validate=validate.OneOf(["never_return", "allow_return"]), load_default="allow_return"
    )


class NodeSchema(ConfigSchema):
    label = fields.Str()
    condition = ExpressionField(required=True)
    slot_filling = fields.List(fields.Nested(SlotSchema))
    slot_handlers = fields.List(fields.Nested(HandlerSchema))
    response = ScenarioField(NodeCommands, many=True, required=True)
    followup = fields.List(fields.Nested(lambda: NodeSchema()))
    settings = fields.Nested(NodeSettings, load_default=NodeSettings().load({}))


class NodeStack:
    def __init__(self, stack, tree):
        self.stack = stack
        self.tree = tree

    def push(self, node, transition):
        self.remove(node)
        self.stack.append([node.label, transition])

    def pop(self):
        if self.stack:
            label, transition = self.stack.pop()
            return self.tree.catalog[label], transition
        return None, None

    def peek(self):
        if self.stack:
            label, transition = self.stack[-1]
            return self.tree.catalog[label], transition
        return None, None

    def remove(self, node):
        label = node.label
        found = False
        for label, transition in self.stack[:]:
            if label == node.label:
                self.stack.remove([label, transition])
                found = True
        return found

    def clear(self):
        self.stack.clear()


class DialogTree:
    def __init__(self, definition):
        self.tree = Tree(definition)

    def __call__(self, ctx, state):
        stack = NodeStack(state.setdefault("node_stack", []), self.tree)
        turn = Turn(self.tree, stack, ctx)
        return turn()


class Turn:
    def __init__(self, tree, stack, ctx):
        self.tree = tree
        self.stack = stack
        self.ctx = ctx

    def __call__(self):
        node, transition = self.stack.peek()
        if node:
            logger.debug(f"peek {node} transition={transition}")
            if transition == "followup":
                return self.focus_followup(node)
            elif transition == "slot_filling":
                return self.trigger(node)
            else:
                raise ValueError(f"Unknown focus transition {transition!r}")
        else:
            return self.root_nodes()

    def root_nodes(self):
        for node in self.tree.root_nodes:
            if node.condition(self.ctx):
                return self.trigger(node)
        else:
            return FlowResult.DONE

    def focus_followup(self, parent_node):
        for node in parent_node.followup:
            if node.condition(self.ctx):
                self.stack.remove(parent_node)
                return self.trigger(node)
        else:
            return self.digression(parent_node)

    def command_followup(self, parent_node):
        logger.debug(f"followup {parent_node}")
        for node in parent_node.followup:
            if node.condition(self.ctx):
                return self.trigger_maybe_digressed(node)
        else:
            logger.warning(f"No followup node matched {parent_node}")
            return FlowResult.LISTEN

    def command_listen(self, node):
        if node.followup:
            self.stack.push(node, "followup")
            return FlowResult.LISTEN
        else:
            return self.return_after_digression() or FlowResult.LISTEN

    def command_end(self):
        self.stack.clear()
        self.ctx.clear_state_variables()
        return FlowResult.DONE

    def command_jump_to(self, from_node, payload):
        logger.debug(f"jump_to {payload}")
        jump_to_node = self.tree.catalog.get(payload["node"])
        if jump_to_node is None:
            raise BotError(f"Unknown jump_to node {payload['node']!r}")
        if payload["transition"] == "response":
            return self.trigger_maybe_digressed(jump_to_node)
        elif payload["transition"] == "condition":
            return self.jump_to_condition(jump_to_node)
        else:
            raise BotError(f"Unknown jump_to transition {payload['transition']!r}")

    def jump_to_condition(self, jump_to_node):
        for node in jump_to_node.me_and_right_siblings:
            if node.condition(self.ctx):
                return self.trigger_maybe_digressed(node)
        else:
            logger.warning(f"No node matched {jump_to_node}")
            return self.return_after_digression() or self.command_end()

    def digression(self, digressed_node):
        logger.debug(f"digression from {digressed_node}")
        for node in self.tree.root_nodes:
            if node == digressed_node:
                continue
            if node.condition(self.ctx, digressing=True):
                return self.trigger_maybe_digressed(node)
        else:
            if digressed_node.followup_allow_return:
                return self.return_after_digression() or self.command_end()
            else:
                return self.command_end()

    def return_after_digression(self):
        node, transition = self.stack.pop()
        if node:
            logger.debug(f"return_after_digression {node} {transition}")
            if transition == "slot_filling":
                return self.trigger(node, returning=True)
            elif transition == "followup":
                if node.followup_allow_return:
                    return self.trigger(node, returning=True)
                else:
                    return self.return_after_digression()
            else:
                raise ValueError(f"Unknown focus transition {transition!r}")
        else:
            # nowere to return
            return None

    def trigger_maybe_digressed(self, node):
        if self.stack.remove(node):
            return self.trigger(node, returning=True)
        else:
            return self.trigger(node)

    def trigger(self, node, returning=False):
        logger.debug(f"trigger {node}, returning={returning}")
        if node.slot_filling:
            result = node.slot_filling(self.ctx, returning)
            if result == FlowResult.DONE:
                self.stack.remove(node)
                return self.response(node, returning)
            elif result == FlowResult.LISTEN:
                self.stack.push(node, "slot_filling")
                return FlowResult.LISTEN
            elif result == FlowResult.DIGRESS:
                return self.digression(node)
            else:
                raise ValueError(f"Unknown flow result {result!r}")
        else:
            return self.response(node, returning)

    def response(self, node, returning):
        for command in node.response(self.ctx, returning=returning):
            if "jump_to" in command:
                return self.command_jump_to(node, command["jump_to"])
            if "listen" in command:
                return self.command_listen(node)
            if "end" in command:
                return self.command_end()
            if "followup" in command:
                return self.command_followup(node)
            self.ctx.commands.append(command)
        else:
            if node.followup:
                return self.command_listen(node)
            return self.return_after_digression() or self.command_end()


class Tree:
    def __init__(self, definition):
        self.catalog = {}
        self.root_nodes = [self.create_node(d) for d in definition]

    def create_node(self, definition, parent=None):
        if "label" not in definition and (
            "followup" in definition or "slot_filling" in definition
        ):
            raise BotError("Stateful node must have a label", YamlSnippet.format(definition))
        node = Node(definition, self, parent)
        if "label" in definition:
            if definition["label"] in self.catalog:
                raise BotError(
                    f"Duplicate node label {definition['label']!r}",
                    YamlSnippet.format(definition["label"]),
                )
            self.catalog[definition["label"]] = node
        return node


class Node:
    def __init__(self, definition, tree, parent):
        self.label = definition.get("label")
        self.definition = definition
        self.parent = parent
        self.tree = tree
        self.condition = definition["condition"]
        self.response = definition["response"]
        self.followup = [tree.create_node(d, self) for d in definition.get("followup", [])]
        self.slot_filling = None
        if "slot_filling" in definition:
            self.slot_filling = FlowComponent(
                definition["label"],
                SlotFilling(
                    definition["slot_filling"],
                    definition.get("slot_handlers", []),
                ),
            )

    @cached_property
    def me_and_right_siblings(self):
        siblings = self.parent.followup if self.parent else self.tree.root_nodes
        index = siblings.index(self)
        return siblings[index:]

    @cached_property
    def followup_allow_return(self):
        policy = self.definition["settings"]["after_digression_followup"]
        if policy == "allow_return":
            return True
        elif policy == "never_return":
            return False
        else:
            raise ValueError(f"Unknown returning policy {policy!r}")

    @cached_property
    def title(self):
        if self.label:
            return f"{self.label!r}"
        elif self.parent:
            return f'{self.parent.title} -> "{self.definition["condition"]!r}"'
        else:
            return f'"{self.definition["condition"]!r}"'

    def __str__(self):
        return self.title
