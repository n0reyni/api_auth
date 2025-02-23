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
        return JsonResponse({"details":"Vous n'êtes pas connectés !"}, status=400)
    data = json.loads(request.body)
    username = data.get('email')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({"details":"Veuillez fournir l'email et le mot de passe !"}, status=400)
    
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"details":"Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"details":"Connexion Réussie !"})


@csrf_exempt
def logout_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"You are not logged in"}, status=400)
    logout(request)
    return JsonResponse({"details":"Logout successful"})

@csrf_exempt
@ensure_csrf_cookie
def session_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False}, status=400)
    return JsonResponse({"is_authenticated":True})

@csrf_exempt
def whoami_views(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False}, status=400)
    return JsonResponse({"username":request.user.username})

@require_POST
@csrf_exempt
def sign_up(request):
    if request.user.is_authenticated:
        return JsonResponse({"details": "Vous êtes déjà connecté"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"details": "Invalid JSON format"}, status=400)

    username = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    date_naissance = data.get('date_naissance')

    # Check for required fields
    if not username or not password:
        return JsonResponse({"details": "Please provide both email and password"}, status=400)

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"details": "Email déjà utilisé"}, status=400)

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name or "",
            last_name=last_name or ""
        )

        # Example: If you have a custom profile model for date_naissance, handle it here
        # profile = UserProfile.objects.create(user=user, date_naissance=date_naissance)
        # profile.save()

        user.save()
        return JsonResponse({"details": "Utilisateur créé avec succès"}, status=201)

    except Exception as e:
        return JsonResponse({"details": f"Erreur lors de la création de l'utilisateur: {str(e)}"}, status=500)

@csrf_exempt
def refresh_session(request):
    if not request.user.is_authenticated:
        return JsonResponse({"details":"You are not logged in"}, status=400)
    request.session.set_expiry(120)
    return JsonResponse({"details":"Session refreshed"})
