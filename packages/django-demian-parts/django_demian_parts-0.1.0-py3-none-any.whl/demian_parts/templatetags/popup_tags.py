from django.template import Library
from ..models import Type4, Type3, Type2, Type1

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.inclusion_tag(f"popup/popup.html")
def show_popup():
    active_type4s = Type4.objects.filter(activate__exact=True)
    active_type3s = Type3.objects.filter(activate__exact=True)
    active_type2s = Type2.objects.filter(activate__exact=True)
    active_type1s = Type1.objects.filter(activate__exact=True)
    print(f"Activated {Type4.__name__} objects : {active_type4s}")
    print(f"Activated {Type3.__name__} objects : {active_type3s}")
    print(f"Activated {Type2.__name__} objects : {active_type2s}")
    print(f"Activated {Type1.__name__} objects : {active_type1s}")

    try:
        type4 = active_type4s[0]
    except IndexError:
        type4 = None
    try:
        type3 = active_type3s[0]
    except IndexError:
        type3 = None
    try:
        type2 = active_type2s[0]
    except IndexError:
        type2 = None
    try:
        type1 = active_type1s[0]
    except IndexError:
        type1 = None

    if type4 is not None:
        obj = type4
    elif type3 is not None:
        obj = type3
    elif type2 is not None:
        obj = type2
    elif type1 is not None:
        obj = type1
    else:
        obj = None

    print(obj.__class__.__name__)
    context = {
        "dont_show_again": "다시보지않기",
        "type": obj.__class__.__name__,
        "obj": obj,
    }
    logger.info(context)
    return context
