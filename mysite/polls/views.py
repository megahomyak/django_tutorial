from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from polls.models import Question


def index(request):
    # noinspection PyUnresolvedReferences
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = f"You're looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    response = f"You're voting on question {question_id}."
    return HttpResponse(response)
