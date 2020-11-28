from django.shortcuts import render
from django.core.paginator import Paginator

from random import randint
from app import models
from .models import *

def paginate(objects, request, per_page=2):
    page = request.GET.get('page')

    paginator = Paginator(objects, per_page)

    page_obj = paginator.get_page(page)

    return page_obj

def index(request):
	page_objects = paginate(Question.objects.hot(), request)
	return render(request, 'index.html', {
		'page_objects': page_objects,
		})

def login_page(request):
	return render(request, 'login.html', {})

def register_page(request):
	return render(request, 'register.html', {})

def settings_page(request):
	return render(request, 'settings.html', {})

def tag_page(request, tag):
	questions_tag = Question.objects.sort_by_tag(tag) 
	page_objects = paginate(questions_tag, request)
	return render(request, 'tags.html', {
		'page_objects': page_objects,
		'tag': tag
		})

def question_page(request, id):
	question = Question.objects.get(pk = id) 
	answers = Answer.objects.filter(question_id = id)
	page_objects = paginate(answers, request)
	tags = Tag.objects.filter(question__id = id)
	return render(request, 'question.html', {
		'question': question,
		'page_objects': page_objects,
		'tags' : tags
		})

def ask_page(request):
	return render(request, 'ask.html')








