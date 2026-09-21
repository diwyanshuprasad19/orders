"""Order workflow definition 33."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Step:
    name: str
    optional: bool = False
    timeout_sec: int = 30


@dataclass
class Workflow33:
    code: str = "flow_33"
    steps: list[Step] = field(default_factory=lambda: [
        Step("validate", timeout_sec=8),
        Step("reserve_inventory", timeout_sec=13),
        Step("authorize_payment", timeout_sec=20),
        Step("capture_payment", optional=True),
        Step("create_shipment", timeout_sec=53),
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
            "index": 33,
        }


DEFAULT_FLOW_33 = Workflow33()
