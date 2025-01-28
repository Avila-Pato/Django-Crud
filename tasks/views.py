from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse  # Corrección de HTTPResponse
from .forms import TaskForm
from .models import Task
from django.utils import timezone

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
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(
        request, "tasks.html", {"tasks": tasks}
    )  # Crear la plantilla tasks.html


def create_task(request):
    if request.method == "GET":
        return render(request, "create_tasks.html", {"form": TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_tasks.html",
                {"form": TaskForm, "error": "Bad data passed in. Try again."},
            )


def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # INSTANCE lo que hace es instanciar el formulario con los datos de la tarea
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            # si todo sale bn y actualiza la tarea lo redirecciona
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": task, "form": form, "error": "Error updating task."},
            )


def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("tasks")  # Redirige a la página de listado de tareas


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
    if user is None:
        return render(
            request,
            "signin.html",
            {
                "form": AuthenticationForm,
                "error": "Username and password did not match.",
            },
        )
    else:
        # login(request, user) me guarda   la sesión del usuario
        login(request, user)
        return redirect("tasks")
