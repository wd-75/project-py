# Create your views here.
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Article


def home(request):
    # Create post only if logged in
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login_view")

        title = (request.POST.get("title") or "").strip()
        content = (request.POST.get("content") or "").strip()
        image = request.FILES.get("image")  # optional

        if title and content:
            Article.objects.create(title=title, content=content, image=image)

        return redirect("home")

    articles = Article.objects.all()
    return render(request, "articles/home.html", {"articles": articles})


def detail(request, pk):
    article = Article.objects.filter(id=pk).first()
    if article is None:
        return HttpResponseNotFound("Article not found")

    return render(request, "articles/detail.html", {"article": article})


@login_required
def edit(request, pk):
    article = Article.objects.filter(id=pk).first()
    if article is None:
        return HttpResponseNotFound("Article not found")

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        content = (request.POST.get("content") or "").strip()
        image = request.FILES.get("image")

        if title and content:
            article.title = title
            article.content = content
            if image:
                article.image = image
            article.save()

        return redirect("detail", pk=article.id)

    return render(request, "articles/edit.html", {"article": article})


@login_required
def delete(request, pk):
    article = Article.objects.filter(id=pk).first()
    if article is None:
        return HttpResponseNotFound("Article not found")

    if request.method == "POST":
        article.delete()
        return redirect("home")

    return render(request, "articles/delete.html", {"article": article})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    error = ""

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")

        error = "Wrong username or password."

    return render(request, "auth/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("home")
