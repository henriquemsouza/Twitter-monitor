from django.contrib.auth.models import User
from .models import Monitoramento, Item
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, Http404
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger
from auth_mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from chartit import DataPool, Chart
from got import *
from .graficos import combview_total, combview_mensal, combview_semanal, barview

def index(request):
	return render( request,'index.html')

class MonitoramentoListView(LoginRequiredMixin, generic.ListView):
    model = Monitoramento
    template_name = 'twitter_monitor/monitoramento_list.html'
    paginate_by = 7
    bar = None

    def get_context_data(self, **kwargs):
	usuario_id = self.request.user.pk
	bar = barview(usuario_id)
	context = super(MonitoramentoListView, self).get_context_data(**kwargs)
	context['chart_list'] = bar
	filtro = '0'
	return context

    def get_queryset(self):
	return Monitoramento.objects.filter(usuario=self.request.user).order_by('id')

from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def GraficoView(request, pk):
    filtro = request.POST.get('acao')
    monit_id = int(pk)
    usuario = None
    usuario_cod = None
    monitoramento_atual = None
    atuais_id = []
    if request.user.is_authenticated():
	usuario_cod = request.user.pk
	usuario = request.user.username	
	monitoramento_atual = Monitoramento.objects.filter(usuario=usuario_cod)
	monitoramento_atual = monitoramento_atual.values()
	for monitor in monitoramento_atual: 	    
	    atuais_id.append(monitor.get('id'))
	if(monit_id not in atuais_id):
	    return HttpResponseRedirect(reverse('monitoramento:monitoramentos'))
    monitoramento_atual = Monitoramento.objects.get(id=monit_id)	  
    if(filtro == "por_mes"):
    	cb = combview_mensal(monit_id) 
    elif(filtro == "por_sem"):
	cb = combview_semanal(monit_id)  	
    else:
	cb = combview_total(monit_id)
    return render_to_response('twitter_monitor/GraficoView.html', {'chart_list': cb, 'monit_id': pk, 'usuario':usuario, 'atual': monitoramento_atual})


@login_required
@csrf_exempt
def MonitoramentoDetailView(request, pk, filtro):
    monit_id = int(pk)
    query = filtro
    usuario = None
    usuario_cod = None
    monitoramento_atual = None
    atuais_id = []
    if request.user.is_authenticated():
	usuario_cod = request.user.pk
	usuario = request.user.username	
	monitoramento_atual = Monitoramento.objects.filter(usuario=usuario_cod)
	monitoramento_atual = monitoramento_atual.values()
	for monitor in monitoramento_atual: 	    
	    atuais_id.append(monitor.get('id'))
	if(monit_id not in atuais_id):
	    return HttpResponseRedirect(reverse('monitoramento:monitoramentos'))

    nome_monitor = Monitoramento.objects.get(id=monit_id)

    if (query == '1'):
        item_list = list(Item.objects.raw("select * from twitter_monitor_item where data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub, id",[monit_id]))
    elif (query == '2'):
	item_list = list(Item.objects.raw("select * from twitter_monitor_item where data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub, id",[monit_id]))
    else:
	item_list = list(Item.objects.filter(monit_id=monit_id))
    
    monitoramento = len(item_list)
    paginator = Paginator(item_list, 7)
    page = request.GET.get('page')

    try:
	itens = paginator.page(page)
    except PageNotAnInteger:
	itens = paginator.page(1)

    return render_to_response('twitter_monitor/monitoramento_detail.html', {'pk': monit_id, 'atual': nome_monitor, 'usuario': usuario, 'object_list': itens, 'monitoramento': monitoramento})

@csrf_exempt
def aplicar(request, pk):
    
    cod_obj = request.POST.getlist('choice')
    cod_acao = request.POST.get('acao')  
    tag = request.POST.get('tag')
    sentimento = ["NEG", "POS", "NEU"]
    filtros = ["total", "por_sem", "por_mes"]
    objeto1 = get_object_or_404(Monitoramento, pk=pk)
    objeto = None
    if(cod_acao in filtros):
    	if (cod_acao == "por_sem"):
    	    return HttpResponseRedirect(reverse('monitoramento:monitoramento_detail', args=(objeto1.id, 2)))
    	elif (cod_acao == "por_mes"):
	    return HttpResponseRedirect(reverse('monitoramento:monitoramento_detail', args=(objeto1.id, 1)))
    	else:
    	    return HttpResponseRedirect(reverse('monitoramento:monitoramento_detail', args=(objeto1.id, 0)))
    if(tag is not 'null'):
	for item in cod_obj:
	    objeto = get_object_or_404(Item, pk=item)
	    objeto.tag = tag
	    objeto.save()
  
    if(cod_acao == "deletar"):
	for item in cod_obj:
	    objeto = get_object_or_404(Item, pk=item)
    	    objeto.delete()

    elif(cod_acao in sentimento):
    	for item in cod_obj:
	    objeto = get_object_or_404(Item, pk=item)
	    objeto.quali = cod_acao
	    objeto.save()

    return HttpResponseRedirect(reverse('monitoramento:monitoramento_detail', args=(objeto.monit_id, 0)))

