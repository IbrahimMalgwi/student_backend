from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
