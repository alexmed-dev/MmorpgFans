from django.urls import path
from .views import * # импортируем наше представление
# from .views import upgrade_me
# from django.views.decorators.cache import cache_page

 
urlpatterns = [
    # path — означает путь
    path('', AdvertList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk_advert>', RespondCreate.as_view(), name = 'add_respond'),
    path('add', AdvertCreate.as_view()),
    path('<int:pk>/edit', AdvertUpdate.as_view()),
    path('<int:advert>/delete_respond/<int:pk>/', RespondDelete.as_view()),
    path('profile', ProfileView.as_view()),
    path('accept_respond/<int:pk>/advert/<int:advert>/', accept_respond, name = 'accept_respond'),
    path('<int:pk_advert>/add_respond', RespondCreate.as_view(), name = 'add_respond'),

]