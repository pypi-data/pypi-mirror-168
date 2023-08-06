from typing import Any, List, Optional

from kisters.network_store.model_library.base import (
    BaseNode as _BaseNode,
    Model as _Model,
)
from pydantic import Field, validator


class _Node(_BaseNode):
    domain: str = Field("water", const=True)
    name: Optional[str] = Field(
        None,
        description="Optional node name",
    )


class Junction(_Node):
    element_class: str = Field("Junction", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class LevelBoundary(_Node):
    element_class: str = Field("LevelBoundary", const=True)
    initial_flow: Optional[float] = Field(
        None, description="Initial volumetric flow rate for simulation in m^3/s"
    )


class FlowBoundary(_Node):
    element_class: str = Field("FlowBoundary", const=True)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )


class _StorageLevelVolume(_Model):
    level: float = Field(..., description="Reservoir level in m")
    volume: float = Field(..., ge=0.0, description="Reservoir volume in m^3")


class Storage(_Node):
    element_class: str = Field("Storage", const=True)
    flow_boundary: Optional[bool] = Field(
        False,
        description="Optional inflow or lateral flow",
    )
    level_volume: List[_StorageLevelVolume] = Field(..., min_items=2)
    initial_level: Optional[float] = Field(
        None, description="Initial level for simulation"
    )

    @validator("level_volume")
    def check_monotonic(cls, v: Any) -> Any:
        for a, b in zip(v, v[1:]):
            if a.level >= b.level:
                raise ValueError(
                    "Level must be strictly increasing ({a.level} >= {b.level})"
                )
            if a.volume >= b.volume:
                raise ValueError(
                    "Volume must be strictly increasing ({a.volume} >= {b.volume})"
                )
        return v
