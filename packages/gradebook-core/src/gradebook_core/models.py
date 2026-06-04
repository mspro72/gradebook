from dataclasses import dataclass


@dataclass
class Student:
    id: int
    name: str


@dataclass
class Subject:
    id: int
    name: str


@dataclass
class Grade:
    student_id: int
    subject_id: int
    value: int