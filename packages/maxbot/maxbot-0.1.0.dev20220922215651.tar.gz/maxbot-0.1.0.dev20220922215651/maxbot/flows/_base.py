from dataclasses import dataclass
from enum import Enum
from typing import Callable


class FlowResult(Enum):

    DIGRESS = "digress"
    LISTEN = "listen"
    DONE = "done"


@dataclass(frozen=True)
class FlowComponent:

    name: str
    flow: Callable

    def __call__(self, ctx, digression_result=None):
        state = ctx.get_state_variable(self.name) or {}
        if digression_result is None:
            result = self.flow(ctx, state)
        else:
            result = self.flow(ctx, state, digression_result)
        if result == FlowResult.DONE:
            # FXIME need to reset all the child states too
            ctx.set_state_variable(self.name, None)
        else:
            ctx.set_state_variable(self.name, state)
        return result
