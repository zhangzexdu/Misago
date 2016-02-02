from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import get_language
from django.views import i18n
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_page, never_cache

from misago.forums.lists import get_forums_list

from misago.core import momentjs


def forum_index(request):
    return render(request, 'misago/index.html', {
        'categories': get_forums_list(request.user),
    })


def home_redirect(*args, **kwargs):
    return redirect('misago:index')


@cache_page(86400, key_prefix='misagojsi18n')
@last_modified(lambda req, **kw: timezone.now())
def javascript_catalog(request):
    return i18n.javascript_catalog(request, 'djangojs', None)


@cache_page(86400, key_prefix='momentjsi18n')
@last_modified(lambda req, **kw: timezone.now())
def momentjs_catalog(request):
    locale_path = momentjs.get_locale_path(get_language())

    if locale_path:
        with open (locale_path, "r") as locale_file:
            locale = locale_file.read()
    else:
        locale = "";
    return HttpResponse(locale,
                        content_type='application/javascript; charset=utf-8')

