from django.contrib.auth.models import User
from .models import Monitoramento, Item
import requests
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, QueryDict
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
import datetime
from chartit import DataPool, Chart

def combview():
	query  = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item group by data_pub")
	query1 = Item.objects.raw("select count(id) as id, quali from twitter_monitor_item group by quali")
	query2 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEU' group by data_pub")
    	query3 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEG' group by data_pub")
    	query4 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='POS' group by data_pub")

	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query2},
	        'terms': [ 
		 'data_pub',
		 {'Neutro':'id'}]},
	      { 
				
		'options': {
		'source': query3},
		'terms': [
		 {'data_pub2':'data_pub'},
		 {'Negativo':'id'}]},
	      {

		'options': {
		'source': query4},
		'terms': [
		 {'data_pub3':'data_pub'},
		 {'Positivo':'id'}]},
	       {

		'options': {
		'source': query},
		'terms': [
		 {'data_pub4':'data_pub'},
		 {'Mensagens':'id'}]},
	       {

		'options': {
		'source': query1},
		'terms': [
		'quali',
		 {'Total':'id'}]}
	     ])

	cht3 = Chart(datasource=info,series_options=[{'options':{'type':'column'}, 'terms':{'data_pub': ['Neutro'], 'data_pub2':['Negativo'],'data_pub3':['Positivo']}},{'options':{'type':'line','color':'rgba(55, 227, 43, 0.6)'}, 'terms':{'data_pub4': ['Mensagens']}},{'options':{'type': 'pie', 'colors':['rgba(170, 0, 255, 0.56)','rgba(145, 75, 180, 0.56)','rgba(212, 0, 255, 0.6)']}, 'terms':{'quali': ['Total']}}], chart_options={'animation':{'duration':3000},'colors': ['rgba(15, 51, 255, 0.6)','rgba(112, 134, 255, 0.6)','rgba(112, 226, 255, 0.6)'],'title': { 'text': 'Total - Total por dia, com sentimento'}, 'tooltip': { 'pointFormat': '{series.name}: <b>{point.y}</b>'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}},'plotOptions':{'line':{'dataLabels':{'enabled': False}}},'plotOptions':{'column':{'dataLabels':{'enabled': False}}},'plotOptions':{'pie':{'center':[100,80],'size':100,'allowPointSelect': True, 'cursor':'pointer', 'dataLabels':{'enabled': True, 'format': '<b>{point.name}</b>: {point.percentage:.1f}%'}}}})
	return cht3

def combview_mensal(monit_id):
	monit_id = monit_id
	query  = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
	query1 = Item.objects.raw("select count(id) as id, quali from twitter_monitor_item where data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by quali",[monit_id])
	query2 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEU' AND data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
    	query3 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEG' AND data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
    	query4 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='POS'AND data_pub >= current_date - integer '30' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])

	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query2},
	        'terms': [ 
		 'data_pub',
		 {'Neutro':'id'}]},
	      { 
				
		'options': {
		'source': query3},
		'terms': [
		 {'data_pub2':'data_pub'},
		 {'Negativo':'id'}]},
	      {

		'options': {
		'source': query4},
		'terms': [
		 {'data_pub3':'data_pub'},
		 {'Positivo':'id'}]},
	       {

		'options': {
		'source': query},
		'terms': [
		 {'data_pub4':'data_pub'},
		 {'Mensagens':'id'}]},
	       {

		'options': {
		'source': query1},
		'terms': [
		'quali',
		 {'Total':'id'}]}
	     ])

	cht4 = Chart(datasource=info,series_options=[{'options':{'type':'column', 'borderWidth': 1,
            'borderColor': 'rgba(255, 255, 46, 0.6)','borderRadius': 5, 'shadow': True}, 'terms':{'data_pub': ['Neutro'], 'data_pub2':['Negativo'],'data_pub3':['Positivo']}},{'options':{'type':'line', 'shadow': True,'color':'rgba(55, 227, 43, 0.6)'}, 'terms':{'data_pub4': ['Mensagens']}},{'options':{'type': 'pie', 'colors':['rgba(170, 0, 255, 0.56)','rgba(145, 75, 180, 0.56)','rgba(212, 0, 255, 0.6)']}, 'terms':{'quali': ['Total']}}], chart_options={'animation':{'duration':3000},'colors': ['rgba(15, 51, 255, 0.6)','rgba(112, 134, 255, 0.6)','rgba(112, 226, 255, 0.6)'],'title': { 'text': 'Mensal - Total por dia, com sentimento'}, 'tooltip': { 'pointFormat': '{series.name}: <b>{point.y}</b>'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}},'plotOptions':{'line':{'dataLabels':{'enabled': False}}},'plotOptions':{'column':{'dataLabels':{'enabled': False}}},'plotOptions':{'pie':{'center':[100,50],'size':70,'allowPointSelect': True, 'cursor':'pointer', 'dataLabels':{'enabled': True, 'distance': 10, 'connectorPadding': 0, 'connectorWidth': 1, 'format': '<b>{point.name}</b>: {point.percentage:.1f}%'}}}})
	return cht4

