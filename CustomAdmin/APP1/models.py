from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    dob=models.DateField(default=timezone.now)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    dob=models.DateField(default=timezone.now)
    email = models.EmailField()
    

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE)
    publication_date = models.DateField()
    rating=models.BigIntegerField(default=4,validators=[MinValueValidator(0), MaxValueValidator(5)])
    createdon=models.DateField(blank=True,null=True,auto_now_add=True)
    modifiedby=models.DateField(blank=True,null=True,auto_now=True)

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=128)
    immortal=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    cover = models.CharField(max_length=256, null=True, default=None)
    image = models.ImageField(blank=True,null=True,upload_to="media/")

    def __str__(self):
        return self.name


