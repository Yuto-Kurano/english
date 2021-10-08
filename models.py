from django.db import models

class Words(models.Model):
    word = models.CharField(max_length = 100)
    meaning = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)

        

        