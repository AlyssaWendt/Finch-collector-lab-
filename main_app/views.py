from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import Finch

class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

class FinchList(TemplateView):
    template_name = "finch_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        print(name)
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["finch"] = Finch.objects.filter(name__icontains=name)
            context["stuff_at_top"] = f"Searching through Finch list for {name}"
        else:
            context["finch"] = Finch.objects.all()
            context["stuff_at_top"] = "Cool Birds"
        return context
