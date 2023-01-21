import mimetypes
import os
import shutil
from datetime import datetime

import magic
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from rembg import remove

from .models import ImageUploaded, LogError

# Create your views here.


def render_index(request):
    my_context = {}

    currentDate = datetime.now()
    description = ''

    target_folder = os.getcwd() + '/media'

    # Reference: https://stackoverflow.com/a/185941/21053661
    try:
        for filename in os.listdir(target_folder):
            _file_path = os.path.join(target_folder, filename)

            try:
                if os.path.isfile(_file_path) or os.path.islink(_file_path):
                    os.unlink(_file_path)

                elif os.path.isdir(_file_path):
                    shutil.rmtree(_file_path)

            except Exception as e:
                description = 'Failed to delete %s. Reason: %s' % (
                    _file_path, e)

                try:
                    insertLog = LogError(
                        date=currentDate, description=description)
                    insertLog.save()

                except Exception as e:
                    print(str(e))

    except Exception as e:
        description = 'Failed to delete %s. Reason: %s' % (
            _file_path, e)
        try:
            insertLog = LogError(
                date=currentDate, description=description)
            insertLog.save()

        except Exception as e:
            print(str(e))

    if request.method == 'POST':
        try:
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
                    file_to_save = file_system_storage.save(
                        _upload.name, _upload)
                    file_path = file_system_storage.url(file_to_save)

                    rm_bg = remove_background_image(request, file_path)

                    if rm_bg is not False:
                        try:
                            insertImageUploaded = ImageUploaded(
                                date=currentDate
                            )
                            insertImageUploaded.save()

                        except Exception as e:
                            try:
                                description = str(e) + '- except in ' \
                                    'render_index function, rm_bg is not False'
                                insertLog = LogError(
                                    date=currentDate, description=description
                                )
                                insertLog.save()

                            except Exception as e:
                                print(str(e), '- except upload file')

                        my_context['image'] = rm_bg
                        return render(
                            request, 'remove_background/index.html',
                            context=my_context
                        )

                    else:
                        my_context['warning'] = 'Oh no! Something wrong ' \
                            'happened. Please, try again.'
                        return render(
                            request, 'remove_background/index.html',
                            context=my_context
                        )

                else:
                    my_context['warning'] = 'Invalid/incorrect file. ' \
                        'Try again.'
                    return render(
                        request, 'remove_background/index.html',
                        context=my_context
                    )

            else:
                my_context['warning'] = 'No files uploaded. Try again.'
                return render(
                    request, 'remove_background/index.html', context=my_context
                )

        except Exception as e:
            try:
                description = str(e) + '- except in render_index function'
                insertLog = LogError(date=currentDate, description=description)
                insertLog.save()

            except Exception as e:
                print(str(e), '- except upload file')

            my_context['warning'] = 'Oh no! Something wrong ' \
                'happened. Please, try again.'
            return render(
                request, 'remove_background/index.html',
                context=my_context
            )

    else:
        return render(request, 'remove_background/index.html')


def remove_background_image(request, image_path):
    _return = False

    if request.method == 'POST':
        try:
            current_dir = os.getcwd()
            full_path = str(current_dir) + str(image_path)
            name_old_file = image_path.split('/')[-1]
            extension_file = '.' + name_old_file.split('.')[-1]
            output_path = full_path.replace(name_old_file, '')

            name_old_file = name_old_file.replace(extension_file, '')
            final_output = output_path + name_old_file + '_no-bg.png'

            input_image = Image.open(full_path)
            output = remove(input_image)
            output.save(final_output)

            _return = name_old_file + '_no-bg.png'

        except Exception as e:
            currentDate = datetime.now()
            description = str(e) + \
                ' - exception in function \'remove_background_image\''

            try:
                insertLog = LogError(date=currentDate, description=description)
                insertLog.save()

            except Exception as e:
                print(str(e), 'trying saving log error description')

    return _return


# Reference: https://djangoadventures.com/how-to-create-file-download-links-in-django/#:~:text=In%20order%20to%20create%20a
def download_image(request, name_image):
    path_to_image = os.getcwd()
    path_to_image += '/media/' + name_image

    file_open = open(path_to_image, 'rb')
    mime_type, _ = mimetypes.guess_type(path_to_image)

    response = HttpResponse(file_open, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % name_image

    return response


# get ip to limit requests in certain time
# def get_ip_address(request):
#     user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
#     if user_ip_address:
#         ip = user_ip_address.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
