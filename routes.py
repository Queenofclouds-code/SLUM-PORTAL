import os
import json
from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import text
from model import db, Slum
from config import PHOTO_UPLOAD_FOLDER, VIDEO_UPLOAD_FOLDER
from flask import send_from_directory, make_response
from werkzeug.utils import secure_filename


slum_routes = Blueprint("slum_routes", __name__)



@slum_routes.route("/", methods=["GET"])
def landing_page():
    return render_template("index.html")


# -------------------------------------------------
# FORM PAGE
# -------------------------------------------------
@slum_routes.route("/form", methods=["GET"])
def form_page():
    return render_template("form.html")



@slum_routes.route("/map", methods=["GET"])
def map_page():
    return render_template("map.html")



# -------------------------------------------------
# DATABASE CHECK
# -------------------------------------------------
@slum_routes.route("/db-check")
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return {"status": "SUCCESS", "message": "Database connected"}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}, 500


# -------------------------------------------------
# ADD SLUM (AUTO BUFFER LOGIC)
# -------------------------------------------------
@slum_routes.route("/slum", methods=["POST"])
def add_slum():
    data = request.form

    # ---------------- BASIC INFO ----------------
    name = data.get("name")
    ward_no = data.get("ward_no")
    zone = data.get("zone")
    latitude = float(data.get("latitude"))
    longitude = float(data.get("longitude"))

    # ---------------- AUTO BUFFER ----------------
    BUFFER_METERS = 100

    buffer_geom = db.session.execute(
        text("""
            SELECT ST_Buffer(
                ST_SetSRID(ST_Point(:lon, :lat), 4326)::geography,
                :buffer
            )::geometry
        """),
        {"lon": longitude, "lat": latitude, "buffer": BUFFER_METERS}
    ).scalar()

    # ---------------- HOUSEHOLD ----------------
    total_households = data.get("total_households")
    total_population = data.get("total_population")
    avg_family_size = data.get("avg_family_size")

    # ---------------- LEGAL ----------------
    established_year = data.get("established_year")
    land_ownership = data.get("land_ownership")
    legal_status = data.get("legal_status")

    # ---------------- INFRA ----------------
    water_supply = data.get("water_supply")
    electricity = data.get("electricity")
    toilets = data.get("toilets")
    drainage = data.get("drainage")

    # ---------------- HOUSING ----------------
    structure_type = data.get("structure_type")
    roof_material = data.get("roof_material")
    flood_prone = data.get("flood_prone")

    # ---------------- FILES ----------------
    photo = request.files.get("photo")
    video = request.files.get("video")

    os.makedirs(PHOTO_UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

    photo_filename = None
    video_filename = None

    if photo and photo.filename:
       photo_filename = secure_filename(photo.filename)
       photo.save(os.path.join(PHOTO_UPLOAD_FOLDER, photo_filename))
    if video and video.filename:
       video_filename = secure_filename(video.filename)
       video.save(os.path.join(VIDEO_UPLOAD_FOLDER, video_filename))

    # ---------------- SAVE ----------------
    slum = Slum(
        name=name,
        ward_no=ward_no,
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        boundary=buffer_geom,
        photo=photo_filename,
        video=video_filename,

        total_households=total_households,
        total_population=total_population,
        avg_family_size=avg_family_size,

        established_year=established_year,
        land_ownership=land_ownership,
        legal_status=legal_status,

        water_supply=water_supply,
        electricity=electricity,
        toilets=toilets,
        drainage=drainage,

        structure_type=structure_type,
        roof_material=roof_material,
        flood_prone=flood_prone
    )

    db.session.add(slum)
    db.session.commit()

    return jsonify({
        "status": "SUCCESS",
        "message": "Slum survey saved successfully"
    })


def compute_overall_status(row):
    statuses = [
        row.admin_status,
        row.demography_status,
        row.legal_verify_status,
        row.infrastructure_status,
        row.housing_status,
        row.gis_status
    ]

    if "Rejected" in statuses:
        return "Rejected"
    elif all(s == "Verified" for s in statuses):
        return "Verified"
    else:
        return "Pending"




# -------------------------------------------------
# GET SLUMS AS GEOJSON (FOR MAP)
# -------------------------------------------------
@slum_routes.route("/slums", methods=["GET"])
def get_slums():
    result = db.session.execute(text("""
    SELECT
        id,
        name,
        ward_no,
        zone,
        photo,
        video,
        admin_status,
        demography_status,
        legal_verify_status,
        infrastructure_status,
        housing_status,
        gis_status,
        ST_AsGeoJSON(boundary) AS geom
    FROM slums
"""))


    features = []

    for row in result:
        features.append({
            "type": "Feature",
            "geometry": json.loads(row.geom),
            "properties": {
    "id": row.id,
    "name": row.name,
    "ward_no": row.ward_no,
    "zone": row.zone,
    "photo": row.photo,
    "video": row.video,
    "status": compute_overall_status(row)
}

        })

    return {
        "type": "FeatureCollection",
        "features": features
    }


@slum_routes.route("/login", methods=["GET"])
def department_login():
    return render_template("department.html")

@slum_routes.route("/verify/admin")
def verify_admin():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.ward_no,
        Slum.zone,
        Slum.latitude,
        Slum.longitude,
        Slum.admin_status
    ).all()

    return render_template(
        "verify/admin.html",
        slums=slums
    )
