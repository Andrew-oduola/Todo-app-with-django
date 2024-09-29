
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from .forms import LoginForm, AddTaskForm

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input) # the startwith method can also be used to get the words starting with that filters

        context['search_input'] = search_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    form = AddTaskForm
    

    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'core/register.html'
    form_class = UserCreationForm
    # redirect_authenticated_user=True   # didn't work so a function was used instead, Function get()
    success_url = reverse_lazy('tasks')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        
        return super(RegisterPage, self).get(*args, **kwargs)
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('tasks')

