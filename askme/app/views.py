from django.shortcuts import render
from django.core.paginator import Paginator

from random import randint

answers = []
for i in range(1,300):
	answers.append({
		'id': randint(1, 29),
		'text': 'Answer' + str(i) + '. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.'
		})

questions = []
for i in range(1,30):
  questions.append({
    'title': 'Title' + str(i), 
    'id': i,
    'text': 'Text' + str(i) + '. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam blandit nulla vitae justo accumsan malesuada. Suspendisse in laoreet ligula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec at hendrerit lectus, sed eleifend felis. Pellentesque finibus massa augue, id finibus nisl laoreet in. Integer faucibus iaculis odio, ut placerat sem mattis quis. Vivamus varius sollicitudin dictum. Vestibulum vehicula lacus nec semper finibus. Nunc eget enim vitae nisl sagittis pellentesque. Vestibulum libero lorem, bibendum fringilla magna quis, lobortis mattis justo.',
    'tag': 'tag' + str(randint(1, 5)),
    'answers_count': 0
  })

for answer in answers:
	for question in questions:
		if answer['id'] == question['id']:
			question['answers_count'] += 1

def paginate(objects, request, per_page=2):
    page = request.GET.get('page')

    paginator = Paginator(objects, per_page)

    page_obj = paginator.get_page(page)

    return page_obj

def index(request):
	page_objects = paginate(questions, request)
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
	questions_tag = [] 
	tags = []
	for question in questions:
		if question['tag'] == tag:
			questions_tag.append(question);
			tags.append(tag)
	page_objects = paginate(questions_tag, request)
	return render(request, 'tags.html', {
		'page_objects': page_objects,
		'tags': set(tags)
		})

def question_page(request, id):
	question_id = []
	answers_id = []
	for question in questions:
		if question['id'] == id:
			question_id = question
			break
	for answer in answers:
		if answer['id'] == id:
			answers_id.append(answer)
	page_objects = paginate(answers_id, request)
	return render(request, 'question.html', {
		'question': question_id,
		'page_objects': page_objects
		})

def ask_page(request):
	return render(request, 'ask.html')








