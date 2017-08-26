from django.conf.urls import url
from twitter_monitor import views

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^monitoramentos/$', views.MonitoramentoListView.as_view(), name='monitoramentos'),
    url(r'^monitoramento/(?P<pk>[0-9]+)/(?P<filtro>[0-9]+)/$', views.MonitoramentoDetailView, name='monitoramento_detail'),
    url(r'^monitoramento/create/$', views.MonitoramentoCreate.as_view(), name='monitoramento_create'),
    url(r'^monitoramento/(?P<pk>\d+)/update/$', views.MonitoramentoUpdate.as_view(), name='monitoramento_update'),
    url(r'^monitoramento/(?P<pk>\d+)/delete/$', views.MonitoramentoDelete.as_view(), name='monitoramento_delete'),
    url(r'^monitoramento/(?P<pk>\d+)/aplicar/$', views.aplicar, name='aplicar'),
    url(r'^monitoramento/coletar/$', views.coletar, name='coletar'),
    url(r'^monitoramento/(?P<pk>\d+)/GraficoView/$', views.GraficoView, name='Grafico'),
]

schema_view = get_schema_view(title='Pastebin API')

urlpatterns += [
    url(r'^monitoramentos/schema/$', schema_view, name='schema'),
    url(r'^monitoramentos/(?P<usuario>[0-9]+)/$', views.MonitoramentoList.as_view()),
    url(r'^monitoramentos/(?P<usuario>[0-9]+)/(?P<monit>[0-9]+)/$', views.ItemList.as_view()),
    url(r'^monitoramentos/item/(?P<id>[0-9]+)/$', views.ItemDetail.as_view()),
    url(r'^monitoramentos/item/mensal/(?P<usuario>[0-9]+)/(?P<monit>[0-9]+)/$', views.ItemListMensal.as_view()),
    url(r'^monitoramentos/item/semanal/(?P<usuario>[0-9]+)/(?P<monit>[0-9]+)/$', views.ItemListSemanal.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

