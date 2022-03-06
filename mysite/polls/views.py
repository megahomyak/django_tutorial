from django.http import HttpResponse, Http404
from django.shortcuts import render

from polls.models import Question


def index(request):
    # noinspection PyUnresolvedReferences
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    # noinspection PyUnresolvedReferences
    try:
        # noinspection PyUnresolvedReferences
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    response = f"You're voting on question {question_id}."
    return HttpResponse(response)
