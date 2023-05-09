from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.user_app.models import Account


class Company(models.Model):
    '''Model definition for Company.'''
    name = models.CharField('Nombre', max_length=200)
    website = models.URLField('Sitio de Internet', max_length=250)
    active = models.BooleanField('activo', default=True)

    class Meta:
        '''Meta definition for Company.'''

        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return str(self.id) + " - "+ self.name

class Property(models.Model):
    '''Model definition for Property.'''
    address = models.CharField('Dirección', max_length=200)
    country = models.CharField('País', max_length=50)
    image = models.ImageField('Imagen', upload_to='media', blank=True, null=True)
    calification_avg = models.FloatField('Promedio de Calificaciones', default=0)
    calification_count = models.IntegerField('Cantidad de Calificaciones', default=0)
    calification_sum = models.PositiveIntegerField('Suma de Calificaciones', default=0)
    active = models.BooleanField('activo',default=True)
    description = models.TextField('Descripción')
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete= models.CASCADE, related_name="property_list")
    
    class Meta:
        '''Meta definition for Property.'''

        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'
        ordering = ('-id',)

    def __str__(self):
        return str(self.id)+" - "+self.address

class Comment (models.Model):
    '''Model definition para comentarios.'''
    comment_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    calification = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Comentario', max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    property = models.ForeignKey(Property, on_delete= models.CASCADE, related_name='comments_list')
    
    class Meta:
        '''Meta definition for Comment.'''

        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ('id',)

    def __str__(self):
        return str(self.id)+" - "+str(self.calification)+" -> "+self.property.address