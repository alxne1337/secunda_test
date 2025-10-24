from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.building_service import BuildingService
from app.services.organization_service import OrganizationService
from app.database.schemas import BuildingListResponse, BuildingResponse, GeoSearch
from app.database.schemas import OrganizationListResponse
from app.database.core import get_db

router = APIRouter(prefix="/buildings", tags=["buildings"])

@router.get("/", response_model=BuildingListResponse)
async def get_all_buildings(db: Session = Depends(get_db)):
    """Список всех зданий"""
    buildings = BuildingService.get_all_buildings(db)
    return BuildingListResponse(
        buildings=buildings,
        total=len(buildings)
    )

@router.post("/geo-search/organizations", response_model=OrganizationListResponse)
async def get_organizations_in_geo_area(
    geo_search: GeoSearch,
    db: Session = Depends(get_db)
):
    """Список организаций в заданном радиусе/прямоугольной области"""
    organizations = BuildingService.get_organizations_in_radius(db, geo_search)
    return OrganizationListResponse(
        organizations=organizations,
        total=len(organizations)
    )

@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building_by_id(
    building_id: int,
    db: Session = Depends(get_db)
):
    """Получить информацию о здании по ID"""
    building = BuildingService.get_building_by_id(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building