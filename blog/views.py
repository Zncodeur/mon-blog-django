from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Article, Commentaire, Categorie, Notification
from .forms import CommentaireForm, ArticleForm, ProfilForm

def liste_articles(request):
    articles = Article.objects.filter(statut='publie').annotate(nb_commentaires=Count('commentaires'))
    return render(request, 'blog/liste_articles.html', {'articles': articles})

def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug, statut='publie')
    commentaires = article.commentaires.filter(approuve=True, parent=None)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
            
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.approuve = True
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Commentaire.objects.get(id=parent_id)
                commentaire.parent = parent_comment
                # Notifier l'auteur du commentaire parent
                if parent_comment.auteur != request.user:
                    Notification.objects.create(
                        destinataire=parent_comment.auteur,
                        expediteur=request.user,
                        article=article,
                        message=f"a répondu à votre commentaire."
                    )
            else:
                # Notifier l'auteur de l'article
                if article.auteur != request.user:
                    Notification.objects.create(
                        destinataire=article.auteur,
                        expediteur=request.user,
                        article=article,
                        message=f"a commenté votre article '{article.titre}'."
                    )
                
            commentaire.save()
            return redirect('blog:detail_article', slug=article.slug)
    else:
        form = CommentaireForm()

    return render(request, 'blog/detail_article.html', {
        'article': article,
        'commentaires': commentaires,
        'form': form
    })

def articles_par_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    articles = Article.objects.filter(categorie=categorie, statut='publie')
    return render(request, 'blog/categorie.html', {'categorie': categorie, 'articles': articles})

@login_required
def creer_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            form.save_m2m()
            return redirect('blog:detail_article', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'blog/creer_article.html', {'form': form})

def profil_utilisateur(request, username):
    utilisateur = get_object_or_404(User, username=username)
    articles = utilisateur.articles.filter(statut='publie')
    return render(request, 'blog/profil.html', {'utilisateur_profil': utilisateur, 'articles': articles})

@login_required
def modifier_profil(request):
    profil = request.user.profil
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('blog:profil', username=request.user.username)
    else:
        form = ProfilForm(instance=profil)
    return render(request, 'blog/modifier_profil.html', {'form': form})

def recherche(request):
    query = request.GET.get('q')
    articles = []
    if query:
        articles = Article.objects.filter(Q(titre__icontains=query) | Q(contenu__icontains=query), statut='publie')
    return render(request, 'blog/recherche.html', {'articles': articles, 'query': query})

@login_required
def aimer_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user in article.likes.all():
        article.likes.remove(request.user)
        aime = False
    else:
        article.likes.add(request.user)
        aime = True
        # Créer une notification
        if article.auteur != request.user:
            Notification.objects.create(
                destinataire=article.auteur,
                expediteur=request.user,
                article=article,
                message=f"a aimé votre article '{article.titre}'."
            )
        
    return JsonResponse({'aime': aime, 'total_likes': article.likes.count()})

@login_required
def aimer_commentaire(request, pk):
    commentaire = get_object_or_404(Commentaire, pk=pk)
    
    if request.user in commentaire.likes.all():
        commentaire.likes.remove(request.user)
        aime = False
    else:
        commentaire.likes.add(request.user)
        aime = True
        # Créer une notification
        if commentaire.auteur != request.user:
            Notification.objects.create(
                destinataire=commentaire.auteur,
                expediteur=request.user,
                article=commentaire.article,
                message=f"a aimé votre commentaire."
            )
        
    return JsonResponse({'aime': aime, 'total_likes': commentaire.likes.count()})

# --- NOUVELLE VUE POUR LES NOTIFICATIONS ---
@login_required
def liste_notifications(request):
    notifications = request.user.notifications.all()
    # Marquer toutes les notifications comme lues
    notifications.update(lu=True)
    return render(request, 'blog/notifications.html', {'notifications': notifications})