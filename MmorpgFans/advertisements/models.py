from django.db import models
from django.contrib.auth.models import User

from bs4 import BeautifulSoup

# Create your models here.


class Advert(models.Model):
    # Объявления состоят из заголовка и текста, внутри которого могут быть картинки, встроенные видео и другой контент.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTimeCreate=models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    text = models.TextField()

    tanks='TN'
    hills='HL'
    dd='DD'
    trader='TR'
    gildmaster='GM'
    questgiver='QG'
    farrier='FR'
    skinner='SK'
    potion='PT'
    spell_masters='SM'

    CATEGORY=[
        (tanks, 'Танки'),
        (hills,'Хилы'),
        (dd,'ДД'),
        (trader,'Торговцы'),
        (gildmaster,'Гилдмастеры'),
        (questgiver,'Квестгиверы'),
        (farrier,'Кузнецы'),
        (skinner,'Кожевники'),
        (potion,'Зельевары'),
        (spell_masters,'Мастера заклинаний'),
    ]
    category=models.CharField(max_length=2, choices=CATEGORY, default=trader)

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с объявлением
        return f'/advertisements/{self.id}'
    
    def preview(self):
        soup = BeautifulSoup (self.text, 'html.parser')
        for img in soup.findAll("img"):
            # a=img.extract()
            a=img.decompose()
        return soup.get_text()[0:123] + '...'
    
    def removeTag(text, tagname):
        soup = BeautifulSoup (text, 'html.parser')
        for tag in soup.findAll(tagname):
            tag.extract()

    def is_author(self, user):
        return self.author==user



class Respond(models.Model):
    text = models.TextField()
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    accept = models.BooleanField(default = False)
    dateTimeCreate=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с 
        # return f'/advertisements/{self.advert.id}/add_respond'
        return f'/advertisements/{self.advert.id}'
    
    def accept_on(self):
        self.accept = True
        self.save(update_fields=['accept'])
