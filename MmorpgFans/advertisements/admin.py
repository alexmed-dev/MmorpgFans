from django.contrib import admin

# Register your models here.
from django.shortcuts import render

from .models import *

from django_summernote.admin import SummernoteModelAdmin


# создаём новый класс для представления товаров в админке
class AdvertAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'author', 'category', 'dateTimeCreate', 'text')
    list_filter = ('author', 'category') # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'category') # тут всё очень похоже на фильтры из запросов в базу, давайте 
    summernote_fields = ('text',)


class RespondAdmin(admin.ModelAdmin):
    list_display = ('advert', 'text', 'accept', 'get_advertTitle', 'author')
    list_filter = ('advert',) # добавляем примитивные фильтры в нашу админку
    search_fields = ('text',) # тут всё очень похоже на фильтры из запросов в базу, давайте

    def get_advertTitle(self, obj):
        return obj.advert.title
    get_advertTitle.admin_order_field  = 'advert'  #Allows column order sorting
    get_advertTitle.short_description = 'Advert title'  #Renames column head
    


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Respond, RespondAdmin)
