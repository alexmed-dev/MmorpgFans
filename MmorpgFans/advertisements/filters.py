from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Respond
 
 
# создаём фильтр
class RespondFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация
    class Meta:
        model = Respond
        
        fields = {
            'author': ['exact'],
            'advert': ['exact'],
            'text': ['icontains'],
        }


        