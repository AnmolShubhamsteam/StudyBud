from django.shortcuts import render,redirect
from django.http import HttpResponse as res
from .models import Room
from.models import Topic,Message
from .forms import RoomForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 


def login_page(request):
    page="login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
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
        return render(request, "home/login_reg.html", {"page":page})
    
def log_out(request):
    logout(request)
    return redirect("home")

def registerUser(request):
    form = UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"An Error Occured")
    context={"form": form} 
    return render(request,"home/login_reg.html",context)

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
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q)).order_by("-created")
    return render(request, "home/home.html", context={"rooms": rooms, "Topics": topics,"count":Room_count,"room_messages":room_messages})

def room(request, pk):
    r1=Room.objects.get(id=pk)
    room_messages=r1.message_set.all().order_by("-created")
    participants=r1.participants.all()
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=r1,
            body=request.POST.get("body")
        )
        r1.participants.add(request.user)
        return redirect("room",pk=r1.id)
    context={"r1":r1,"room_messages":room_messages,"participants":participants}
    return render(request,"home/room.html",context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # include all rooms associated with user
    rooms = user.room_set.all() 
    Topics=Topic.objects.all()
    room_messages = Message.objects.filter(user=user)
    context = {"user": user,"rooms":rooms,"room_messages":room_messages,"Topics":Topics}
    return render(request, "home/profile.html", context)



@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # Corrected line
            room.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "home/room_form.html", context)

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

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return res("You are not allowed to delete this message.")
    if request.method == "POST":
        message.delete()
        # Redirect the user back to the room page
        # return redirect("room", pk=message.room.id)
        return redirect("home")
    context = {"message": message}
    return render(request, "home/delete-message.html", context)
    
