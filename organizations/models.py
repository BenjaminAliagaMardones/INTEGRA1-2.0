from django.db import models
from django.contrib.auth.models import User


# Sectores disponibles para empresas y cooperativas
SECTOR_CHOICES = [
    ('tecnologia', 'Tecnología'),
    ('agricultura', 'Agricultura'),
    ('manufactura', 'Manufactura'),
    ('servicios', 'Servicios'),
    ('comercio', 'Comercio'),
    ('construccion', 'Construcción'),
    ('educacion', 'Educación'),
    ('salud', 'Salud'),
    ('transporte', 'Transporte'),
    ('turismo', 'Turismo'),
]


class Company(models.Model):
    """Modelo de Empresa/PYME"""
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, verbose_name='Sector')
    description = models.TextField(verbose_name='Descripción')
    access_code = models.CharField(max_length=20, default='123456', verbose_name='Código de Acceso', help_text='Código para que otros usuarios se unan a tu empresa')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='companies_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-created_at']

    @property
    def members_count(self):
        return self.members.count()


class Cooperative(models.Model):
    """Modelo de Cooperativa (agrupa empresas del mismo sector)"""
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, verbose_name='Sector')
    description = models.TextField(verbose_name='Descripción')
    companies = models.ManyToManyField(Company, related_name='cooperatives', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cooperatives_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cooperativa'
        verbose_name_plural = 'Cooperativas'
        ordering = ['-created_at']

    @property
    def companies_count(self):
        return self.companies.count()

    def can_join(self, company):
        """Verificar si una empresa puede unirse (mismo sector)"""
        return company.sector == self.sector

