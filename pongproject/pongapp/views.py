from django.shortcuts import render

# Create your views here.

def pong_view(request):
    return render(request, 'pongapp/pongapp.html')
