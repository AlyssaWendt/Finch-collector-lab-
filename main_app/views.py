from django.views import View
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Song, Playlist
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





class Home(TemplateView):
    template_name = "home.html"
    # Here we have added the playlists as context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context


class About(TemplateView):
    template_name = "about.html"
    


@method_decorator(login_required, name='dispatch')
class FinchList(TemplateView):
    template_name = "finch_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["finch"] = Finch.objects.filter(
                name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for {name}"
        else:
            context["finch"] = Finch.objects.filter(user=self.request.user)
            context["header"] = "Cool Birds"
        return context



@method_decorator(login_required, name='dispatch')
class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'img', 'bio']
    template_name = "finch_create.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FinchCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('finch_detail', kwargs={'pk': self.object.pk})



@method_decorator(login_required, name='dispatch')
class FinchDetail(DetailView):
    model = Finch
    template_name = "finch_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context



@method_decorator(login_required, name='dispatch')
class FinchUpdate(UpdateView):
    model = Finch
    fields = ['name', 'img', 'bio', 'verified_finch']
    template_name = "finch_update.html"
    success_url = "/finch/"

    def get_success_url(self):
        return reverse('finch_detail', kwargs={'pk': self.object.pk})



@method_decorator(login_required, name='dispatch')
class FinchDelete(DeleteView):
    model = Finch
    template_name = "finch_delete_confirmation.html"
    success_url = "/finch/"



@method_decorator(login_required, name='dispatch')    
class SongCreate(View):

    def post(self, request, pk):
        formTitle = request.POST.get("title")
        minutes = request.POST.get("minutes")
        seconds = request.POST.get("seconds")
        formLength = 60 * int(minutes) + int(seconds)
        theFinch = Finch.objects.get(pk=pk)
        Song.objects.create(title=formTitle, length=formLength, finch=theFinch)
        return redirect('finch_detail', pk=pk)


class PlaylistSongAssoc(View):
    def get(self, request, pk, song_pk):
        # get the query parameter from the 
        assoc = request.GET.get("assoc")

        if assoc == "remove":
            # get the playlist by the pk, remove the song (row) with the song_pk
            Playlist.objects.get(pk=pk).songs.remove(song_pk)
        
        if assoc == "add":
            # get the playlist by the pk, add the song (row) with the song_pk
            Playlist.objects.get(pk=pk).songs.add(song_pk)
        
        return redirect('home')


class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("finch_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)


    
