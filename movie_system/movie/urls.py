from django.urls import path

from .views import (
    MovieListView, TheaterListView, ScreeningListView,
    RoomRetrieveView
)

urlpatterns = [
    path("movie/", MovieListView.as_view(), name="movieList"),
    path("theater/", TheaterListView.as_view(), name="theaterList"),
    path("screening/", ScreeningListView.as_view(), name="screeningList"),
    path("screening/<int:screening_id>/room/<int:pk>/", RoomRetrieveView.as_view(), name="roomDetail"),
]