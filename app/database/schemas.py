from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class PhoneBase(BaseModel):
    phone_number: str

    model_config = ConfigDict(from_attributes=True)

class ActivityBase(BaseModel):
    id: int
    name: str
    level: int

    model_config = ConfigDict(from_attributes=True)

class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)

class OrganizationBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class OrganizationResponse(OrganizationBase):
    building: BuildingBase
    phones: List[PhoneBase]
    activities: List[ActivityBase]

    model_config = ConfigDict(from_attributes=True)

class OrganizationListResponse(BaseModel):
    organizations: List[OrganizationResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)

class OrganizationSearch(BaseModel):
    name: Optional[str] = None
    activity_id: Optional[int] = None
    building_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class BuildingResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)

class BuildingListResponse(BaseModel):
    buildings: List[BuildingResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)

class GeoSearch(BaseModel):
    latitude: float
    longitude: float
    radius_km: Optional[float] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lng: Optional[float] = None
    max_lng: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)