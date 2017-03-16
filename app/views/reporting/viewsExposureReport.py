import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models.models import Portfolio, Fund
from app.views.workspace.views_Workspace import defaultWorkspaceDate
from app.modules.portfolio_module import portfolio
from app.reporting_modules.exposureReport import ExposureReport
from app.reporting_modules.managerExposureReport import ManagerExposureReport
from app.reporting_modules.tables.securityDetailTable import SecurityDetailTable

################################################################################
################################################################################
## Exposure Reporting

##########################
@api_view(['GET'])
def download_security_details(request):

    referenceID = str(request.GET['referenceID'])
    selection = str(request.GET['selection'])

    ### Get snapshot date from session - default it not available.
    if 'snapshot_date' not in request.session:
        defaultWorkspaceDate(request)
    snapshot_date = str(request.session['snapshot_date'])
    print 'Generating Security Detail CSV File for : ',snapshot_date
    snapshot_date = pd.to_datetime(snapshot_date)

    ######## Fund Situation
    if 'fund' in selection:

        ### Default for Now
        referenceID = 'LGWXBOK7'
        fund_name = Fund.objects.filter(id=referenceID).first().name

        models = Portfolio.objects.filter(fund_id=referenceID).all()
        portfolios = []

        ### Create Threads for Each Portfolio
        for model in models:

            ## Temporary Patch - 9740 is Rock Creek 40 Act Sub-Advser, Not Included in Limit Report
            if str(model.id) == '9740':
                continue

            ### Use PortID to Instantiate New Manager Limit Report in Thread
            port_id = str(model.id)
            p = portfolio(port_id,snapshot_date)
            p.run()

            print p.date_error
            ### Make Sure Date Valid (i.e. Not Weekend)
            if not p.date_error:
                portfolios.append(p)

        ### Check for errors
        if len(portfolios) == 0:
            print 'Invalid Date : ',snapshot_date,' -> Probably Weekend - '
            return Response('Invalid Date : '+snapshot_date.strftime("%Y-%m-%d")+' -> Probably Weekend - ')

        table = SecurityDetailTable(portfolios=portfolios,name=fund_name)
        table.generate()
        response = table.createCSVResponse()
        return response

    ######## Portfolio Situation
    else:

        p = portfolio(referenceID,snapshot_date)
        p.run()

        ### Check for errors
        if p.date_error:
            print 'Invalid Date : ',snapshot_date,' -> Probably Weekend - '
            return Response('Invalid Date : '+snapshot_date.strftime("%Y-%m-%d")+' -> Probably Weekend - ')

        table = SecurityDetailTable(portfolio=p)
        table.generate()
        response = table.createCSVResponse()
        return response



##########################
@api_view(['GET'])
def download_exposure_report(request):

    referenceID = str(request.GET['referenceID'])
    selection = str(request.GET['selection'])

    ### Get snapshot date from session - default it not available.
    if 'snapshot_date' not in request.session:
        defaultWorkspaceDate(request)
    snapshot_date = str(request.session['snapshot_date'])
    snapshot_date = pd.to_datetime(snapshot_date)

    ######## Fund Situation
    if 'fund' in selection:
        referenceID = 'LGWXBOK7' ### Hardcoded/defaulted for now.
        report = ExposureReport(referenceID, snapshot_date)
        report.generate()
        response = report.createCSVResponse()
        return response

    ######## Portfolio Situation
    else:
        report = ManagerExposureReport(referenceID, snapshot_date)
        report.generate()
        response = report.createCSVResponse()
        return response
