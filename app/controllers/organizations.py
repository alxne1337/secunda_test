from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.services.organization_service import OrganizationService
from app.database.schemas import OrganizationResponse, OrganizationListResponse
from app.database.core import get_db

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.get("/building/{building_id}", response_model=OrganizationListResponse)
async def get_organizations_by_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    """Список всех организаций в конкретном здании"""
    organizations = OrganizationService.get_organizations_by_building(db, building_id)
    return OrganizationListResponse(
        organizations=organizations,
        total=len(organizations)
    )

@router.get("/activity/{activity_id}", response_model=OrganizationListResponse)
async def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Список всех организаций, относящихся к указанному виду деятельности"""
    organizations = OrganizationService.get_organizations_by_activity(db, activity_id)
    return OrganizationListResponse(
        organizations=organizations,
        total=len(organizations)
    )

@router.get("/search", response_model=OrganizationListResponse)
async def search_organizations_by_name(
    name: str = Query(..., description="Название организации для поиска"),
    db: Session = Depends(get_db)
):
    """Поиск организаций по названию"""
    organizations = OrganizationService.search_organizations_by_name(db, name)
    return OrganizationListResponse(
        organizations=organizations,
        total=len(organizations)
    )

@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization_by_id(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """Получить информацию об организации по ID"""
    organization = OrganizationService.get_organization_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization