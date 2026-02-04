from django.db import models

# Create your models here.
# 1
class Content(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField(default="Write your contents here...")
    published_date=models.DateField(auto_now_add=True)