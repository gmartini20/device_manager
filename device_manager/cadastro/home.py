# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import StallTrainee, User, Stall, Feature
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render_to_response
from decorator import my_login_required
from users import get_user_features
from datetime import datetime, timedelta

@my_login_required
def show_home(request):
    t = get_template('home.html')
    expiration_messages = []
    try:
        today = datetime.now()
        expiration_date = today + timedelta(days=10)
        username=request.COOKIES.get("logged_user")
        user = User.objects.select_related().get(username=username)
        message_feature = Feature.objects.get(name="home_message")
        has_message = False
        if message_feature and user.profile.features.get(id = message_feature.id):
            has_message = True
            stall_list = Stall.objects.filter(leader = user.person)
            stall_trainees = StallTrainee.objects.select_related().filter(stall__in = stall_list, finish_period__gte=today, finish_period__lte=expiration_date)
            for trainee in stall_trainees:
                expiration_messages.append(u'O período de utilização da baia {0} na sala {1} pelo bolsista {2} irá expirar em {3}.'.format(trainee.stall.name, trainee.stall.room.number, trainee.trainee.name, trainee.finish_period.strftime('%d/%m/%Y')))
    except:
        messages.error(request, u'Ocorreu um erro ao processar a requisição, por favor tente novamente.')
    html = t.render(Context({'welcome_message': u'Bem-vindo ao sistema de controle de dispositivos', 'message': expiration_messages, 'has_message': has_message, 'features':get_user_features(request)}))
    return HttpResponse(html)
