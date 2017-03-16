import json
from django.http import HttpResponse

from app.dataManage.missingSecurities import MissingSecurities
from rest_framework.decorators import api_view

### Get missing security data for all securities in static database, without regard to
### whether or not they are still being held.
@api_view(['GET'])
def findAllMissingSecurities(request):

    ### Option to Include Proxies and Underlyings
    include_proxy_underlying = bool(request.GET['include_proxy_underlying'])

    missingSecurities = MissingSecurities(include_proxy_underlying=include_proxy_underlying)

    ### Find all missing securities, irrelevant of dates held.
    missingSecurities.findAll()
    missingSecurityData = missingSecurities.format()

    response = json.dumps({'missingSecurities': missingSecurityData})
    return HttpResponse(response)

### Get missing security data for only the securities that are currently being held based on whether
### or not they are completely missing from static DB (stage 1) or not.
@api_view(['GET'])
def findHeldMissingSecurities(request):

    include_proxy_underlying = bool(request.GET['include_proxy_underlying'])

    startDate = str(request.GET['startDate'])
    endDate = str(request.GET['endDate'])
    singleDate = str(request.GET['singleDate'])
    refreshType = str(request.GET['refreshType'])

    missingSecurityData = {}

    missingSecurities = MissingSecurities(include_proxy_underlying=include_proxy_underlying)
    if refreshType == 'single_date':
        ### Find Missing Securities On Date
        missingSecurities.findForHoldings(date=singleDate, start_date=None, end_date=None)
        missingSecurityData = missingSecurities.format()

    elif refreshType == 'between_dates':
        ### Find Missing Securities Between Dates
        missingSecurities.findForHoldings(date=None, start_date=startDate, end_date=endDate)
        missingSecurityData = missingSecurities.format()

    response = json.dumps({'missingSecurities': missingSecurityData})

    return HttpResponse(response)

