from rest_framework import serializers
from twitter_monitor.models import Monitoramento, Item

class MonitoramentoSerializer(serializers.ModelSerializer):
    class Meta:
	model = Monitoramento
	fields = ('id', 'palavra', 'usuario')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
	model = Item
	fields = ('id', 'monit', 'quali', 'data_pub', 'texto', 'nome_twi', 'tag')
