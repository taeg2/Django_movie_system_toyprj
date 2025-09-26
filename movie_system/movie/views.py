from rest_framework import generics

from .serializers import MovieSerializer

from .models import Movie

class MovieListView(generics.ListAPIView):
    queryset = Movie
    serializer_class = MovieSerializer