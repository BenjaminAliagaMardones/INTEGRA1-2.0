from django.db import models
from django.contrib.auth.models import User
from organizations.models import Company, Cooperative


class Chat(models.Model):
    """Modelo de Chat (3 tipos: directo, empresa, cooperativa)"""
    TYPE_CHOICES = [
        ('direct', 'Directo'),
        ('company', 'Empresa'),
        ('cooperative', 'Cooperativa'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    participants = models.ManyToManyField(User, related_name='chats')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type == 'direct':
            return f"Chat: {', '.join([u.username for u in self.participants.all()[:2]])}"
        elif self.type == 'company':
            return f"Chat Empresa: {self.company.name}"
        else:
            return f"Chat Cooperativa: {self.cooperative.name}"

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-created_at']

    def user_can_access(self, user):
        """Verificar si un usuario puede acceder al chat"""
        if self.type == 'direct':
            return self.participants.filter(id=user.id).exists()
        elif self.type == 'company':
            # Acceso si el usuario pertenece a la empresa del chat
            return hasattr(user, 'profile') and user.profile.company == self.company
        elif self.type == 'cooperative':
            # Acceso si la empresa del usuario pertenece a la cooperativa del chat
            return (hasattr(user, 'profile') and 
                    user.profile.company and 
                    self.cooperative.companies.filter(id=user.profile.company.id).exists())
        return False


class Message(models.Model):
    """Modelo de Mensaje"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']

