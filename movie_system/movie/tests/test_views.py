# app_name/tests/test_views.py

from rest_framework.test import APITestCase
from django.urls import reverse
from movie.models import Movie, Theater, Room, Screening, Seats, Reservation
from datetime import datetime, date, time

class RoomRetrieveViewTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Test Movie")
        self.theater = Theater.objects.create(name="MegaBox")
        self.room = Room.objects.create(theater=self.theater, number=101, type="VIP")
        
        # RoomSerializer에서 start_time.hour 접근 오류 방지 위해 start_time을 DateTimeField 가정
        start_dt = datetime.combine(date.today(), time(14, 0))
        self.screening = Screening.objects.create(
            movie=self.movie, 
            room=self.room, 
            price=20000, 
            start_time=start_dt 
        )
        
        # 좌석 생성
        self.seat_a1 = Seats.objects.create(room=self.room, row=1, col=1)
        self.seat_a2 = Seats.objects.create(room=self.room, row=1, col=2)
        
        # 좌석 A1 예약 (예약됨)
        Reservation.objects.create(screening=self.screening, seats=self.seat_a1, booking_status=True)
        # 좌석 A2 예약 없음 (예약 안됨)

        # URL 설정. 'screening-room-detail'과 같은 URL name을 가정해야 함
        # 실제 urls.py에 정의된 URL 이름을 사용해야 합니다.
        self.url = f'/api/screening/{self.screening.id}/room/{self.room.id}/' # 실제 URL 경로로 수정

    def test_room_detail_includes_reservation_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # 응답 데이터 확인
        data = response.json()
        self.assertEqual(data['number'], 101)
        self.assertIn('seats', data)
        
        seats_data = data['seats']
        self.assertEqual(len(seats_data), 2)
        
        # A1 좌석 상태 확인 (예약됨)
        a1_seat = next(item for item in seats_data if item["row"] == 1 and item["col"] == 1)
        self.assertTrue(a1_seat['is_reserved'])
        
        # A2 좌석 상태 확인 (예약 안됨)
        a2_seat = next(item for item in seats_data if item["row"] == 1 and item["col"] == 2)
        self.assertFalse(a2_seat['is_reserved'])