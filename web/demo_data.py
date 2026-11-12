"""Sample data for demos/video: a teacher, several exams and graded submissions from a few students."""
import random

from models import Exam, Question, Submission, User, db

EXAMS = [
    {
        "title": "Cloud Computing - Midterm Quiz",
        "description": "Fundamentals of AWS, Azure and cloud service models.",
        "duration": 15, "pass": 50, "published": True,
        "questions": [
            ("Which AWS service is used for object storage?", ["Amazon EC2", "Amazon S3", "Amazon RDS", "AWS Lambda"], [1]),
            ("What is Microsoft Entra ID used for?", ["File storage", "Identity & access management", "Running containers", "Sending email"], [1]),
            ("Which of these services are serverless?", ["AWS Lambda", "Amazon EC2", "Azure Functions", "Azure Virtual Machines"], [0, 2]),
            ("What is an S3 presigned URL for?", ["Granting temporary access to an object", "Deleting a bucket", "Creating an IAM user", "Encrypting a disk"], [0]),
            ("Which service model does Azure SQL Database belong to?", ["IaaS", "PaaS", "SaaS", "On-premises"], [1]),
            ("Which model combines several cloud providers?", ["Single-cloud", "Multi-cloud", "Private cloud", "Edge"], [1]),
        ],
    },
    {
        "title": "Cloud Security Basics",
        "description": "IAM, encryption and the principle of least privilege.",
        "duration": 10, "pass": 60, "published": True,
        "questions": [
            ("What does the 'least privilege' principle mean?", ["Give admins full access", "Grant only the minimum permissions needed", "Never use passwords", "Turn off logging"], [1]),
            ("Which services store secrets securely?", ["AWS Secrets Manager", "A public S3 bucket", "Azure Key Vault", "A spreadsheet"], [0, 2]),
            ("What does MFA stand for?", ["Multi-Factor Authentication", "Main File Access", "Multi-Function App", "Managed Firewall"], [0]),
            ("When should you enable S3 'Block Public Access'?", ["Never", "When the bucket holds private data", "Only when hosting a website", "Only with Lambda"], [1]),
        ],
    },
    {
        "title": "Course Satisfaction Survey",
        "description": "Draft - not yet published to students.",
        "duration": 5, "pass": 0, "published": False,
        "questions": [
            ("How useful did you find this course?", ["Very useful", "Useful", "Neutral", "Not useful"], [0, 1, 2, 3]),
        ],
    },
]

STUDENTS = ["Emma Nguyen", "Liam Tran", "Olivia Le", "Noah Pham", "Ava Vo", "Lucas Dang"]


def seed_demo(app, grade_fn):
    """grade_fn(submission) grades and saves one submission (the app's normal grading path)."""
    if Exam.query.first():
        return False
    rng = random.Random(42)
    teacher = User(external_id="dev:teacher@demo.local", name="Dr. Sarah Mitchell", email="teacher@demo.local",
                   role="teacher")
    db.session.add(teacher)
    exams = []
    for spec in EXAMS:
        exam = Exam(title=spec["title"], description=spec["description"], duration_minutes=spec["duration"],
                    pass_percent=spec["pass"], published=spec["published"], teacher=teacher)
        for i, (text, opts, correct) in enumerate(spec["questions"]):
            exam.questions.append(Question(text=text, options=opts, correct=correct, points=1, position=i))
        db.session.add(exam)
        exams.append(exam)
    db.session.commit()

    for idx, name in enumerate(STUDENTS):
        email = f"student{idx + 1}@demo.local"
        student = User(external_id=f"dev:{email}", name=name, email=email, role="student")
        db.session.add(student)
        db.session.commit()
        for exam in exams[:2]:
            if exam is exams[1] and idx % 2:
                continue
            skill = 0.35 + 0.6 * rng.random()
            answers = {}
            for q in exam.questions:
                if rng.random() < skill:
                    answers[str(q.id)] = list(q.correct)
                else:
                    answers[str(q.id)] = [rng.randrange(len(q.options))]
            sub = Submission(exam_id=exam.id, student_id=student.id, answers=answers)
            db.session.add(sub)
            db.session.commit()
            grade_fn(sub)
    return True
