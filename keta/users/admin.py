from django.contrib import admin

from .models import Jusuarios, Jpersonas

admin.site.register(Jusuarios)
admin.site.register(Jpersonas)
admin.site.site_header = "Keta Admistration"
admin.site.site_title = "Keta Admistration"
admin.site.index_title = "Keta Admistration"
