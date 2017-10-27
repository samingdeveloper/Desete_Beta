from django.contrib.auth.models import Permission, User
from django.db import models


class Classroom(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=500)
    year = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.year


class Quiz(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=250)

    def __str__(self):
        return self.quiz_title
