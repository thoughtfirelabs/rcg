import sys
sys.dont_write_bytecode = True
from django.shortcuts import render_to_response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

### View that associates the different HTML templates with keywords that can be accessed from
### AJAX calls or directly from the url patterns.  Allows the individual pages to be decorated with
### login and permission requirements.


##########################################################################
### Base Level Views

######################### Restricts usage only to users who have staff rights and can
######################### edit data in the data management section.
def is_staff(user):
	return user.groups.filter(name="staff").exists()

@user_passes_test(is_staff)
@login_required
def data_manage(request):
	return render_to_response('data_manage/data_manage.html')

######################### Restricts usage only to users who have data administration rights, 
######################### and this means they can perform the functions in the data admin tab
@login_required
def data_manageAdmin(request):

	exists = request.user.groups.filter(name='dataManageAdministrator').exists()
	if exists:
		return render_to_response('data_manage/admin/adminData.html')
	else:
		### Use doesn't have administrator data management permission, restrict access.
		raise PermissionDenied()

@login_required
def portfolio_level(request):
	return render_to_response('portfolio_level/portfolio_level.html')

@login_required
def fund_level(request):
	return render_to_response('fund_level/fund_level.html')

@login_required
def holding_level(request):
	return render_to_response('holding_level/holding_level.html')

@login_required
def reporting_level(request):
	return render_to_response('reporting_level/reporting_level.html')

