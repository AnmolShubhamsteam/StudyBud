from django.shortcuts import render
# from django.http import HttpResponse as res
# Create your views here.

rooms=[
    {"id":1,"name":"Learning Python"},
    {"id":2,"name":"Learning Machine Learning"},
    {"id":3,"name":"Learning Data Analytics"}
    ]


def home(request):
    return render(request,"home/home.html",context={"rooms":rooms})
def room(request,pk):
    r1=None
    for i in rooms:
        if i["id"]==int(pk):
            r1=i
    context={"r1":r1}
    return render(request,"home/room.html",context)