import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-production")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "lms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB upload limit
    ALLOWED_EXTENSIONS = {"xlsx", "csv"}
    QUESTIONS_PER_EXAM = 50  # default / max questions pulled into a single exam attempt
    QUESTION_IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "question_images")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    WTF_CSRF_TIME_LIMIT = None
