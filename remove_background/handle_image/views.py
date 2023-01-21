import magic
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.


def render_index(request):
    my_context = {
        'return': 0,
        'message': ''
    }

    if request.method == 'POST':
        if request.FILES['_upload']:
            _upload = request.FILES['_upload']
            can_save = False
            valid_extensions = ['jpg', 'jpeg', 'png']
            magic_file = magic.from_buffer(_upload.read(2048))

            for extensions in valid_extensions:
                if extensions.upper() in magic_file.upper():
                    can_save = True
                    break

            if can_save:
                file_system_storage = FileSystemStorage()
                file_to_save = file_system_storage.save(_upload.name, _upload)
                file_path = file_system_storage.url(file_to_save)

                remove_background_image(request, file_path)

            else:
                print('invalid file')

            try:
                # print(_upload)
                # print(magic.from_buffer(_upload.read(2048)))
                print(type(magic.from_buffer(_upload.read(2048))))

            except Exception as e:
                print(str(e))

        else:
            print('no file uploaded')

        # remove_background_image(request, '')
        return render(request, 'remove_background/index.html', my_context)

    else:
        return render(request, 'remove_background/index.html')


def remove_background_image(request, image_path):
    print('remove bg')


# def get_ip_address(request):
#     user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
#     if user_ip_address:
#         ip = user_ip_address.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
