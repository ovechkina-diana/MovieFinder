from django.shortcuts import render, redirect
from  .models import  Films
from .forms import FilmsForm
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

def films_home(request):
    films = Films.objects.order_by('year')  #[:3]
    return render(request, 'films/films_home.html', {'films': films})

class FilmsDeatilView(DetailView):
    model = Films
    template_name = 'films/detail_view.html'
    context_object_name = 'film'

class FilmsUpdateView(UpdateView):
    model = Films
    template_name = 'films/create.html'

    form_class = FilmsForm

class FilmsDeleteView(DeleteView):
    model = Films
    success_url = '/films/'
    template_name = 'films/film-delete.html'



def create(request):
    error = ''
    if request.method == "POST":
        form = FilmsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Ошибка в заполенении формы"


    form = FilmsForm

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'films/create.html', data)
