import json
import random
import re

from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import Name


def home_view(request):
    context = dict()
    context['title'] = 'project'
    return render(request, template_name='home.html', context=context)

@csrf_exempt
def add_name(request):
    if request.body:
        body = json.loads(request.body.decode("utf-8"))
        context = dict()
        name = body.get('name')
        if not re.match("^[A-Za-z0-9_-]+$", name):
            context['error'] = {
                'type': 'Irregular name',
                'message': 'Name should contain only letters, numbers, hyphen or underscores'
            }
        else:
            try:
                instance = Name(name=name)
                Name.save(instance)
                names_list = [str(name) for name in Name.objects.all()]
                context['names_list'] = names_list
            except IntegrityError:
                context['error'] = {
                    'type': 'IntegrityError',
                    'message': 'This name already exists!'
                }
        return JsonResponse(context)


def get_all(request):
    context = dict()
    names_list = [str(name) for name in Name.objects.all()]
    print(names_list)
    context['names_list'] = names_list
    return JsonResponse(context)


def delete_name(request, name):
    context = dict()
    try:
        instance = Name.objects.get(name=name)
        instance.delete()
        names_list = [str(nm) for nm in Name.objects.all()]
        context['names_list'] = names_list
        print(names_list)
    except Name.DoesNotExist:
        context['error'] = {
            'type': 'DoesNotExist',
            'message': 'There isn\'t such a name in the database!'
        }
    return JsonResponse(context)


def lottery(request):
    context = dict()
    names_list = [str(nm) for nm in Name.objects.all()]
    if len(names_list) == 0:
        context['error'] = {
            'message': 'Empty database!'
        }
    elif len(names_list) < 3:
        context['winners'] = names_list
    else:
        sample = random.sample(range(len(names_list)), 3)
        context['winners'] = [names_list[number] for number in sample]
    return JsonResponse(context)

