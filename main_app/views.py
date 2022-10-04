#from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Song
# after our other imports 
from django.views.generic import DetailView

class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

class FinchList(TemplateView):
    template_name = "finch_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mySearchName = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if mySearchName != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["finch"] = Finch.objects.filter(name__icontains=mySearchName)
            context["stuff_at_top"] = f"Searching through Finches list for {mySearchName}"
        else:
            context["finch"] = Finch.objects.all()
            context["stuff_at_top"] = "Cool Birds"
        return context

class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'img', 'bio']
    template_name = "finch_create.html"
    success_url = "/finch/"

class FinchDetail(DetailView):
    model = Finch
    template_name = "finch_detail.html"

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['name', 'img', 'bio', 'verified_finch']
    template_name = "finch_update.html"
    success_url = "/finch/"

    def get_success_url(self):
        return reverse('finch_detail', kwargs={'pk': self.object.pk})

class FinchDelete(DeleteView):
    model = Finch
    template_name = "finch_delete_confirmation.html"
    success_url = "/finch/"
    
class SongCreate(View):

    def post(self, request, pk):
        formTitle = request.POST.get("title")
        minutes = request.POST.get("minutes")
        seconds = request.POST.get("seconds")
        formLength = 60 * int(minutes) + int(seconds)
        theFinch = Finch.objects.get(pk=pk)
        Song.objects.create(title=formTitle, length=formLength, finch=theFinch)
        return redirect('finch_detail', pk=pk)
    
