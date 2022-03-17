from django.db import models

class Location(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=6) #has to be of format nn.nnnnnn
    longitude = models.DecimalField(max_digits=8, decimal_places=6) #has to be of format nn.nnnnnn 

    def __str__(self):
        return (self.latitude,self.longitude)

class User(models.Model):
    email = models.EmailField()
    age = models.PositiveIntegerField()
    gender = models.BooleanField()
    password = models.CharField(max_length=50)
    hasbicycle = models.BooleanField(default=False) 
    currentLocation = models.ForeignKey(Location, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.email

class Trip(models.Model):
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return (self.UID,self.timestamp)

