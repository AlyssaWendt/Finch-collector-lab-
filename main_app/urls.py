from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"), # <- new route
    path('finch/', views.FinchList.as_view(), name="finch_list"),
    path('finch/new/', views.FinchCreate.as_view(), name="finch_create"),
    path('finch/<int:pk>/', views.FinchDetail.as_view(), name="finch_detail"),
    path('finch/<int:pk>/update',views.FinchUpdate.as_view(), name="finch_update"),
    path('finch/<int:pk>/delete',views.FinchDelete.as_view(), name="finch_delete"),
    path('finch/<int:pk>/songs/new/', views.SongCreate.as_view(), name="song_create"),
   
]