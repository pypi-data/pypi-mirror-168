from django.template import Library, loader
from ..forms import AppointmentForm
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
def hero(context):
    t = loader.get_template("medicio/_hero.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def whyus(context):
    t = loader.get_template("medicio/_whyus.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def services(context):
    t = loader.get_template("medicio/_services.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def cta(context):
    t = loader.get_template("medicio/_cta.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def about(context):
    t = loader.get_template("medicio/_about.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def counts(context):
    t = loader.get_template("medicio/_counts.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def appointment(context):
    t = loader.get_template("medicio/_appointment.html")
    context.update({
        'form': AppointmentForm(),
        'post_message': context.get('post_message', None),
        'naver_link': context.get('naver', None),
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def departments(context):
    t = loader.get_template("medicio/_departments.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def testimonials(context):
    t = loader.get_template("medicio/_testimonials.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def gallery(context):
    t = loader.get_template("medicio/_gallery.html")

    # static 파일 경로 찾는 방법
    # https://stackoverflow.com/questions/30430131/get-the-file-path-for-a-static-file-in-django-code
    dir = finders.find('img/gallery')
    logger.info(f'gallery path: {dir}')

    files = []

    # static 갤러리 폴더안의 사진 파일의 수를 세어서 파일명을 리스트로 만든다.
    # https://www.delftstack.com/howto/python/count-the-number-of-files-in-a-directory-in-python/
    # https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    if dir:
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.jpg'):
                files.append(file)
        logger.info(files)

    context.update({
        'gallery_files': files
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def doctors(context):
    t = loader.get_template("medicio/_doctors.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def faq(context):
    t = loader.get_template("medicio/_faq.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def contact(context):
    t = loader.get_template("medicio/_contact.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def pricing(context):
    t = loader.get_template("medicio/_pricing.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def features(context):
    t = loader.get_template("medicio/_features.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


