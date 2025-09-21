from django.db import models

class Movie(models.Model):
    title = models.IntegerField()
    runtime = models.IntegerField()
    genre = models.CharField(max_length=30)
    totalAudience = models.BigIntegerField()

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

    room_number = models.IntegerField()
    row_count = models.IntegerField()
    col_count = models.IntegerField()

    class Meta:
        unique_together = ('theater', 'room_number')

    def __str__(self):
        return f"{self.theater.name} - {self.room_number}"
    
class Seats(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    row = models.IntegerField()
    col = models.IntegerField()

    def __str__(self):
        return f"행: {self.row}, 열: {self.col}"
    
class Screening(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    starttime = models.DateField()
    discountstatus = models.BooleanField()

    def __str__(self):
        return f"{self.theater.name}\n{self.movie.title}\n{self.starttime}\n"

class Reservation(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seats = models.ForeignKey(Seats, on_delete=models.CASCADE)

    booking_status = models.BooleanField()
    discount_satus = models.BooleanField()