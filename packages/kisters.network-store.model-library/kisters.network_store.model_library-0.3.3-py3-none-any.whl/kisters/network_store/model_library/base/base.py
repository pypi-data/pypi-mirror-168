import enum
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import (
    BaseModel,
    Extra,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    constr,
    validator,
)


class Model(BaseModel):
    class Config:
        extra = Extra.forbid


UserMetadataKey = constr(regex=r"^\w+$")
UserMetadataValue = Union[StrictBool, StrictInt, StrictFloat, StrictStr]


class TimeSeriesMapping(Model):
    """Attributes to identify a specific time series

    Leaving the the dispatch_info or ensemble_member properties unset means
    that the model adapter provides the missing information. Model Adapters may
    also ignore properties if they are irrelevant. For example, a model task
    may define a dispatch_info which would take precedence over the
    dispatch_info defined here when writing output.
    """

    store_id: Optional[str] = None
    path: str = Field(..., description="Path identifying the time series")
    t0: Optional[datetime] = None
    dispatch_info: Optional[str] = None
    ensemble_member: Optional[str] = None


class ElementMapping(Model):
    """Element attribute

    Very similar to the concept in the config store, but the UID is already defined"""

    attribute: str = Field(..., description="Attribute of an element in the adapter")
    attribute_index: Optional[int] = Field(
        None,
        description="Specific index of an attribute in the adapter, if it is an array",
    )


class DataMapping(Model):
    """Associate an element mapping with a time series mapping"""

    time_series: TimeSeriesMapping
    element: ElementMapping
    type: Optional[StrictStr] = Field(
        None, description="Arbitrary string field to identify the mapping"
    )


class BaseElement(Model):
    domain: Optional[str] = None
    element_class: Optional[str] = None
    uid: str = Field(..., regex="^[a-zA-Z]\\w*$", description="Unique identifier")
    display_name: Optional[str] = Field(
        None, description="String for labeling an element in a GUI"
    )
    created: Optional[datetime] = Field(
        None, description="Timestamp element was added to the network"
    )
    deleted: Optional[datetime] = Field(
        None, description="Timestamp element was removed from the network"
    )
    group_uid: Optional[str] = Field(
        None, description="UID of group to which link belongs"
    )
    user_metadata: Optional[Dict[UserMetadataKey, UserMetadataValue]] = Field(
        None, description="Optional dictionary of user-provided key-value pairs"
    )
    time_series_mappings: Optional[List[DataMapping]] = Field(
        None, description="List of timeseries mappings"
    )

    @validator("display_name", always=True)
    def default_display_name(cls, v: Any, values: Dict[str, Any]) -> Any:
        return v or values.get("uid")


class Location(Model):
    x: float
    y: float
    z: float = 0.0


class LocationSet(str, enum.Enum):
    GEOGRAPHIC = "location"
    SCHEMATIC = "schematic_location"


class LocationExtent(BaseModel):
    """Mapping of dimensions to range, e.g. {"x": [-10, 10]}"""

    x: Optional[Tuple[float, float]] = None
    y: Optional[Tuple[float, float]] = None
    z: Optional[Tuple[float, float]] = None


class BaseLink(BaseElement):
    collection: str = Field("links", const=True)
    source_uid: str = Field(..., description="UID of source node")
    target_uid: str = Field(..., description="UID of target node")
    vertices: Optional[List[Location]] = Field(
        None,
        description="Additional geographical points refining the path"
        " from source to target nodes",
    )
    schematic_vertices: Optional[List[Location]] = Field(
        None,
        description="Additional schematic points refining the path"
        " from source to target nodes",
    )


class BaseNode(BaseElement):
    collection: str = Field("nodes", const=True)
    location: Location = Field(..., description="Geographical location")
    schematic_location: Optional[Location] = Field(
        None, description="Schematic location. Takes value of 'location' if unset."
    )

    @validator("schematic_location", always=True)
    def default_schematic_location(cls, v: Any, values: Dict[str, Any]) -> Any:
        if v is None:
            return values.get("location")
        return v


class BaseGroup(BaseNode):
    collection: str = Field("groups", const=True)