@csrf_exempt
def coletar(request):
    pk = request.POST.get('palavra')
    objeto = get_object_or_404(Monitoramento, pk=pk)
    palavra = objeto.palavra
    dataini = date.today() - timedelta(7)
    for dias in range(7):
    	dataFrom = dataini - timedelta(dias + 1)
	dataTo = dataFrom + timedelta(1)
    	tweetCriteria = manager.TweetCriteria().setQuerySearch(palavra).setSince(str(dataFrom)).setUntil(str(dataTo)).setMaxTweets(20)
    	tweet = manager.TweetManager.getTweets(tweetCriteria)
    	for msg in tweet:
	    i = Item()
	    i.texto = msg.text
	    i.data_pub = msg.date
	    i.nome_twi = msg.username
	    i.monit_id = objeto.pk
	    i.save()
    return HttpResponseRedirect(reverse('monitoramento:monitoramentos'))


      	
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class MonitoramentoCreate(LoginRequiredMixin, CreateView):
    model = Monitoramento
    fields = ['palavra']
    success_url = reverse_lazy('monitoramento:monitoramentos')

    def form_valid(self, form):
	object = form.save(commit=False)
	object.usuario = self.request.user
	object.save()
	return super(MonitoramentoCreate, self).form_valid(form)

def cadastro(request):
    if request.method == 'POST':
	form = UserCreationForm(request.POST)
	if form.is_valid():
	    form.save()
	    username = form.cleaned_data.get('username')
	    raw_password = form.cleaned_data.get('password1')
	    user = authenticate(username=username, password=raw_password)
	    login(request, user)
	    return redirect('monitoramento:monitoramentos')
    else:
	form = UserCreationForm()
    return render(request, 'twitter_monitor/cadastro_form.html', {'form': form})
	
class MonitoramentoUpdate(UpdateView):
    model = Monitoramento
    fields = ['palavra']

class MonitoramentoDelete(DeleteView):
    model = Monitoramento
    success_url = reverse_lazy('monitoramento:monitoramentos')


from serializers import MonitoramentoSerializer, ItemSerializer
from django.db.models import Q
from rest_framework import generics

class MonitoramentoList(generics.ListCreateAPIView):
    lookup_url_kwarg = 'usuario'  
    serializer_class = MonitoramentoSerializer

    def get_queryset(self):
	usuario = self.kwargs.get(self.lookup_url_kwarg)
	monits = Monitoramento.objects.filter(usuario=usuario)
	return monits
	
class ItemList(generics.ListCreateAPIView):
    lookup_url_kwarg = ('usuario', 'monit')
    serializer_class = ItemSerializer

    def get_queryset(self):
	usuario = self.kwargs.get(self.lookup_url_kwarg[0])
	monit = self.kwargs.get(self.lookup_url_kwarg[1])
	itens = Item.objects.filter(monit=monit)
	return itens

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = ('id')
    serializer_class = ItemSerializer

    def get_queryset(self):
	id = self.kwargs.get(self.lookup_url_kwarg)
	item = Item.objects.filter(id=id)	
	return item

class ItemListMensal(generics.ListAPIView):
    lookup_url_kwarg = ('usuario', 'monit')
    serializer_class = ItemSerializer

    def get_queryset(self):
	usuario = self.kwargs.get(self.lookup_url_kwarg[0])
	monit = self.kwargs.get(self.lookup_url_kwarg[1])
	itens = list(Item.objects.raw("select * from twitter_monitor_item where data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub, id",[monit]))
	return itens

class ItemListSemanal(generics.ListAPIView):
    lookup_url_kwarg = ('usuario', 'monit')
    serializer_class = ItemSerializer

    def get_queryset(self):
	usuario = self.kwargs.get(self.lookup_url_kwarg[0])
	monit = self.kwargs.get(self.lookup_url_kwarg[1])
	itens = list(Item.objects.raw("select * from twitter_monitor_item where data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub, id",[monit]))
	return itens
