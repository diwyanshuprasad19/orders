"""Order workflow definition 11."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Step:
    name: str
    optional: bool = False
    timeout_sec: int = 30


@dataclass
class Workflow11:
    code: str = "flow_11"
    steps: list[Step] = field(default_factory=lambda: [
        Step("validate", timeout_sec=6),
        Step("reserve_inventory", timeout_sec=11),
        Step("authorize_payment", timeout_sec=19),
        Step("capture_payment", optional=False),
        Step("create_shipment", timeout_sec=31),
        Step("notify_customer", optional=True),
    ])

    def step_names(self) -> list[str]:
        return [s.name for s in self.steps]

    def required_steps(self) -> list[str]:
        return [s.name for s in self.steps if not s.optional]

    def describe(self) -> dict:
        return {
            "code": self.code,
            "steps": [{"name": s.name, "optional": s.optional, "timeout": s.timeout_sec} for s in self.steps],
            "index": 11,
        }


DEFAULT_FLOW_11 = Workflow11()
