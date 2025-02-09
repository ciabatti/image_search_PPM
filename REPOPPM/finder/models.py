from django.db import models

# Create your models here.
class Img(models.Model):
    photo = models.ImageField(upload_to='')
    name= models.CharField(max_length=255)
    description= models.TextField(default='')
 
    def __str__(self):
        return self.name