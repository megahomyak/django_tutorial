import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @property
    def was_published_recently(self):
        now = timezone.now()
        # noinspection PyTypeChecker
        return (
            self.pub_date <= now
        ) and (self.pub_date + datetime.timedelta(days=1)) >= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
