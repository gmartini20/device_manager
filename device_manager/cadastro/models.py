from django.db import models

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class DeviceCategory(models.Model):
    name = models.CharField(max_length=90) 

class Device(models.Model):
    patrimony_number = models.CharField(max_length=50)
    description = models.CharField(max_length=555)
    category = models.ForeignKey(DeviceCategory)

class Person(models.Model):
    name = models.CharField(max_length=90) 
    level = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

class Stall(models.Model):
    obs = models.CharField(max_length=200)
    device = models.ForeignKey(Device)
    leader = models.ForeignKey(Person)
    room = models.ForeignKey(Room)

class StallTrainee(models.Model):
    trainee = models.ForeignKey(Person)
    stall = models.ForeignKey(Stall)
    hour_start = models.TimeField()
    hour_finish = models.TimeField()
    start_period = models.DateField()
    finish_period = models.DateField()

