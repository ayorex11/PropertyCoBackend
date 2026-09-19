from django.db import models



class Blog(models.Model):
    title = models.CharField(max_length=250, blank=False)
    body = models.TextField(max_length=1000000, blank= False)
    image = models.ImageField(upload_to='news', blank=True)
    date_created = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    ordering = ['-date_created',]