def combview_semanal(monit_id):
	monit_id = monit_id
	query  = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
	query1 = Item.objects.raw("select count(id) as id, quali from twitter_monitor_item where data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by quali",[monit_id])
	query2 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEU' AND data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
    	query3 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEG' AND data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])
    	query4 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='POS'AND data_pub >= current_date - integer '7' and data_pub <= current_date and monit_id = %s group by data_pub",[monit_id])

	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query2},
	        'terms': [ 
		 'data_pub',
		 {'Neutro':'id'}]},
	      { 
				
		'options': {
		'source': query3},
		'terms': [
		 {'data_pub2':'data_pub'},
		 {'Negativo':'id'}]},
	      {

		'options': {
		'source': query4},
		'terms': [
		 {'data_pub3':'data_pub'},
		 {'Positivo':'id'}]},
	       {

		'options': {
		'source': query},
		'terms': [
		 {'data_pub4':'data_pub'},
		 {'Mensagens':'id'}]},
	       {

		'options': {
		'source': query1},
		'terms': [
		'quali',
		 {'Total':'id'}]}
	     ])

	cht6 = Chart(datasource=info,series_options=[{'options':{'type':'column', 'borderWidth': 1,
            'borderColor': 'rgba(255, 255, 46, 0.6)','borderRadius': 5, 'shadow': True}, 'terms':{'data_pub': ['Neutro'], 'data_pub2':['Negativo'],'data_pub3':['Positivo']}},{'options':{'type':'line', 'shadow': True,'color':'rgba(55, 227, 43, 0.6)'}, 'terms':{'data_pub4': ['Mensagens']}},{'options':{'type': 'pie', 'colors':['rgba(170, 0, 255, 0.56)','rgba(145, 75, 180, 0.56)','rgba(212, 0, 255, 0.6)']}, 'terms':{'quali': ['Total']}}], chart_options={'animation':{'duration':3000},'colors': ['rgba(15, 51, 255, 0.6)','rgba(112, 134, 255, 0.6)','rgba(112, 226, 255, 0.6)'],'title': { 'text': 'Semanal - Total por dia, com sentimento'}, 'tooltip': { 'pointFormat': '{series.name}: <b>{point.y}</b>'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}},'plotOptions':{'line':{'dataLabels':{'enabled': False}}},'plotOptions':{'column':{'dataLabels':{'enabled': False}}},'plotOptions':{'pie':{'center':[100,50],'size':70,'allowPointSelect': True, 'cursor':'pointer', 'dataLabels':{'enabled': True, 'distance': 10, 'connectorPadding': 0, 'connectorWidth': 1, 'format': '<b>{point.name}</b>: {point.percentage:.1f}%'}}}})
	return cht6

def combview_total(monit_id):
	monit_id = monit_id
	query  = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where monit_id = %s group by data_pub",[monit_id])
	query1 = Item.objects.raw("select count(id) as id, quali from twitter_monitor_item where monit_id = %s group by quali",[monit_id])
	query2 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEU' AND monit_id = %s group by data_pub",[monit_id])
    	query3 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEG' AND monit_id = %s group by data_pub",[monit_id])
    	query4 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='POS'AND monit_id = %s group by data_pub",[monit_id])

	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query2},
	        'terms': [ 
		 'data_pub',
		 {'Neutro':'id'}]},
	      { 
				
		'options': {
		'source': query3},
		'terms': [
		 {'data_pub2':'data_pub'},
		 {'Negativo':'id'}]},
	      {

		'options': {
		'source': query4},
		'terms': [
		 {'data_pub3':'data_pub'},
		 {'Positivo':'id'}]},
	       {

		'options': {
		'source': query},
		'terms': [
		 {'data_pub4':'data_pub'},
		 {'Mensagens':'id'}]},
	       {

		'options': {
		'source': query1},
		'terms': [
		'quali',
		 {'Total':'id'}]}
	     ])

	cht7 = Chart(datasource=info,series_options=[{'options':{'type':'column', 'borderWidth': 1,
            'borderColor': 'rgba(255, 255, 46, 0.6)','borderRadius': 5, 'shadow': True}, 'terms':{'data_pub': ['Neutro'], 'data_pub2':['Negativo'],'data_pub3':['Positivo']}},{'options':{'type':'line', 'shadow': True,'color':'rgba(55, 227, 43, 0.6)'}, 'terms':{'data_pub4': ['Mensagens']}},{'options':{'type': 'pie', 'colors':['rgba(170, 0, 255, 0.56)','rgba(145, 75, 180, 0.56)','rgba(212, 0, 255, 0.6)']}, 'terms':{'quali': ['Total']}}], chart_options={'animation':{'duration':3000},'colors': ['rgba(15, 51, 255, 0.6)','rgba(112, 134, 255, 0.6)','rgba(112, 226, 255, 0.6)'],'title': { 'text': 'Total - Total por dia, com sentimento'}, 'tooltip': { 'pointFormat': '{series.name}: <b>{point.y}</b>'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}},'plotOptions':{'line':{'dataLabels':{'enabled': False}}},'plotOptions':{'column':{'dataLabels':{'enabled': False}}},'plotOptions':{'pie':{'center':[100,50],'size':70,'allowPointSelect': True, 'cursor':'pointer', 'dataLabels':{'enabled': True, 'distance': 10, 'connectorPadding': 0, 'connectorWidth': 1, 'format': '<b>{point.name}</b>: {point.percentage:.1f}%'}}}})
	return cht7

