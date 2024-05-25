from django.shortcuts import render
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@require_POST
@csrf_exempt
def login_views(request):
    if request.user.is_authenticated:
        return JsonResponse({"details":"You are already logged in"}, status=400)
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({"details":"Please provide both username and password"}, status=400)
    
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"details":"Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"details":"Login successful"})

def logout_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"You are not logged in"}, status=400)
    logout(request)
    return JsonResponse({"details":"Logout successful"})

@ensure_csrf_cookie
def session_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False}, status=400)
    return JsonResponse({"is_authenticated":True})

def whoami_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False}, status=400)
    return JsonResponse({"username":request.user.username})

@require_POST
@csrf_exempt
def sign_up(request):
    if request.user.is_authenticated:
        return JsonResponse({"details":"You are already logged in"}, status=400)
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({"details":"Please provide both username and password"}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"details":"Username already exists"}, status=400)
    
    user = User.objects.create_user(username=username, password=password)
    
    if user.save():
        return JsonResponse({"details":"User created"})

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"details":"Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"details":"Sign-up and authentification successful"})

def refresh_session(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"You are not logged in"}, status=400)
    request.session.set_expiry(120)
    return JsonResponse({"details":"Session refreshed"})
