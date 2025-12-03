from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from organizations.models import Company, Cooperative
from messaging.models import Chat


def register(request):
    """Vista de registro de usuario"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login después de registro
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido {user.username}')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """Vista del perfil de usuario"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado exitosamente!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard(request):
    """Dashboard principal después del login"""
    # Contar estadísticas
    companies_count = Company.objects.count()
    cooperatives_count = Cooperative.objects.count()
    user_chats_count = Chat.objects.filter(participants=request.user).count()
    
    context = {
        'user': request.user,
        'profile': request.user.profile,
        'companies_count': companies_count,
        'cooperatives_count': cooperatives_count,
        'user_chats_count': user_chats_count,
    }
    return render(request, 'dashboard.html', context)
