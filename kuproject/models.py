from django.db import models


class user(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    pw = models.CharField(max_length=100)
    email = models.EmailField()


class favorite(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    code = models.IntegerField()
    name = models.CharField(max_length=45)
    cnt = models.IntegerField()
    price = models.IntegerField()
