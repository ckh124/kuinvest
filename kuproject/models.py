from django.db import models


class user(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    pw = models.CharField(max_length=100)
    email = models.EmailField()


class stock_fav(models.Model):
    user_id = models.CharField(max_length=20)
    code = models.IntegerField(max_length=6)
    name = models.CharField(max_length=45)
    cnt = models.IntegerField()
    price = models.IntegerField()


class stock_comm(models.Model):
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    context = models.TextField()
    code = models.IntegerField(max_length=6)
    name = models.CharField(max_length=45)
    rep_cnt = models.PositiveIntegerField(default=0)


class community(models.Model):
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    context = models.TextField()
    rep_cnt = models.PositiveIntegerField(default=0)

class comment(models.Model):
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    context = models.TextField()
    fk = models.ForeignKey('stock_comm', null=True, blank=True, on_delete=models.CASCADE)
    code = models.IntegerField(max_length=6)