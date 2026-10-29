from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connecte l'utilisateur automatiquement après inscription
            return redirect('blog:liste_articles')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/inscription.html', {'form': form})