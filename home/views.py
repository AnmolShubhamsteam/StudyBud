from django.shortcuts import render,redirect
from django.http import HttpResponse as res
from .models import Room
from.models import Topic
from .forms import RoomForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Incorrect Username")
            return render(request, "home/login_reg.html", {})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Incorrect Password or Username")
            return render(request, "home/login_reg.html", {})
    else:
        return render(request, "home/login_reg.html", {})
    
def log_out(request):
    logout(request)
    return redirect("home")

def home(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |                        
        Q(description__icontains=q) |
        Q(host__username__icontains=q)                
        )
    Room_count=rooms.count()
    topics = Topic.objects.all()
    return render(request, "home/home.html", context={"rooms": rooms, "Topics": topics,"count":Room_count})

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


@login_required(login_url="login")
def createRoom(request):
    form=RoomForm()
    if (request.method == "POST"):
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={"form":form}
    return render(request,"home/room_form.html",context)

@login_required(login_url="login")
def updateRoom(request,pk):
    rooms=Room.objects.get(id=pk)
    form=RoomForm(instance=rooms)

    if request.user!=rooms.host:
        return res("You are not allowed here")
    
    if request.method=="POST":
        form=RoomForm(request.POST,instance=rooms)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={"form":form}
    return render (request,"home/room_form.html",context)

@login_required(login_url="login")
def deleteRoom(request,pk):
    rooms=Room.objects.get(id=pk)
    if request.user!=rooms.host:
        return res("You are not allowed here")
    if request.method=="POST":
        rooms.delete()
        return redirect("home")
    context={"obj":rooms}
    return render(request,"home/delete.html",context)
    
