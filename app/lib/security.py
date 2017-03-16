import sys
import os
#from AssetAllocationModel.AAM.models import UserPermission, Applications

## Manually Edited for Now - Will Make Similiar to AAM When Incorporated
def getUserApps(request):
	return ['Daily Metrics Viewer','Daily Platform','Data','Fund Screener','Index Screens',
	'Indexes','Manager Analytics','Maps','Performance Updates','Portfolio Analytics','Portfolio Trends','Position File','RCG Indices']
	# try:
	# 	#return UserPermission.objects.get(user=request.user).applications.all().order_by('name')
	# except:
	# 	return Applications.objects.filter(name='Manager Analytics')

# def checkPermission(request, application, portfolio=''):
# 	hasPermission = UserPermission.objects.filter(user=request.user, applications=application)
# 	if portfolio != '':
# 		hasPermission.filter(portfolios=portfolio)
# 	if len(hasPermission) == 0:
# 		return False
# 	else:
# 		return True