from django.http import HttpResponse

from polls.models import Question


def index(request):
    # noinspection PyUnresolvedReferences
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    response = ",<br>".join(
        f'"{question.question_text}" - {question.pub_date}'
        for question in latest_question_list
    )
    return HttpResponse(response)


def detail(request, question_id):
    response = f"You're looking at question {question_id}."
    return HttpResponse(response)


def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    response = f"You're voting on question {question_id}."
    return HttpResponse(response)
