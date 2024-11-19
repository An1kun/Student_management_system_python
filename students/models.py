from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
