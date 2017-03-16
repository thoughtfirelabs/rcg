import sys
sys.dont_write_bytecode = True
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth import logout


#### Anonymous required decorator restricts views to users who are not currently logged in.
def anonymous_required(view_function, redirect_to=None):
    return AnonymousRequired(view_function, redirect_to)


class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            from django.conf import settings
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)



########## Checks if the user is already logged in, if so they are redirected to the home page.  If not, they are
######### direceted to login.
@api_view(['GET'])
def custom_login(request):

    if request.user.is_authenticated():
        print 'User is authenticated.'
        return HttpResponseRedirect('/')
    else:
        return login(request)

@api_view(['GET','POST'])
def custom_logout(request):
    return logout(request,next_page = '/',template_name = 'base.html')
    #return HttpResponseRedirect('/')

@api_view(['GET'])
def getAuthenticatedUser(request):

    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return HttpResponse(username)
