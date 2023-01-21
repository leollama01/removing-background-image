from django.urls import path

from . import views

urlpatterns = [
    path('', views.render_index, name='render_index'),
    path(
        'download/image/<str:name_image>', views.download_image,
        name='download_image'
    ),
]
