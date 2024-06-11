from django.db import models
from django.contrib.auth.models import AbstractUser

class Word(models.Model):
    word = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255)
    level = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.word}  ({self.part_of_speech})  : {self.meaning}"


class CustomUser(AbstractUser):
    word = models.CharField(max_length=255, null=True)
    openai_key = models.CharField(max_length=255, null=True)



