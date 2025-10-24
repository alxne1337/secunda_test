from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

organization_activities = Table(
    'organization_activities',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'))
    level = Column(Integer, default=1)
    
    children = relationship("Activity", back_populates="parent")
    parent = relationship("Activity", back_populates="children", remote_side=[id])

    organizations = relationship("Organization", secondary=organization_activities, back_populates="activities")

class Building(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    
    building = relationship("Building", back_populates="organizations")
    phones = relationship("OrganizationPhone", back_populates="organization")
    activities = relationship("Activity", secondary=organization_activities, back_populates="organizations")

class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    phone_number = Column(String(50), nullable=False)
    
    organization = relationship("Organization", back_populates="phones")