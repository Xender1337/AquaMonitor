from django.shortcuts import render
from IHM.models import Temperature
# Create your views here.


def index(request):
    return render(request, "index.html",{})

