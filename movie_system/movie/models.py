from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100, default="")
    runtime = models.IntegerField(default=0)
    genre = models.CharField(max_length=100, default="")

    #예약이 증가 -> totalAudience 같이 증가
    #signal.py로 구현 예정
    totalAudience = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.name

class Room(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

    number = models.IntegerField(default=0)
    type = models.CharField(max_length=100, default="")

    class Meta:
        unique_together = ('theater', 'number')

    def __str__(self):
        return f"{self.theater.name} - {self.number}"
    
class Seats(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)

    class Meta:
        unique_together = ('room', 'row', 'col')

    def __str__(self):
        return f"행: {self.row}, 열: {self.col}"
    
class Screening(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    price = models.IntegerField(default=0)
    start_time = models.DateField()
    discount_status = models.BooleanField(default=False)

    def discount_price(self):
        if self.is_discount:
            self.discount_status = True
            return self.price * 0.9

    def is_discount(self):
        start_hour = self.start_time.hour
        return start_hour < 10 or start_hour > 22

    def __str__(self):
        return f"{self.movie.title}\n{self.start_time}\n"

class Reservation(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.ForeignKey(Seats, on_delete=models.CASCADE)

    booking_status = models.BooleanField(default=False)