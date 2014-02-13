# Create your views here.
from models import *
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import sys
import datetime



 
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
    
def index(request, message=None):
    dictionary = {}
    if request.user.is_authenticated():
        user = User.objects.get(pk = request.user.id)
        boards=Board.objects.filter(user = user)
        dictionary['boards'] = boards
        dictionary['user'] = user
    else:
        pass
    return render_to_response('base.html', dictionary, 
        context_instance=RequestContext(request))

def rickandmorty(request):
    dictionary = {}
    user = User.objects.get(username = 'rickandmorty')
    boards=Board.objects.filter(user = user)
    dictionary['boards'] = boards
    dictionary['user'] = user
    
    return render_to_response('base.html', dictionary, 
        context_instance=RequestContext(request))


def new_board(request):
    context = RequestContext(request)
    if request.user == None:
        print >>sys.stderr, 'no user'
        return render_to_response('new_user.html', {})
    user = User.objects.get(username = request.user.username)
    if request.method == 'POST': 
        print request.POST
        b = Board(name = request.POST['name'],
                 user = user,
                 priority = 0,
                 )
        b.save()
    return HttpResponseRedirect('/')
    

def new_task(request, board_id):
    #add a please join or login message
    context = RequestContext(request)
    if request.user == None:
        print >>sys.stderr, 'no user'
        return render_to_response('new_user.html', {})
    if request.method == 'POST': # If the form has been submitted...\
        print request.POST
        board = Board.objects.get(pk = board_id)
        print board
        t = Task(name = request.POST['name'],
                 board = board,
                 priority = 0,
                 )
        t.save()
        print t
        return HttpResponseRedirect('/')

    return render_to_response('base.html', {
        
    }, context)

def complete_task(request, task_id):
    t = Task.objects.get(pk= task_id)
    t.completed = True
    t.save()
    return HttpResponseRedirect('/')

def delete_board(request, board_id):
    b = Board.objects.get(pk= board_id)
    b.delete()
    return HttpResponseRedirect('/')

def login_user(request):
    #add a please join or login message
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        print >>sys.stderr, form.is_valid()
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u = authenticate(username=username, password=password)
            if u is not None:
                login(request, u)
            else:
                return HttpResponseRedirect('/new_user/')
            return index(request, message = 'loggedin') # Redirect after POST
    else:
        form = LoginForm() # An unbound form

    return render_to_response('base.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return index(request)

def new_user(request):
    dictionary = {}
    if request.method == 'POST': # If the form has been submitted...
        form = UserForm(request.POST) # A form bound to the POST 
        print >>sys.stderr, form.errors
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username, email, password)
            except:
                dictionary['error'] = 'Username is taken'
            up = UserProfile(user = user, description = description, location = location)
            up.save()

            return index(request, message = 'newuser') # Redirect after POST
            print user
    else:
        form = TaskForm() # An unbound form
    dictionary['form'] = form
    return render_to_response('new_user.html', dictionary, context_instance=RequestContext(request))



def user_detail(request, username):
    user = User.objects.get(username = username)
    tasks = user.task_set.all()
    comments = Comment.objects.filter(user = user)
    profile = UserProfile.objects.get(user = user)

    return render_to_response('user_detail.html', {
        'user': user,
        'profile': profile,
        'tasks': tasks,
        'comments': comments,
    }, context_instance=RequestContext(request))    

def join(request, task_id):
    
    u = User.objects.get(pk=request.user.id)
    t = Task.objects.get(pk=task_id)
    t.users.add(u)
    c = Comment(
        task=t,
        content = str(u.username) + 'has joined!',
        user = u
        )

def new_comment(request, task_id):
    if request.method == 'POST': # If the form has been submitted...
        form = CommentForm(request.POST) # A form bound to the POST 
        print >>sys.stderr, form.errors
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            print >>sys.stderr, 'is_valid'
            content = form.cleaned_data['content']
            user = User.objects.get(pk=request.user.id)
            t = Task.objects.get(pk=task_id)
            c = Comment(user = user, content = content, task = task)

            return task_detail(request, task_id = task_id) # Redirect after POST
            print user
    else:
        form = CommentForm() # An unbound form

    return render_to_response('new_user.html', {
        'form': form,
    }, context_instance=RequestContext(request))

