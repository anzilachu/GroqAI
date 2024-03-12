from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='authors', blank=True, default='default.jpg')
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chat:author_detail', kwargs={'username': self.name})