@slum_routes.route("/verify/demography")
def verify_demography():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.total_households,
        Slum.total_population,
        Slum.avg_family_size,
        Slum.demography_status
    ).all()

    return render_template(
        "verify/demography.html",
        slums=slums
    )
@slum_routes.route("/verify/legal")
def verify_legal():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.established_year,
        Slum.legal_status,
        Slum.land_ownership,
        Slum.legal_verify_status
    ).all()

    return render_template(
        "verify/legal.html",
        slums=slums
    )
@slum_routes.route("/verify/infrastructure")
def verify_infrastructure():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.water_supply,
        Slum.electricity,
        Slum.toilets,
        Slum.drainage,
        Slum.infrastructure_status
    ).all()

    return render_template(
        "verify/infrastructure.html",
        slums=slums
    )
@slum_routes.route("/verify/housing")
def verify_housing():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.structure_type,
        Slum.roof_material,
        Slum.flood_prone,
        Slum.housing_status
    ).all()

    return render_template(
        "verify/housing.html",
        slums=slums
    )
@slum_routes.route("/verify/gis")
def verify_gis():
    slums = Slum.query.with_entities(
         Slum.id,
        Slum.name,
        Slum.boundary,
        Slum.photo,
        Slum.video,
        Slum.gis_status
    ).all()

    return render_template(
        "verify/gis.html",
        slums=slums
    )

@slum_routes.route("/update/admin-status", methods=["POST"])
def update_admin_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.admin_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})
@slum_routes.route("/update/demography-status", methods=["POST"])
def update_demography_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.demography_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})
@slum_routes.route("/update/legal-status", methods=["POST"])
def update_legal_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.legal_verify_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})
@slum_routes.route("/update/infrastructure-status", methods=["POST"])
def update_infrastructure_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.infrastructure_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})
@slum_routes.route("/update/housing-status", methods=["POST"])
def update_housing_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.housing_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})
@slum_routes.route("/update/gis-status", methods=["POST"])
def update_gis_status():
    data = request.get_json()
    slum = Slum.query.get(data["slum_id"])
    slum.gis_status = data["status"]
    db.session.commit()
    return jsonify({"success": True})

@slum_routes.route("/photos/<path:filename>")
def serve_photo(filename):
    return send_from_directory(PHOTO_UPLOAD_FOLDER, filename)


@slum_routes.route("/videos/<path:filename>")
def serve_video(filename):
    response = make_response(
        send_from_directory(VIDEO_UPLOAD_FOLDER, filename)
    )
    response.headers["Content-Type"] = "video/mp4"
    response.headers["Content-Disposition"] = "inline"
    return response

