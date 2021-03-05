from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Sum
import datetime

from .models import User, Transaction

# Create your views here.

def index(request):
    if request.method == "POST":
        tran = Transaction()
        form = createTransaction(request.POST)
        if form.is_valid():
            tran.user = request.user
            tran.category = form.cleaned_data['category']
            tran.description = form.cleaned_data['descr']
            if form.cleaned_data['value'] >= 0:
                tran.credit = form.cleaned_data['value']
            else:
                tran.debit = form.cleaned_data['value']
            tran.save()
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tracker/index.html", {
            "form": createTransaction(),
            "trans": Transaction.objects.all().filter(user=request.user, created__year=datetime.datetime.now().year, 
                      created__month=datetime.datetime.now().month),
            "credit": Transaction.objects.filter(user=request.user).aggregate(Sum('credit')),
            "debit": Transaction.objects.filter(user=request.user).aggregate(Sum('debit')),
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tracker/register.html")

category_choices = (
    ("Food", "Food"),
    ("Income", "Income"),
    ("Transport", "Transport"),
    ("Bills", "Bills"),
    ("Clothes", "Clothes")


)


class createTransaction(forms.Form):
    category = forms.ChoiceField(choices=category_choices)
    descr = forms.CharField(label="Description",
                            widget=forms.TextInput())
    value = forms.DecimalField(label="Value")


def edit(request, uuid):
    if request.method == "POST":
        tran = Transaction()
        form = createTransaction(request.POST)
        if "delete" in request.POST:
            Transaction.objects.all().filter(uuid=uuid).first().delete()
    
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

