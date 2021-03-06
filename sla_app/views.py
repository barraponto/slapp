from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.template import RequestContext, loader
from sla_app.forms import CompanyForm
from sla_app.models import Company
from django.contrib.auth.models import User

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url

##To get logged in user info 
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)
# Create your views here.
# Create your views here.


def pag_inicio(request):
    return render(request,'sla_app/pagina_inicio.html',{'new_item_text':request.POST.get('item_text','')})

def home(request):
    template = loader.get_template('sla_app/home.html')
    context = RequestContext(request, {
        'test': 'test',
    })
    return HttpResponse(template.render(context))

#def profile_update(request):
#    template = loader.get_template('sla_app/profile_update.html')
#    context = RequestContext(request, {
#        'test': 'test',
#    })
#    return HttpResponse(template.render(context))

# Create your views here.

def profile_update(request):
    if request.method=='POST':
        new_company_name=request.POST.get('name','Enter Company Name')
        new_service_name=request.POST.get('service','Enter detail of service ofered')
        user_list=get_all_logged_in_users()
        try:
            #first_user=User(pk=user_list[0])
            first_user=User.objects.create_user('testuser1','test@gmail.com',password='testpass')
        except:
            first_user=User(username='testuser1')
            print("el usuario es el %s"%first_user.username)
        try:
            Company.objects.create(user=first_user,name=new_company_name,service=new_service_name)
        except:
            first_user.company.name=new_company_name
            first_user.company.service=new_service_name
            first_user.company.save()
        return redirect('/slapp/profile_update/')
    
    new_company_name='Enter Company Name'
    new_service_name='Enter detail of service ofered'


    return render(request,'sla_app/profile_update.html',
        {'new_company_name':new_company_name,
        'new_service_name':new_service_name,
        })


#def profile_update(request, template_name='sla_app/profile_update.html',
#          redirect_field_name=REDIRECT_FIELD_NAME,
#          company_form=CompanyForm,
#          current_app=None, extra_context=None):
#    """
#    Displays the profile update form and handles the update action.
#    """
#    redirect_to = request.POST.get(redirect_field_name,
#                                   request.GET.get(redirect_field_name, ''))
#
#    if request.method == "POST":
#        form = company_form(data=request.POST)
#        if form.is_valid():
#
#            # Ensure the user-originating redirection url is safe.
#            if not is_safe_url(url=redirect_to, host=request.get_host()):
#                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
#
#            # Save a new Article object from the form's data.
#            
#            update_profile = form.save(commit=False)
#            update_profile.user = request.user
#            update_profile.save()
#            return HttpResponseRedirect(redirect_to)
#    else:
#        form = company_form(request)
#
#    current_site = get_current_site(request)
#
#    context = {
#        'form': form,
#        redirect_field_name: redirect_to,
#        'site': current_site,
#        'site_name': current_site.name,
#    }
#    if extra_context is not None:
#        context.update(extra_context)
#
#    if current_app is not None:
#        request.current_app = current_app
#
#    return TemplateResponse(request, template_name, context)

#def index(request):
#    return HttpResponse("This will hold the SLAPP Landing Page")