from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()

class Slum(db.Model):
    __tablename__ = "slums"

    id = db.Column(db.Integer, primary_key=True)

    # Basic
    name = db.Column(db.String(200))
    ward_no = db.Column(db.String(50))
    zone = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Household & Population
    total_households = db.Column(db.Integer)
    total_population = db.Column(db.Integer)
    avg_family_size = db.Column(db.Integer)

    # Legal
    established_year = db.Column(db.Integer)
    land_ownership = db.Column(db.String(50))
    legal_status = db.Column(db.String(50))

    # Infrastructure
    water_supply = db.Column(db.String(50))     # Municipal / Borewell / None
    electricity = db.Column(db.String(10))      # Yes / No
    toilets = db.Column(db.String(50))           # Individual / Community / None
    drainage = db.Column(db.String(10))          # Yes / No

    # Housing
    structure_type = db.Column(db.String(50))
    roof_material = db.Column(db.String(50))
    flood_prone = db.Column(db.String(10)) 

    # Geometry & Media
    boundary = db.Column(Geometry("POLYGON", srid=4326))
    photo = db.Column(db.String)
    video = db.Column(db.String)

    # Verification Status (ADD BELOW VIDEO FIELD)
    admin_status = db.Column(db.String(20), default="Pending")
    demography_status = db.Column(db.String(20), default="Pending")
    legal_verify_status = db.Column(db.String(20), default="Pending")
    infrastructure_status = db.Column(db.String(20), default="Pending")
    housing_status = db.Column(db.String(20), default="Pending")
    gis_status = db.Column(db.String(20), default="Pending")


