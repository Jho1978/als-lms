# Campus LMS — Flask Learning Management System

A complete Flask + SQLite LMS with Admin / Teacher / Student roles, subject
enrollment, Excel/CSV-based question import, auto-graded 50-question
multiple-choice exams, and results history.

## Features

- Landing page, unified login, and student self-registration
- **Admin:** create teacher & student accounts, create subjects, assign
  teachers to subjects, view all exam results
- **Teacher:** create subjects, then build the test questionnaire either by
  **adding questions one at a time in the app** or by **uploading a
  questionnaire file** (`.xlsx` or `.csv`) — or both, mixed together; set
  the passing score and time limit; view and delete individual questions;
  view student scores
- **Student:** view subjects a teacher/admin has enrolled them in, take a
  timed, randomized multiple-choice exam, get an instant auto-graded score,
  review past attempts with per-question answer review. **Students cannot
  self-enroll** — only a teacher or admin can enroll them in a subject.
- Flask-Login session auth, Werkzeug password hashing, CSRF protection
  (Flask-WTF) on every form, role-based access control on every route
- Subjects are organized by **school level** — Elementary, Junior High
  School, Senior High School, or College — and students accounts can
  optionally record a grade level too
- Randomized question order and randomized A/B/C/D choice order per attempt
- **Manual enrollment only**: teachers and admins enroll or remove specific
  students on a subject (searchable/filterable by grade level) — there is
  no student-facing "enroll" option anywhere in the app
- **Bulk Add Students**: teachers and admins can paste a whole class list
  (one name per line) and the system creates every student account
  automatically — auto-generated username, auto-generated temporary
  password, optional grade level, and optional instant enrollment into a
  chosen subject — all in a single click
- **Images in test questions**: when adding a question manually, teachers
  can attach a photo, diagram, or chart (PNG/JPG/GIF/WebP) — it's shown to
  the student above the question during the exam and again in the answer
  review
- **Excel results export**: every results page (a teacher's subject, the
  admin's all-results view, and a student's own history) has an "Export to
  Excel" button — auto-calculates each student's score, percentage, a
  standard letter grade (A–F), and PASS/FAIL, and downloads it as a
  ready-to-print, formatted `.xlsx` file
- **Editable exam timer**: teachers and admins can change a subject's time
  limit (and passing score) any time after creation — and every attempt,
  including retakes, always starts with its own full, fresh timer
- Countdown exam timer that auto-submits when time runs out
- SQLite database (auto-created on first run) via SQLAlchemy

## Setup

### Windows — one-click launcher

Just double-click **`start_lms.bat`** inside the project folder. The first
time you run it, it will:

1. Check that Python is installed (if not, it tells you where to get it)
2. Create a local virtual environment and install the required packages
3. Start the server in its own window titled **"Campus LMS Server"**
4. Open your browser to `http://localhost:5000` automatically

Next time, just double-click it again — it starts much faster since the
packages are already installed. **To stop the app, close the "Campus LMS
Server" window.**

### Manual setup (Windows/Mac/Linux)

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The app runs at **http://localhost:5000**.

On first run it creates `instance/lms.db` automatically and seeds a default
admin account:

- **Username:** `admin`
- **Password:** `admin123`

**Change this password immediately** (or create a new admin manually in the
database) before using this anywhere beyond local testing.

## Typical workflow

1. Log in as `admin` → **Teachers** tab → create a teacher account.
2. Log in as that teacher → **New Subject** → create e.g. "Mathematics"
   (set passing score / time limit) → you're taken straight to the
   question-builder page for that subject.
3. On the question-builder page, either:
   - Use the **Add Question Manually** tab to type in one MCQ at a time
     (question text, choices A–D, and the correct answer) — the form
     clears after each submit so you can keep going, or
   - Use the **Upload Excel/CSV** tab to bulk-import a whole test at once
     (see `sample_questionnaire.xlsx`, 50 sample math questions, included
     in this folder). You can mix both — upload a batch, then add a few
     more manually, or vice versa.

   Every question you add appears in the list below with a delete button,
   so the teacher can review and edit the test before students take it.
   The file format, if you use the upload option:

   | Question | A | B | C | D | Answer |
   |---|---|---|---|---|---|
   | What is 2+2? | 1 | 2 | 3 | 4 | D |
   | Capital of France? | London | Paris | Rome | Berlin | B |

   The `Answer` column must contain exactly one letter: `A`, `B`, `C`, or `D`.
4. Register a student account (or have the admin create one).
5. As the teacher or admin, open the subject → **Students** (or **Enroll
   Students**) → find the student and click **Enroll**. Students cannot
   enroll themselves — this step is required before they can see the
   subject at all.
6. The student logs in and sees the subject on their dashboard → **Take
   Exam**. It's graded instantly; the student sees PASS/FAIL, their score,
   and a full answer review. Admin and the subject's teacher can see every
   attempt under **Results**.

## Project structure

```
lms/
├── start_lms.bat              # Windows double-click launcher
├── app.py                  # routes, app factory, Excel/CSV import logic
├── config.py                # configuration (secret key, DB path, upload limits)
├── extensions.py            # SQLAlchemy / Flask-Login / CSRF singletons
├── models.py                 # User, Subject, Enrollment, Question, ExamAttempt, ExamAnswer
├── forms.py                  # Flask-WTF forms (login, create user, subject, upload)
├── requirements.txt
├── sample_questionnaire.xlsx # 50 sample math questions, ready to upload
├── sample_questionnaire.csv
├── templates/                # Jinja2 + Bootstrap 5 templates
│   ├── base.html, index.html, login.html, register.html, error.html
│   ├── admin/    (dashboard, teachers, students, subjects, results)
│   ├── teacher/  (dashboard, create_subject, edit_subject, manage_questions, manage_enrollment, bulk_add_students, results)
│   └── student/  (dashboard, take_exam, results, result_detail)
├── static/css/style.css
└── instance/lms.db           # created automatically on first run
```

## Notes on scope

This is a solid, working core of the system you described. A few of the
"nice-to-have" items on your feature list were intentionally left out to
keep this a clean, reviewable codebase rather than a sprawling one — they'd
each be a focused add-on rather than a rewrite:

- **PDF/module uploads & attendance tracking** — not implemented (different
  data model; happy to add as a follow-up).
- **Certificates of completion** — the pass/fail result is already computed;
  generating a PDF certificate on top of `ExamAttempt` is a small addition
  (the `pdf` skill/library can do this).
- **Excel/PDF grade export** — teacher/admin results tables are ready to
  export; adding a "Download as Excel/PDF" button is straightforward with
  `openpyxl`/`reportlab`.
- **Email notifications** — would need an SMTP or transactional-email
  provider configured; not wired in since that requires your credentials.

Everything else on your list — auth, hashing, CSRF, role-based access,
subject creation, Excel/CSV question import, 50-question timed exams with
randomized order, automatic scoring, dashboards, and results history — is
implemented and working.
