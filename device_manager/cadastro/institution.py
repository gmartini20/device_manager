# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import Institution
from forms import InstitutionForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
from users import get_user_features

institution_list_header = [u'Nome', u'País', u'Observação']

@my_login_required
def list_institution(request):
    t = get_template('list.html')
    institution_list = Institution.objects.all().order_by('id')
    values_dict = {}
    for institution in institution_list:
        institution.list_values = [institution.name, institution.country, institution.observation]
    html = t.render(Context({'page_title': u'Instituições', 'header_name_list': institution_list_header, 'object_list': institution_list, 'edit_name': 'institution', 'can_remove': True, 'features':get_user_features(request)}))
    return HttpResponse(html)

@my_login_required
def remove_institution(request, id):
    obj = Institution.objects.get(id=id)
    obj.is_removed = True
    obj.save()
    return list_institution(request)

@my_login_required
def edit_institution(request, id=None):
    context = {'page_title': u'Instituição', 'edit_name': 'institution', 'has_back': False, 'features':get_user_features(request)}
    t = get_template('edit.html')
    institution = None
    form = InstitutionForm()
    try:
        if request.method == 'POST':
            form = InstitutionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                institution = _save_institution(cd)
                initial = institution.__dict__
                messages.success(request, 'Instituição salva com sucesso.')
                form = InstitutionForm(initial=initial)

        elif id:
            institution = Institution.objects.get(id=id)
            initial = institution.__dict__
            form = InstitutionForm(initial=initial)

    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    context = _set_institution_form_context(institution, form, context)
    return render_to_response('edit.html', context, context_instance=RequestContext(request))

def _save_institution(cd):
    institution = Institution()
    institution.id = cd['id'] or None
    institution.observation = cd['observation']
    institution.name = cd['name']
    institution.country = cd['country']
    institution.save()
    return institution

def _set_institution_form_context(institution, form, context):
    if institution:
        context['object_id'] = institution.id
    
    context['has_list'] = False
    context['fields'] = form.as_ul()
    return context

