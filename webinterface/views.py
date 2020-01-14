from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Directories
# from django.template import loader


def index(request):
    latest_question_list = Directories.objects.all()
    context = {'tab': 'Directories', 'latest_question_list': latest_question_list}
    return render(request, 'webinterface/index.html', context)
