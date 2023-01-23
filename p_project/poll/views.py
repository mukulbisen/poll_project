from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreatePollForm
from .models import Poll
#from poll.models import Poll

""""
 •Registration/Login page 
 • User can register new account 
 • User can login into existing account  Homepage 
 • Only registered users can view this page 
 • User can view poll questions asked by other users 
 • There must be an option to create poll question  Create Poll question 
 • Users can create poll question on this page 
 • Each question must have 4 options as vote 
 • User can create up to maximum 5 questions  User Profile Page 
 • User details will be displayed on the page - name, email, phone 
 • Details cannot be edited 
 • There must be a list of questions created by this user.   
    add celery tasks in the project to delete polls which are created before 24 hours.  

"""

def home(request):
    polls = Poll.objects.all()
    context = {'polls' : polls}
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')
            print(form.cleaned_data['question'])
    else:
        form = CreatePollForm()
    context = {'form' : form}
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == "POST":
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {'poll' : poll}
    return render(request, 'poll/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {'poll':poll}
    return render(request, 'poll/results.html', context)