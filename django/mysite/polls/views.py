from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     print("hello world")
#     return HttpResponse("hello world, polls index")
# # Create your views here.

def index(request):
    print(1)
    context = {'latest_question_list': 'tmp'}
    return render(request, 'polls/index.html', context)

def tmp(request):
    print(1000000000000000000)
    context = {'latest_question_list': 'tmp'}
    # return render(request, 'polls/tmp.html',context)


def search_table(request): 
    search_key = request.GET['search_key'] 
    context = {'search_key':search_key} 
    print(10000000000000)
    return render(request,'only_table.html',context)
