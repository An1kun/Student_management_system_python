from django.db import models

from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    date = models.DateField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade}"
