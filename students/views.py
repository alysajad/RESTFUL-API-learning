from django.shortcuts import render
from django.http import HttpResponse

# Create your views here

def students(request):
    students=[
        {'id':1, 'name':'Alice'},
        {'id':2, 'name':'Bob'},
    ]
    return HttpResponse(students)