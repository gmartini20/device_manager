from django.db import models

class Room(models.Model):
    number = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Computer(models.Model):
    patrimony_number = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    video_card = models.CharField(max_length=50)
    hard_disk = models.CharField(max_length=50)

class Person(models.Model):
    name = models.CharField(max_length=90) 
    level = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

class Stall(models.Model):
    obs = models.CharField(max_length=200)
    computer = models.ForeignKey(Computer)
    leader = models.ForeignKey(Person)
    room = models.ForeignKey(Room)

class StallTrainee(models.Model):
    trainee = models.ForeignKey(Person)
    stall = models.ForeignKey(Stall)
    date_start = models.DateField()
    date_finish = models.DateField()

