from django.contrib import admin
from .models import Categorie, Tag, Article, Commentaire


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'statut', 'date_creation')
    list_filter = ('statut', 'categorie', 'tags', 'date_creation')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'date_creation'


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'date_creation', 'approuve')
    list_filter = ('approuve', 'date_creation')
    search_fields = ('contenu', 'auteur__username')
    actions = ['approuver_commentaires']

    @admin.action(description="Approuver les commentaires sélectionnés")
    def approuver_commentaires(self, request, queryset):
        queryset.update(approuve=True)