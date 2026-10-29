from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.liste_articles, name='liste_articles'),
    path('article/<slug:slug>/', views.detail_article, name='detail_article'),
    path('categorie/<slug:slug>/', views.articles_par_categorie, name='articles_par_categorie'),
    path('nouvel-article/', views.creer_article, name='creer_article'),
    path('profil/<str:username>/', views.profil_utilisateur, name='profil'),
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),
    path('recherche/', views.recherche, name='recherche'), # La ligne qui manquait !
    path('article/<slug:slug>/aimer/', views.aimer_article, name='aimer_article'),
    path('commentaire/<int:pk>/aimer/', views.aimer_commentaire, name='aimer_commentaire'),
    path('notifications/', views.liste_notifications, name='notifications'),
]