def lineview():

    	query1 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item group by data_pub")
        info =\
	DataPool(
	    series=
	     [{'options': {
		'source': query1},
	       'terms': [ 
		 'data_pub',
		 {'Mensagens':'id',}]}
	     ])

    	cht = Chart(datasource=info, series_options=[{'options':{'type': 'line', 'stacking': False}, 'terms':{'data_pub': ['Mensagens']}}], chart_options={'title': { 'text': 'Total por dia'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}}})
	return cht
  
def columnview():
    
	query2 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEU' group by data_pub")
    	query3 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='NEG' group by data_pub")
    	query4 = Item.objects.raw("select count(id) as id, data_pub from twitter_monitor_item where quali='POS' group by data_pub")
	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query2},
	        'terms': [ 
		 'data_pub',
		 {'Neutro':'id'}]},
	      { 
				
		'options': {
		'source': query3},
		'terms': [
		 {'data_pub2':'data_pub'},
		 {'Negativo':'id'}]},
	      {

		'options': {
		'source': query4},
		'terms': [
		 {'data_pub3':'data_pub'},
		 {'Positivo':'id'}]},
	     ])

    	cht1 = Chart(datasource=info, series_options=[{'options':{'type': 'column', 'stacking': False}, 'terms':{'data_pub': ['Neutro'], 'data_pub2':['Negativo'], 'data_pub3':['Positivo']}}], chart_options={'animation':{'duration':3000}, 'colors':['rgba(213, 10, 7, 0.71)','rgba(16, 203, 194, 0.71)','rgba(150, 203, 16, 0.71)'],'title': { 'text': 'Total por dia, com sentimento'}, 'xAxis':{'title':{'text':'Dia'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Mensagens'}}})
	return cht1

def pieview():	
    	query1 = Item.objects.raw("select count(id) as id, quali from twitter_monitor_item group by quali")

    	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query1},
	        'terms': [ 
		 'quali',
		 'id']}
	     ])

    	cht2 = Chart(datasource=info, series_options=[{'options':{'type': 'pie', 'stacking': False, 'plotBackgroundColor': 'null', 'plotBorderWidth': 'null', 'plotShadow': False}, 'terms':{'quali': ['id']}}], chart_options={'animation':{'duration':3000}, 'colors':['rgba(213, 10, 7, 0.71)','rgba(16, 203, 194, 0.71)','rgba(150, 203, 16, 0.71)'],'title': { 'text': 'Total por dia, com sentimento'}, 'tooltip': { 'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'}, 'plotOptions':{'pie':{'allowPointSelect': True, 'cursor':'pointer', 'dataLabels':{'enabled': True, 'format': '<b>{point.name}</b>: {point.percentage:.1f}%', 'style': {'color': '(Highcharts.theme && Highcharts.theme.contrastTextColor)'}}}}})
    	return cht2

def barview(usuario_id):

	usuario_id = usuario_id
        query = Item.objects.raw('SELECT count(li.id) as id, lm.palavra as monitoramento FROM twitter_monitor_item li INNER JOIN twitter_monitor_monitoramento lm ON li.monit_id = lm.id WHERE lm.usuario_id= %s GROUP BY lm.id', [usuario_id])	
	info =\
	DataPool(
	    series=
	     [{ 
		
		'options': {		
		'source': query},
	        'terms': [ 		
		{'Total':'id'},
		{'Palavra': 'monitoramento'}]}
	     ])

    	cht5 = Chart(datasource=info, series_options=[{'options':{'type': 'bar', 'maxPointWidth': 25, 'stacking': False}, 'terms':{'Palavra': ['Total']}}], chart_options={'animation':{'duration':3000}, 'colors':['#ff8e24'],'title': { 'text': 'Total por monitoramento'}, 'xAxis':{'title':{'text':'Palavra'}}, 'yAxis':{'allowDecimals': False, 'title':{'text':'Total'}}})
	return cht5
    
