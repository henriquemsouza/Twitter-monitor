from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from datetime import date

class Monitoramento(models.Model):

    palavra = models.CharField(max_length=60)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
    	
    	return self.palavra

    def get_absolute_url(self):
    	
    	return reverse('monitoramento_detail', args=[str(self.id)])

class Item(models.Model):

    monit = models.ForeignKey('Monitoramento')

    quali = models.CharField(max_length=3, default='sem')
    data_pub = models.DateField(null=True, blank=True)
    texto = models.TextField(max_length=200, null=True, blank=True)
    nome_twi = models.CharField(max_length=100)
    tag = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):

    	return self.monitoramento.palavra



    
    
    
