from django.shortcuts import render
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


def home(request):
    random_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'home.html', {'random_recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def add_edit_recipe(request, recipe_id=None):
    if recipe_id:
        recipe = Recipe.objects.get(id=recipe_id)
    else:
        recipe = None

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
