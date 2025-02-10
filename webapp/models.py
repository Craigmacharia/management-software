from django.db import models

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=225)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=225)

    province = models.CharField(max_length=200)

    country = models.CharField(max_length=125)
