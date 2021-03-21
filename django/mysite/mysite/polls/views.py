from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from .forms import NameForm

# def index(request):
#     print("hello world")
#     return HttpResponse("hello world, polls index")
# # Create your views here.

# def index(request):
#     print(1)
#     context = {'latest_question_list': 'tmp123123'}
#     #모델을 여기서 실행후 결과를 context에 넣어서 하면에 돌려주는곳
    
#     return render(request, 'polls/index.html', context)
def index(request):


    # print(form)
    print(10000000000000000)
    return render(request, 'polls/index.html', {'form': "asd"})
    

@csrf_protect
def tmp(request):
    
    print(1000000000000000000)

        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/polls/tmp/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    print(1000000000000000000)

    return render(request, 'polls/tmp.html',{'form':form})


def search_table(request): 
    search_key = request.GET['search_key'] 
    context = {'search_key':search_key} 
    print(10000000000000)
    return render(request,'only_table.html',context)
