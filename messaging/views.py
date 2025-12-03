from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Max
from django.http import HttpResponseForbidden
from .models import Chat, Message
from .forms import MessageForm
from organizations.models import Company, Cooperative


@login_required
def chat_list(request):
    """Lista todos los chats del usuario"""
    # Obtener chats donde el usuario tiene acceso dinámico
    user_company = getattr(request.user.profile, 'company', None)
    
    # 1. Chats directos (donde es participante)
    direct_chats = Q(type='direct', participants=request.user)
    
    # 2. Chats de su empresa
    company_chats = Q(type='company', company=user_company) if user_company else Q(pk__in=[])
    
    # 3. Chats de cooperativas donde su empresa es miembro
    cooperative_chats = Q(type='cooperative', cooperative__companies=user_company) if user_company else Q(pk__in=[])
    
    chats = Chat.objects.filter(
        direct_chats | company_chats | cooperative_chats
    ).distinct().annotate(
        last_message_time=Max('messages__created_at')
    ).order_by('-last_message_time')
    
    context = {
        'chats': chats
    }
    return render(request, 'messaging/chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    """Muestra un chat específico y permite enviar mensajes"""
    chat = get_object_or_404(Chat, id=chat_id)
    
    # Verificar que el usuario tenga acceso a este chat
    if not chat.user_can_access(request.user):
        messages.error(request, 'No tienes acceso a este chat.')
        return redirect('messaging:chat_list')
    
    # Obtener todos los mensajes del chat
    chat_messages = chat.messages.all().order_by('created_at')
    
    # Procesar formulario de envío de mensaje
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            messages.success(request, 'Mensaje enviado.')
            return redirect('messaging:chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()
    
    context = {
        'chat': chat,
        'chat_messages': chat_messages,
        'form': form
    }
    return render(request, 'messaging/chat_detail.html', context)


@login_required
def chat_messages(request, chat_id):
    """Vista parcial para obtener mensajes (HTMX polling)"""
    chat = get_object_or_404(Chat, id=chat_id)
    
    if not chat.user_can_access(request.user):
        return HttpResponseForbidden()
    
    chat_messages = chat.messages.all().order_by('created_at')
    return render(request, 'messaging/partials/message_list.html', {'chat_messages': chat_messages, 'user': request.user})


@login_required
def create_direct_chat(request, user_id):
    """Crea o abre un chat directo con otro usuario"""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, 'No puedes chatear contigo mismo.')
        return redirect('dashboard')
    
    # Buscar si ya existe un chat directo entre estos usuarios
    existing_chat = Chat.objects.filter(
        type='direct',
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_chat:
        return redirect('messaging:chat_detail', chat_id=existing_chat.id)
    
    # Crear nuevo chat directo
    chat = Chat.objects.create(
        type='direct'
    )
    chat.participants.add(request.user, other_user)
    
    messages.success(request, f'Chat con {other_user.username} creado.')
    return redirect('messaging:chat_detail', chat_id=chat.id)


@login_required
def create_company_chat(request, company_id):
    """Crea o abre el chat de una empresa"""
    company = get_object_or_404(Company, id=company_id)
    
    # Verificar que el usuario sea miembro de la empresa
    # company.members son Profiles, verificamos si el perfil del usuario tiene esta empresa
    if not hasattr(request.user, 'profile') or request.user.profile.company != company:
        messages.error(request, 'Debes ser miembro de la empresa para acceder a su chat.')
        return redirect('organizations:company_detail', pk=company_id)
    
    # Buscar si ya existe un chat para esta empresa
    existing_chat = Chat.objects.filter(
        type='company',
        company=company
    ).first()
    
    if existing_chat:
        return redirect('messaging:chat_detail', chat_id=existing_chat.id)
    
    # Crear nuevo chat de empresa
    chat = Chat.objects.create(
        type='company',
        company=company
    )
    # Agregar todos los miembros de la empresa al chat
    # company.members son Profiles, necesitamos obtener los Users
    users = User.objects.filter(profile__company=company)
    chat.participants.set(users)
    
    messages.success(request, f'Chat de {company.name} creado.')
    return redirect('messaging:chat_detail', chat_id=chat.id)


@login_required
def create_cooperative_chat(request, cooperative_id):
    """Crea o abre el chat de una cooperativa"""
    cooperative = get_object_or_404(Cooperative, id=cooperative_id)
    
    # Verificar que el usuario sea miembro de alguna empresa de la cooperativa
    # members son Profiles, verificamos si el perfil del usuario tiene empresa en la cooperativa
    user_company = None
    if hasattr(request.user, 'profile'):
        user_company = request.user.profile.company
    
    if not user_company or not cooperative.companies.filter(id=user_company.id).exists():
        messages.error(request, 'Debes ser miembro de una empresa asociada para acceder al chat.')
        return redirect('organizations:cooperative_detail', pk=cooperative_id)
    
    # Buscar si ya existe un chat para esta cooperativa
    existing_chat = Chat.objects.filter(
        type='cooperative',
        cooperative=cooperative
    ).first()
    
    if existing_chat:
        return redirect('messaging:chat_detail', chat_id=existing_chat.id)
    
    # Crear nuevo chat de cooperativa
    chat = Chat.objects.create(
        type='cooperative',
        cooperative=cooperative
    )
    # Agregar todos los miembros de las empresas de la cooperativa
    users = User.objects.filter(
        profile__company__in=cooperative.companies.all()
    ).distinct()
    chat.participants.set(users)
    
    messages.success(request, f'Chat de {cooperative.name} creado.')
    return redirect('messaging:chat_detail', chat_id=chat.id)
