from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse  # Corrección de HTTPResponse

# Create your views here.


def home(request):
    return render(
        request, "home.html", {"form": UserCreationForm()}
    )  # Instanciando el formulario correctamente


def signup(request):
    if request.method == "GET":
        return render(
            request, "signup.html", {"form": UserCreationForm()}
        )  # Instanciando el formulario correctamente
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                return redirect("home")
            except Exception as e:
                return HttpResponse(
                    "Username already exists"
                )  # Asegúrate de manejar mejor los errores en producción
        return HttpResponse(
            "Passwords do not match"
        )  # Asegúrate de manejar esto en el frontend también
