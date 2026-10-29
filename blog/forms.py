from django import forms
from .models import Commentaire, Article, Profil

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary', 
                'rows': 3, 
                'placeholder': 'Écrivez votre commentaire ici...'
            }),
        }
        labels = {
            'contenu': ''
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'categorie', 'tags', 'statut', 'image_couverture']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 6}),
            'categorie': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'statut': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'image_couverture': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['statut'].initial = 'publie'

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary', 
                'rows': 3, 
                'placeholder': 'Parlez-nous de vous en quelques mots...'
            }),
        }