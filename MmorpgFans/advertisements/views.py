from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import *
from .forms import AdvertForm, RespondForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .filters import RespondFilter
from django.http import HttpResponseForbidden



class AdvertList(ListView):
    model = Advert  # указываем модель, объекты которой мы будем выводить
    template_name = 'adverts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'adverts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Advert.objects.order_by('-id') # это если без формы поиска
    # ordering = ['-id'] # это если с формой поиска
    paginate_by = 3 # поставим постраничный вывод в 10 элементов


class AdvertCreate(LoginRequiredMixin,CreateView):
    template_name = 'advert_create.html'
    permission_required = ('advertisements.add_advert', )
    form_class = AdvertForm
    

    def get_initial(self):
        initial = super(AdvertCreate, self).get_initial()
        initial['author'] = self.request.user
        return initial


# AdvertDetail скорее всего не нужен, вместо него RespondCreate
# т.к., наверное, не будет такого юзкейса: просмотр объявления без откликов на него
# будет редактирование объявления - там без откликов, но это отдельный класс и шаблон
# для неавторизованных и для автора объявления - не будет выводиться форма добавления отклика
class RespondCreate(SuccessMessageMixin, CreateView):
    template_name='advert.html'
    model=Respond
    fields=['text', 'accept', 'advert']
    # messages.success(request, "Profile details updated.")
    success_message="Отклик будет добавлен после утверждения автором объявления."

    def get_context_data(self, **kwargs):
        context = super(RespondCreate, self).get_context_data(**kwargs)
        pk_advert=self.kwargs["pk_advert"]
        advert = Advert.objects.get(pk=pk_advert)
        context['advert'] = advert
        #  выводим отклики только к данному обявлению:
        context['responds'] = Respond.objects.filter(advert=advert, accept=True).order_by('-id')
        return context
    
    def get_initial(self):
        initial = super(RespondCreate, self).get_initial()
        pk_advert=self.kwargs["pk_advert"]
        initial['advert'] = Advert.objects.get(pk=pk_advert)
        return initial
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        pk_advert=self.kwargs["pk_advert"]
        form.instance.advert = Advert.objects.get(pk=pk_advert)
        # добавлям сообщения
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags='add_respond')
        return response
    

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
    

class ProfileView(ListView):
    model = Respond  # указываем модель, объекты которой мы будем выводить
    template_name = 'profile.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'responds'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id'] # это если с формой поиска
    #paginate_by = 2 #

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        user = self.request.user
        my_responds = Respond.objects.filter(advert__author=user).order_by('-id')
        # context['my_responds'] = my_responds # это временно, для сравнения
        context['filter'] = RespondFilter(self.request.GET, queryset=my_responds, request=self.request)
        return context


class AdvertUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'advert_edit.html'
    form_class = AdvertForm

    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        obj = Advert.objects.get(pk=id)
        if not obj.author==self.request.user:
            return HttpResponseForbidden('Объявление может редактировать только автор: '+obj.author.username)
        return super(AdvertUpdate, self).dispatch(request, *args, **kwargs)
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advert.objects.get(pk=id)
        # obj = Advert.objects.get(pk=id)
        # obj.owner=obj.author=self.request.user
        # return obj

    
    def can_edit(self, **kwargs):
        id = self.kwargs.get('pk')
        user=self.request.user=Advert.objects.get(pk=id)


class RespondDelete(LoginRequiredMixin, DeleteView):
    template_name = 'respond_delete.html'
    queryset = Respond.objects.all()
    success_url = '/advertisements/profile'


@login_required
def accept_respond(request, pk, advert):
    respond = Respond.objects.get(pk=pk)
    respond.accept_on()
    # print(request.GET['advert'])
    # return redirect(f'/advertisements/profile?advert={advert}') # так всегда будет вычисляться advert и перенавправление
    return redirect(f'/advertisements/profile')
