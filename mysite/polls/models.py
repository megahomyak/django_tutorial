import datetime

from django.contrib import admin
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @property
    @admin.display(
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        # noinspection PyTypeChecker
        return (
            self.pub_date <= now
        ) and (self.pub_date + datetime.timedelta(days=1)) >= now

    @classmethod
    def get_valid_questions_query(cls):
        """
        Excludes any questions that aren't published yet or do not have any
        choices.
        """
        # noinspection PyUnresolvedReferences
        query = cls.objects.filter(
            Exists(Choice.objects.filter(question=OuterRef("pk"))),
            pub_date__lte=timezone.now(),
        )
        return query


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
