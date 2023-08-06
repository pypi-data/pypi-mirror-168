from django.template import Library, loader
from django.contrib.staticfiles import finders
import os

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def about(context):
    t = loader.get_template("photofolio/_about.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def hero(context):
    t = loader.get_template("photofolio/_hero.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def testimonials(context):
    t = loader.get_template("photofolio/_testimonials.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def gallery(context):
    t = loader.get_template("photofolio/_gallery.html")

    files = []

    if context['random_pickup_signatures'] and (context['category'] == 'signatures'):
        for item in context['gallery']:
            files += make_image_path_list(item[0])
        import random
        files = random.sample(files, 20)
    else:
        files = make_image_path_list(context['category'])

    context.update({
        'gallery_files': files
    })
    logger.info(context)
    return t.render(context.flatten())


def make_image_path_list(category: str) -> list:
    # static 파일 경로 찾는 방법
    # https://stackoverflow.com/questions/30430131/get-the-file-path-for-a-static-file-in-django-code
    relative_dir = ''.join(['img/gallery/', category])
    absolute_dir = finders.find(relative_dir)
    logger.info(f'gallery path: {absolute_dir}')

    files = []

    # static 갤러리 폴더안의 사진 파일의 수를 세어서 파일명을 리스트로 만든다.
    # https://www.delftstack.com/howto/python/count-the-number-of-files-in-a-directory-in-python/
    # https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    if absolute_dir:
        for file in os.listdir(absolute_dir):
            if os.path.isfile(os.path.join(absolute_dir, file)) and (file.endswith('.jpg') or file.endswith('.png')):
                files.append(''.join([relative_dir, '/', file]))
        logger.info(files)
    return files


@register.simple_tag(takes_context=True)
def contact(context):
    t = loader.get_template("photofolio/_contact.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def services(context):
    t = loader.get_template("photofolio/_services.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def pricing(context):
    t = loader.get_template("photofolio/_pricing.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())

