import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PHOTO_UPLOAD_FOLDER = os.path.join(BASE_DIR, "Photos")
VIDEO_UPLOAD_FOLDER = os.path.join(BASE_DIR, "Videos")

MAX_CONTENT_LENGTH = 60 * 1024 * 1024  # 60 MB

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/slum_gis"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
