from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.models import Building, Organization
from app.database.schemas import BuildingResponse, GeoSearch, OrganizationResponse
from app.services.organization_service import OrganizationService
from sqlalchemy.orm import Session, joinedload

class BuildingService:
    @staticmethod
    def get_all_buildings(db: Session) -> List[BuildingResponse]:
        buildings = db.query(Building).all()
        return [BuildingResponse.model_validate(building) for building in buildings]

    @staticmethod
    def get_organizations_in_radius(db: Session, geo_search: GeoSearch) -> List[OrganizationResponse]:
        if geo_search.radius_km:

            earth_radius_km = 6371
            
            lat_rad = func.radians(geo_search.latitude)
            lng_rad = func.radians(geo_search.longitude)
            
            building_lat_rad = func.radians(Building.latitude)
            building_lng_rad = func.radians(Building.longitude)
        
            dlat = building_lat_rad - lat_rad
            dlng = building_lng_rad - lng_rad
            
            a = a = func.pow(func.sin(dlat/2), 2) + func.cos(lat_rad) * func.cos(building_lat_rad) * func.pow(func.sin(dlng/2), 2)
            c = 2 * func.asin(func.sqrt(a))
            distance = earth_radius_km * c
            
            buildings_in_radius = db.query(Building).filter(distance <= geo_search.radius_km).all()
            
        else:
            buildings_in_radius = db.query(Building).filter(
                Building.latitude >= geo_search.min_lat,
                Building.latitude <= geo_search.max_lat,
                Building.longitude >= geo_search.min_lng,
                Building.longitude <= geo_search.max_lng
            ).all()
        
        building_ids = [building.id for building in buildings_in_radius]
        organizations = db.query(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities)
        ).filter(Organization.building_id.in_(building_ids)).all()
        
        return [OrganizationResponse.model_validate(org) for org in organizations]

    @staticmethod
    def get_building_by_id(db: Session, building_id: int) -> BuildingResponse:
        building = db.query(Building).filter(Building.id == building_id).first()
        if building:
            return BuildingResponse.model_validate(building)
        return None