from rest_framework import serializers

from .models import Movie, Theater, Room, Screening, Seats

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "runtime", "genre", "totalAudience"]

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ["id", "name", "address"]


class SeatsSerializer(serializers.ModelSerializer):
    is_reserved = serializers.SerializerMethodField()

    class Meta:
        model  = Seats
        fields = ["id", "row", "col", "is_reserved"]
    
    def get_is_reserved(self, obj):
        #Room으로 전달받은 Screening contexts를 이용해야 함!
        screening = self.context.get('screening')

        if not screening:
            return False
        
        return screening.reservation_set.filter(seats=obj, booking_status = True).exists()


#Room 상세 조회
#역 참조이기 때문에 seats_set을 불러와서 serialize해서 다시 전달해야 함!
class RoomSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "seats", "number"]

    def get_seats(self, obj):
        seats_queryset = obj.seats_set.all()
        #View에서 RoomSerailizer를 호출할 때 context를 넣어주기 때문에 context를 그대로 전달하면 됨
        return SeatsSerializer(seats_queryset, many=True, context=self.context).data
    
#ScreeningSerializer에서 쓸 RoomSerializer
class RoomSummarySerailizer(serializers.ModelSerializer):
    seats_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "seats_count", "number", "type"]
    
    def get_seats_count(self, obj):
        return obj.seats_set.count()


class ScreeningSerializer(serializers.ModelSerializer):
    room = RoomSummarySerailizer()
    reserved_seats = serializers.SerializerMethodField()

    class Meta:
        model = Screening
        fields = ["id", "room", "reserved_seats", "price", "start_time", "discount_status"]

    def get_reserved_seats(self, obj):
        reserved_seats = obj.reservation_set.filter(booking_status = True).count()
        return reserved_seats