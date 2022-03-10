from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # noinspection PyUnresolvedReferences
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        # noinspection PyUnresolvedReferences
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        # noinspection PyUnresolvedReferences
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # noinspection PyUnresolvedReferences
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice",
        })
    else:
        # F applies the changes only when you save the object to the database...
        selected_choice.votes = F("votes") + 1
        # ...but changes you made will still persist on the object, WITHOUT
        # being shared between threads (manual test below). It means that if
        # I change the value by 1 in one thread and by 1 in another, the value
        # will still be incremented by 1 in each thread, but when saving to the
        # database, these changes will merge.
        # import time
        # time.sleep(15)
        # print(selected_choice.votes)
        selected_choice.save()
        # If I do that:...
        # selected_choice.save()
        # ...again, F would be applied again, and votes
        # will be incremented by two!
        # Fix:
        selected_choice.refresh_from_db()
        selected_choice.save()  # And now it's completely safe!
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
