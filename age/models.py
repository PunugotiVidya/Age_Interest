from django.db import models

# Create your models here.


class Age(models.Model):
    startDate = models.DateField('Born Date')
    EndDate = models.DateField('Today Date')

    def __str__(self):
        return self.startDate
