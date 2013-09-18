# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext

def forbidden(request):
    t = get_template('forbidden.html')
    html = t.render(Context({}))
    return HttpResponse(html)
