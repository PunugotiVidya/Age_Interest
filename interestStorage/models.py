from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class InterestStorageModel(models.Model):
    givenPerson = models.ForeignKey(User, on_delete=models.CASCADE)
    takenPerson = models.CharField(default="", max_length=50,verbose_name="Taken Person")
    amount = models.IntegerField(verbose_name="Taken Amount")
    rate = models.FloatField()
    startDate = models.DateField(verbose_name="Start Date")
    presentinterest = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.takenPerson}'

    def get_absolute_url(self):
        return reverse('list-interests')
