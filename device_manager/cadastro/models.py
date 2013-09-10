from django.db import models

class GenericManager(models.Manager):
    def get_query_set(self):
        return super(GenericManager, self).get_query_set().exclude(is_removed=True)

class DeviceCategory(models.Model):
    name = models.CharField(max_length=90)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        self.is_removed = True
        self.save()

class Device(models.Model):
    patrimony_number = models.CharField(max_length=50)
    description = models.CharField(max_length=555)
    category = models.ForeignKey(DeviceCategory)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        self.is_removed = True
        self.save()

class Period(models.Model):
    name = models.CharField(max_length=200)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

class Institution(models.Model):
    name = models.CharField(max_length=155)
    observation = models.CharField(max_length=555)
    country = models.CharField(max_length=155)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()
    
    def delete(self):
        self.is_removed = True
        self.save()

class Person(models.Model):
    name = models.CharField(max_length=90) 
    level = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    observation = models.CharField(max_length=555)
    institution = models.ForeignKey(Institution)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()
    
    def delete(self):
        self.is_removed = True
        self.save()

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    is_removed = models.BooleanField(default=False)
    syndic = models.ForeignKey(Person, null=True)
    objects = GenericManager()

    def delete(self):
        for stall in self.stall_set.all():
            stall.delete()
        self.is_removed = True
        self.save()

class Stall(models.Model):
    name = models.CharField(max_length=200)
    obs = models.CharField(max_length=200)
    devices = models.ManyToManyField(Device)
    leader = models.ForeignKey(Person)
    room = models.ForeignKey(Room)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        for trainee in self.stalltrainee_set.all():
            trainee.delete()
        self.is_removed = True
        self.save()

class StallTrainee(models.Model):
    trainee = models.ForeignKey(Person)
    stall = models.ForeignKey(Stall)
    start_period = models.DateField()
    finish_period = models.DateField()
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        for period in self.stalltraineeperiod_set.all():
            period.delete()
        self.is_removed = True
        self.save()


class StallTraineePeriod(models.Model):
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    periods = models.ManyToManyField(Period)
    stall_trainee = models.ForeignKey(StallTrainee)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        self.is_removed = True
        self.save()

class Feature(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=555)
    uri = models.CharField(max_length=50)

class Profile(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=555)
    features = models.ManyToManyField(Feature)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        self.is_removed = True
        self.save()

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    person = models.ForeignKey(Person)
    profile = models.ForeignKey(Profile, null=True)
    is_removed = models.BooleanField(default=False)
    objects = GenericManager()

    def delete(self):
        self.is_removed = True
        self.save()
