"""Order workflow definition 25."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Step:
    name: str
    optional: bool = False
    timeout_sec: int = 30


@dataclass
class Workflow25:
    code: str = "flow_25"
    steps: list[Step] = field(default_factory=lambda: [
        Step("validate", timeout_sec=10),
        Step("reserve_inventory", timeout_sec=10),
        Step("authorize_payment", timeout_sec=19),
        Step("capture_payment", optional=False),
        Step("create_shipment", timeout_sec=45),
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
            "index": 25,
        }


DEFAULT_FLOW_25 = Workflow25()
