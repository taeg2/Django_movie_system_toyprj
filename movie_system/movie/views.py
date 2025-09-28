from rest_framework import generics

from django.shortcuts import get_object_or_404

from .serializers import (
    MovieSerializer, TheaterSerializer, ScreeningSerializer,
    RoomSerializer
)

from .models import (
    Movie, Theater, Screening, Room
)

class MovieListView(generics.ListAPIView):
    queryset = Movie
    serializer_class = MovieSerializer

#GET theater?province_name = "province_name"/
#이것도 query로 데이터 탐색을 manager로 대체 가능 -> view의 크기는 최대한 줄이는 게 좋음
class TheaterListView(generics.ListAPIView):
    queryset = Theater
    serializer_class = TheaterSerializer

    def get_queryset(self):
        queryset = self.queryset

        province_name = self.request.query_parms.get("province_name", "서울")

        if province_name:
            queryset = queryset.filter(address__startswith=province_name)
        
        return queryset

#Screening?movie_id={movie_id}&theater_id={theater_id}
#view가 filtering 하기 위해 모델의 세부 구현을 이용해서 filtering 중임 -> 리팩터링 필요.
class ScreeningListView(generics.ListAPIView):
    queryset = Screening
    serializer_class = ScreeningSerializer

    def get_queryset(self):
        query_set = self.queryset

        movie_id = self.request.query_parms.get("movie_id")
        theater_id = self.request.query_parms.get("theater_id")
        cur_date = self.request.query_parms.get("cur_date")

        if movie_id:
            query_set = query_set.filter(movie_id = movie_id)
        
        if theater_id:
            query_set = query_set.filter(room__theater_id = theater_id)
        
        if cur_date:
            query_set = query_set.filter(cur_date__date = cur_date)
        
        return query_set

#api/screening/{screening_id}/room/<int:pk>
class RoomRetrieveView(generics.RetrieveAPIView):
    queryset = Room
    serializer_class = RoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        screening_id = self.kwargs.get("screening_id")

        if screening_id:
            screening = get_object_or_404(Screening, pk=screening_id)
            context['screening'] = screening
        
        return context