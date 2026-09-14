from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

ROLE_ADMIN = "admin"
ROLE_TEACHER = "teacher"
ROLE_STUDENT = "student"

LEVEL_ELEMENTARY = "elementary"
LEVEL_JUNIOR_HIGH = "junior_high"
LEVEL_SENIOR_HIGH = "senior_high"
LEVEL_COLLEGE = "college"

LEVEL_CHOICES = [
    (LEVEL_ELEMENTARY, "Elementary"),
    (LEVEL_JUNIOR_HIGH, "Junior High School"),
    (LEVEL_SENIOR_HIGH, "Senior High School"),
    (LEVEL_COLLEGE, "College"),
]
LEVEL_LABELS = dict(LEVEL_CHOICES)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_STUDENT)
    grade_level = db.Column(db.String(30), nullable=True)  # e.g. 'elementary' — students only
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subjects_taught = db.relationship(
        "Subject", backref="teacher", lazy=True, foreign_keys="Subject.teacher_id"
    )
    enrollments = db.relationship(
        "Enrollment", backref="student", lazy=True, foreign_keys="Enrollment.student_id"
    )
    attempts = db.relationship(
        "ExamAttempt", backref="student", lazy=True, foreign_keys="ExamAttempt.student_id"
    )

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def is_teacher(self):
        return self.role == ROLE_TEACHER

    def is_student(self):
        return self.role == ROLE_STUDENT

    def grade_level_label(self):
        return LEVEL_LABELS.get(self.grade_level, "—")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(30), nullable=False, default=LEVEL_JUNIOR_HIGH)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    passing_score = db.Column(db.Integer, default=75)  # percentage required to pass
    time_limit_minutes = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship(
        "Question", backref="subject", lazy=True, cascade="all, delete-orphan"
    )
    enrollments = db.relationship(
        "Enrollment", backref="subject", lazy=True, cascade="all, delete-orphan"
    )
    attempts = db.relationship(
        "ExamAttempt", backref="subject", lazy=True, cascade="all, delete-orphan"
    )

    def question_count(self):
        return len(self.questions)

    def level_label(self):
        return LEVEL_LABELS.get(self.level, self.level)


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("student_id", "subject_id", name="uq_student_subject"),
    )


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    choice_a = db.Column(db.String(500), nullable=False)
    choice_b = db.Column(db.String(500), nullable=False)
    choice_c = db.Column(db.String(500), nullable=False)
    choice_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A' | 'B' | 'C' | 'D'
    image_filename = db.Column(db.String(255), nullable=True)  # optional, in static/question_images/

    def choices(self):
        return {
            "A": self.choice_a,
            "B": self.choice_b,
            "C": self.choice_c,
            "D": self.choice_d,
        }


class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    answers = db.relationship(
        "ExamAnswer", backref="attempt", lazy=True, cascade="all, delete-orphan"
    )

    def letter_grade(self):
        """A standard A–F letter grade based on percentage score.

        This is independent of the subject's PASSED/FAILED threshold
        (passing_score), which can be set to any percentage per subject —
        this letter grade is just the conventional 90/80/70/60 scale.
        """
        pct = self.percentage
        if pct >= 90:
            return "A"
        if pct >= 80:
            return "B"
        if pct >= 70:
            return "C"
        if pct >= 60:
            return "D"
        return "F"


class ExamAnswer(db.Model):
    __tablename__ = "exam_answers"

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("exam_attempts.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship("Question")
