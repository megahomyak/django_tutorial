import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days_bias):
    pub_date = timezone.now() + datetime.timedelta(days=days_bias)
    # noinspection PyUnresolvedReferences
    return Question.objects.create(
        question_text=question_text, pub_date=pub_date
    )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently, False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently should return True for questions whose pub_date
        was not older than one day (inclusive).
        """
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently, True)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently should return False for questions whose pub_date
        was older than one day (not inclusive).
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently, False)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        past_question = create_question(
            question_text="Past question.", days_bias=-30,
        )
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days_bias=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_question = create_question(
            question_text="Past question.", days_bias=-30,
        )
        create_question(question_text="Future question.", days_bias=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions in a descending
        order of their publication dates. (Newest questions come first)
        """
        older_question = create_question(
            question_text="Past question 1.", days_bias=-30,
        )
        old_question = create_question(
            question_text="Past question 2.", days_bias=-5,
        )
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [old_question, older_question],
        )
