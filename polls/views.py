from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

# Getting all the polls list and displaying them
def index(request):
    latest_questions = Question.objects.order_by('-publish_date')[:10]
    context = { 'latest_questions' : latest_questions }
    return render(request, 'polls/index.html', context)

# Show choices for a specific question
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: 
        raise Http404("Question Not Found!")
    context = { 'question' : question,
        'choices' : question.choice_set.all()
    }
    return render(request, 'polls/detail.html', context)

# Get question and show results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question' : question,
        'choices' : question.choice_set.order_by('-votes')
     }
    return render(request, 'polls/results.html', context)

# Vote for a question choice
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = { 'question' : question,
            'choices' : question.choice_set.all(),
            'error_message' : "You did not selected a choice"
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))

    
        