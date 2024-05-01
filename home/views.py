from django.shortcuts import render,redirect
# from django.http import HttpResponse as res
# Create your views here.
from .models import Room
from .forms import RoomForm
# rooms=[
#     {"id":1,"name":"Learning Python"},
#     {"id":2,"name":"Learning Machine Learning"},
#     {"id":3,"name":"Learning Data Analytics"}
#     ]

def home(request):
    rooms=Room.objects.all()
    return render(request,"home/home.html",context={"rooms":rooms})
from django.shortcuts import render, get_object_or_404
def room(request, pk):
    # rooms = Room.objects.all()
    # r1 = None
    # for room in rooms:
    #     if room.id == int(pk):
    #         r1 = room
    #         break
    # if r1 is None:
    #     return render(request, "home/room_not_found.html")
    # context = {"room": r1}
    # return render(request, "home/room.html", context)
    r1=Room.objects.get(id=pk)
    context={"r1":r1}
    return render(request,"home/room.html",context)

def createRoom(request):
    form=RoomForm()
    if (request.method == "POST"):
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={"form":form}
    return render(request,"home/room_form.html",context)

def updateRoom(request,pk):
    rooms=Room.objects.get(id=pk)
    form=RoomForm(instance=rooms)
    if request.method=="POST":
        form=RoomForm(request.POST,instance=rooms)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={"form":form}
    return render (request,"home/room_form.html",context)
    
