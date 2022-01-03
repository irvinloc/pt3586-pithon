from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=50)


