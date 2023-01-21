from django.shortcuts import render

# Create your views here.


def render_index(request):
    print('pass here')
    if request.method == 'POST':
        remove_background_image(request)
        my_context = {}
        return render(request, 'remove_background/index.html', my_context)

    else:
        return render(request, 'remove_background/index.html')


def remove_background_image(request):
    print('remove bg')
