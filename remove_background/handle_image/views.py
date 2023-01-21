from django.shortcuts import render

# Create your views here.


def render_index(request):
    return render(request, 'remove_background/index.html')
