from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    cards = [
        {"name" : "Розділ 1",
         "image" : "django.png"
         },
        {"name": "Розділ 2",
         "image": "fastapi.png"
         },
        {"name": "Розділ 3",
         "image": "flask.png"
         },
    ]
    return render(request, 'main/index.html',{"cards" : cards})

def about(request):
    text = 'Це сторінка про нас'
    frameworks = ["django","flask","fastapi"].clear()
    return render(request,'main/about.html',{'frameworks':frameworks})
