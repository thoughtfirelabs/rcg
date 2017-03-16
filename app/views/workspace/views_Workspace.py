import sys
sys.dont_write_bytecode = True
import pandas as pd
import json

from django.views.generic.base import View
from django.http import HttpResponse
from app.models.models import Portfolio, Fund, holdingRecord

import datetime

### Defaults the Workspace Date for a Given Session
def defaultWorkspaceDate(request):

    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    snapshot_date = yesterday.strftime('%m/%d/%Y')
    request.session['snapshot_date']=snapshot_date
    return


########################################################################
class WorkspaceView(View):

    def __init__(self):

        self.validity = True
        self.fund_id = None
        self.portfolio_id = None
        self.snapshot_date = None

        return

    #####################################################
    #### Directs the process of the view based on the request data
    def get(self, request):

        handle = str(request.GET['handle'])
        print handle
        if handle == 'getWorkspace':
            response = self.getWorkspace(request)

        ### Loading Workspace Data
        elif handle == 'loadPortfolios':
            response = self.loadPortfolios(request)
        elif handle == 'loadFunds':
            response = self.loadFunds(request)

        ### Setting Workspace Variables
        elif handle == 'setDate':
            response = self.setWorkspaceDate(request)
        elif handle == 'setFund':
            response = self.setWorkspaceFund(request)
        elif handle == 'setFundandDate':
            response = self.setWorkspaceFundandDate(request)
        elif handle == 'setPortfolio':
            response = self.setWorkspacePortfolio(request)
        else:
            response = HttpResponse("Invalid Handler")
        return response

    ### Creates a respnose object representing all of the data for the workspace in the session
    def createWorkspaceResponse(self,request):

        response = {}

        ### Populate Response for Portfolio ID
        if 'portfolio_id' in request.session:
            port_id = str(request.session['portfolio_id'])
            response['portfolio_id']=port_id

            if 'portfolio_name' in request.session:
                response['portfolio_name'] = str(request.session['portfolio_name'])
            else:
                ### Get Portfolio Name for ID
                portObj = Portfolio.objects.filter(id=port_id).first()
                response['portfolio_name'] = str(portObj.portfolio_name)

        ### Default Portfolio ID
        else:
            defaultPort = Portfolio.objects.first()

            request.session['portfolio_name'] = str(defaultPort.portfolio_name)
            request.session['portfolio_id'] = str(defaultPort.id)

            response['portfolio_name'] = str(defaultPort.portfolio_name)
            response['portfolio_id'] = str(defaultPort.id)

        ### Default For Now
        ### Populate Response for Portfolio ID
        if 'fund_id' in request.session:

            fund_id = str(request.session['fund_id'])
            response['fund_id'] = fund_id

            if 'fund_name' in request.session:
                response['fund_name'] = str(request.session['fund_name'])
            else:
                ### Get Portfolio Name for ID
                fundObj = Fund.objects.filter(id=fund_id).first()
                response['fund_name'] = str(fundObj.fund_name)

        ### Default Fund ID
        else:
            fund_id = 'LGWXBOK7'
            defaultFund = Fund.objects.filter(id=fund_id).first()

            request.session['fund_name'] = str(defaultFund.name)
            request.session['fund_id'] = str(defaultFund.id)

            response['fund_name'] = str(defaultFund.name)
            response['fund_id'] = str(defaultFund.id)

        ### Populate Response for Snapshot Date
        if 'snapshot_date' in request.session:
            snapshot_date = str(request.session['snapshot_date'])
            response['snapshot_date']=snapshot_date
            response['valid'] = self.validWorkspaceDate(snapshot_date)

        ### Use a default date if the available session date is not there
        else:
            ## Set workspace session date to default
            defaultWorkspaceDate(request)
            response['snapshot_date'] = str(request.session['snapshot_date'])
            response['valid'] = self.validWorkspaceDate(request.session['snapshot_date'])

        return response

    ### The route connected to the API Call to get the workspace data
    def getWorkspace(self,request):
        response = self.createWorkspaceResponse(request)
        return HttpResponse(json.dumps(response))

    ### Sets both the workspace  fund and date for front end convenience and returns
    ### response associated with the updated id and date if successful
    def setWorkspaceFundandDate(self,request):

        snapshot_date = pd.to_datetime(str(request.GET['snapshot_date']))
        snapshot_date = snapshot_date.strftime('%m/%d/%Y')
        validity = self.validWorkspaceDate(snapshot_date)

        ### Only update session date if it is a valid date.
        if validity:
            ### Store new portfolio id to session
            fund_id = str(request.GET['fund_id'])
            ### To do: validate portfolio id
            request.session['fund_id'] = fund_id

            ### Get Fund Name for ID
            fundObj = Fund.objects.filter(id=fund_id).first()
            request.session['fund_name'] = str(fundObj.fund_name)

        ### Send back previously valid workspace date if updating one is not valid
        response = self.createWorkspaceResponse(request)

        return response

    ### Sets the workspace date for the application
    def setWorkspaceDate(self,request):

        snapshot_date = pd.to_datetime(str(request.GET['snapshot_date']))
        snapshot_date = snapshot_date.strftime('%m/%d/%Y')
        validity = self.validWorkspaceDate(snapshot_date)

        ### Only update session date if it is a valid date.
        if validity:
            request.session['snapshot_date']=snapshot_date
        ### Send back previously valid workspace date if updating one is not valid

        ### Create Response from Request Session
        response = self.createWorkspaceResponse(request)
        return HttpResponse(json.dumps(response))

    ### Sets the workspace portfolio for the application
    ### This is defaulted for now.
    def setWorkspaceFund(self, request):

        ### Store new portfolio id to session
        fund_id = 'LGWXBOK7'
        request.session['fund_id'] = fund_id

        ### Get Fund Name for ID
        fundObj = Fund.objects.filter(id=fund_id).first()
        request.session['fund_name'] = str(fundObj.fund_name)

        ### Create Response from Request Session
        response = self.createWorkspaceResponse(request)
        return HttpResponse(json.dumps(response))

    ### Sets the workspace portfolio for the application
    def setWorkspacePortfolio(self, request):

        ### Store new portfolio id to session
        port_id = str(request.GET['port_id'])
        ### To do: validate portfolio id
        request.session['portfolio_id'] = port_id

        ### Get Portfolio Name for ID
        portObj = Portfolio.objects.filter(id=port_id).first()
        request.session['portfolio_name'] = str(portObj.portfolio_name)

        ### Create Response from Request Session
        response = self.createWorkspaceResponse(request)
        return HttpResponse(json.dumps(response))


    ### Validates the workspace date depending on whether or not holding models exist
    ### for this date.
    def validWorkspaceDate(self,snapshot_date):

        if type(snapshot_date) is str:
            snapshot_date = pd.to_datetime(snapshot_date)
        records = holdingRecord.objects.filter(date_held=snapshot_date).all()
        if len(records) == 0:
            return False
        return True

    ############################################################################
    ### Retrieve data for funds stored in database
    def loadFunds(self,request):

        funds = Fund.objects.all()
        output_data = []
        for fund in funds:
            subdata = {}
            subdata['id'] = str(fund.id)
            subdata['fund_name'] = str(fund.name)
            subdata['fund_description'] = str(fund.description)
            output_data.append(subdata)

        final_data = json.dumps({'funds': output_data})
        return HttpResponse(final_data)

    ############################################################################
    ### Retrieve data for portfolios stored in database
    def loadPortfolios(self,request):

        portfolios = Portfolio.objects.all()
        output_data = []
        for portfolio in portfolios:
            subdata = {}
            subdata['id'] = portfolio.id
            subdata['portfolio_name'] = portfolio.portfolio_name
            subdata['strategy'] = portfolio.strategy
            subdata['portfolio_description'] = portfolio.portfolio_description
            subdata['fund_id'] = portfolio.fund_id
            subdata['fund_name'] = portfolio.fund_name

            output_data.append(subdata)

        final_data = json.dumps({'portfolios': output_data})
        return HttpResponse(final_data)

