from django.db import models

# Create your models here.
class Urls(models.Model):
	urlFormulario = models.CharField(max_length=32)
