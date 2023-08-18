from django.contrib import admin

from .models import Jusuarios, Jpersonas

admin.site.register(Jusuarios)
admin.site.register(Jpersonas)
admin.site.site_header = "Jakaysa Admistration"
admin.site.site_title = "Jakaysa Admistration"
admin.site.index_title = "Jakaysa Admistration"
