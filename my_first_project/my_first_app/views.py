from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Content

# Create your views here.
# 2
def Home(request):
    return render(request,'my_first_app/home.html')

#5
class welcome(View):
    def get(self,request):
        return HttpResponse("Welcome to Django CBV")

#6
def listBlog(request):
    blog=Content.objects.all()
    titles=[blog.title for title in titles]
    title_str=", ".join(titles) if titles else "Empty,No blog exists"
    return HttpResponse(title_str)