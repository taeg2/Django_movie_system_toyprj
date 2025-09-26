from django.urls import path

from .views import MovieListView

urlpatterns = [
    path("movie/", MovieListView.as_view(), name="movieList")
]