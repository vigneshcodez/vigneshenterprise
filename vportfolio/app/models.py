from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Blog(models.Model):
    bannerimage = models.ImageField(upload_to='blog/')
    image = models.ImageField(upload_to='blog/')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    content = HTMLField(blank=True, null=True)
    youtubevide = models.URLField(null=True,blank=True)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Testimonial(models.Model):
    name=models.CharField(max_length=25)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='testimonial/')

    def __str__(self):
        return self.name
    
class Projects(models.Model):
    name=models.CharField(max_length=25)
    description=models.TextField()
    image=models.ImageField(upload_to='projects/')
    link = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=70)
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return f'{self.name}  {self.subject}'
