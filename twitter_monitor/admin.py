from django.contrib import admin

from .models import Monitoramento,Item

# Register your models here.

admin.site.site_header = 'MoniTwi Admin'
admin.site.site_title = 'MoniTwi'
admin.site.index_title = 'Administration'


admin.site.register(Monitoramento)
admin.site.register(Item)
