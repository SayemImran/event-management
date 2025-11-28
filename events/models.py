from django.db import models

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
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='events')
    
    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    event = models.ManyToManyField(Events, related_name='participants')

    def __str__(self):
        return self.name