from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    """Студент - основная сущность системы"""

    __tablename__ = "students"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(150), unique=True, nullable=False)

    grades = db.relationship("Grade", back_populates="student", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}


class Subject(db.Model):
    """Учебный предмет"""

    __tablename__ = "subjects"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False, unique=True)

    grades = db.relationship("Grade", back_populates="subject", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


class Grade(db.Model):
    """Оценка студента по предмету. Значение от 1 до 5"""

    __tablename__ = "grades"

    id: int = db.Column(db.Integer, primary_key=True)
    student_id: int = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id: int = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    value: float = db.Column(db.Float, nullable=False)

    student = db.relationship("Student", back_populates="grades")
    subject = db.relationship("Subject", back_populates="grades")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "value": self.value,
        }