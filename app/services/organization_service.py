from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from typing import List, Optional
from app.database.models import Organization, Building, Activity, OrganizationPhone
from app.database.schemas import OrganizationResponse, BuildingBase, ActivityBase, PhoneBase

class OrganizationService:
    @staticmethod
    def get_organizations_by_building(db: Session, building_id: int) -> List[OrganizationResponse]:
        organizations = db.query(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities)
        ).filter(Organization.building_id == building_id).all()
        
        return [OrganizationResponse.model_validate(org) for org in organizations]

    @staticmethod
    def get_organizations_by_activity(db: Session, activity_id: int) -> List[OrganizationResponse]:
        query = text("""
            WITH RECURSIVE activity_tree AS (
                SELECT id FROM activities WHERE id = :activity_id
                UNION
                SELECT a.id FROM activities a
                INNER JOIN activity_tree at ON a.parent_id = at.id
                WHERE a.level <= 3
            )
            SELECT o.id FROM organizations o
            JOIN organization_activities oa ON o.id = oa.organization_id
            WHERE oa.activity_id IN (SELECT id FROM activity_tree)
        """)
        result = db.execute(query, {'activity_id': activity_id})
        organization_ids = [row[0] for row in result]
        
        # Получаем организации с полными данными
        organizations = db.query(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities)
        ).filter(Organization.id.in_(organization_ids)).all()
        
        return [OrganizationResponse.model_validate(org) for org in organizations]

    @staticmethod
    def search_organizations_by_name(db: Session, name: str) -> List[OrganizationResponse]:
        organizations = db.query(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities)
        ).filter(
            Organization.name.ilike(f"%{name}%")
        ).all()
        
        return [OrganizationResponse.model_validate(org) for org in organizations]

    @staticmethod
    def get_organization_by_id(db: Session, organization_id: int) -> Optional[OrganizationResponse]:
        organization = db.query(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities)
        ).filter(Organization.id == organization_id).first()
        
        if organization:
            return OrganizationResponse.model_validate(organization)
        return None