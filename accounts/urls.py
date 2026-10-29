from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Connexion / Déconnexion (fournies par Django)
    path('connexion/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Inscription (codée par nous)
    path('inscription/', views.inscription, name='inscription'),
]