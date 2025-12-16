from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Events(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events'
    )

    rsvps = models.ManyToManyField(
        User,
        through='RSVP',
        related_name='rsvped_events',
        blank=True
    )

    image = models.ImageField(
        upload_to='events/',
        default='events/default.jpg'
    )

    def __str__(self):
        return self.name


class RSVP(models.Model):
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('going', 'Going'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # prevents duplicate RSVPs

    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.status})"