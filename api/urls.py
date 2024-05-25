from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_views, name='login'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('logout', views.logout_views, name='logout'),  
    path('session', views.session_views, name='session'),
    path('whoami', views.whoami_views, name='whoami'),
    path('refresh-session', views.refresh_session, name='refresh-session'),
]