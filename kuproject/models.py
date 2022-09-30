from django.db import models


class user(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    pw = models.CharField(max_length=100)
    email = models.EmailField()


class stock_fav(models.Model):
    user_id = models.CharField(max_length=20)
    code = models.FloatField()
    name = models.CharField(max_length=45)
    cnt = models.IntegerField()
    price = models.IntegerField()
