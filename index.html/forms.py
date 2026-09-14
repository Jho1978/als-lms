from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange, EqualTo

from models import LEVEL_CHOICES


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])


class CreateUserForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=120)])
    grade_level = SelectField(
        "Grade Level (students only)",
        choices=[("", "-- N/A --")] + LEVEL_CHOICES,
        validators=[Optional()],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )


class SubjectForm(FlaskForm):
    name = StringField("Subject Name", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=255)])
    level = SelectField("School Level", choices=LEVEL_CHOICES, validators=[DataRequired()])
    teacher_id = SelectField("Assign Teacher", coerce=int, validators=[Optional()])
    passing_score = IntegerField(
        "Passing Score (%)", default=75, validators=[DataRequired(), NumberRange(min=1, max=100)]
    )
    time_limit_minutes = IntegerField(
        "Time Limit (minutes)", default=60, validators=[DataRequired(), NumberRange(min=1, max=600)]
    )


class QuestionForm(FlaskForm):
    question_text = TextAreaField(
        "Question", validators=[DataRequired(), Length(max=1000)], render_kw={"rows": 2}
    )
    image = FileField(
        "Question Image (optional)",
        validators=[Optional(), FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "Images only!")],
    )
    choice_a = StringField("Choice A", validators=[DataRequired(), Length(max=500)])
    choice_b = StringField("Choice B", validators=[DataRequired(), Length(max=500)])
    choice_c = StringField("Choice C", validators=[DataRequired(), Length(max=500)])
    choice_d = StringField("Choice D", validators=[DataRequired(), Length(max=500)])
    correct_answer = SelectField(
        "Correct Answer",
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        validators=[DataRequired()],
    )


class BulkAddStudentsForm(FlaskForm):
    names = TextAreaField(
        "Student Names",
        validators=[DataRequired()],
        render_kw={"rows": 10, "placeholder": "Maria Santos\nJuan Dela Cruz\nAna Reyes"},
    )
    grade_level = SelectField(
        "Grade Level (applied to everyone in the list)",
        choices=[("", "-- N/A --")] + LEVEL_CHOICES,
        validators=[Optional()],
    )
    subject_id = SelectField(
        "Enroll everyone in this subject now (optional)",
        coerce=int,
        validators=[Optional()],
    )


class UploadQuestionsForm(FlaskForm):
    file = FileField(
        "Questionnaire File (.xlsx or .csv)",
        validators=[FileRequired(), FileAllowed(["xlsx", "csv"], "Excel or CSV files only!")],
    )
