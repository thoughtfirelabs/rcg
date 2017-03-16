import sys
sys.dont_write_bytecode = True
import json

from django.http import HttpResponse
from django.views.generic import View

from app.models.models import Portfolio
from app.modules.portfolio_module import portfolio

from app.dataManage.staticDataReport import MissingStaticDataReport
from app.dataManage.dynamicDataReport import MissingDynamicDataReport

from app.views.dataUpdateBase import DataUpdate
########################################################################
class DataReportView(View,DataUpdate):

    def __init__(self):
        self.fund_id = None
        DataUpdate.__init__(self)
        self.portfolios = []
        return

    #####################################################
    #### Directs the process of the view based on the request data
    def get(self,request):

        self.fund_id = 'LGWXBOK7'  ## Hardcoded for Now
        self.startDate = str(request.GET['startDate'])
        self.endDate = str(request.GET['endDate'])
        self.singleDate = str(request.GET['singleDate'])

        self.dataType = str(request.GET['dataType'])
        self.refreshType = str(request.GET['refreshType'])

        ### Prepare if Needed - Send Respond Message on Error
        if not self.prepared:
            self.prepare()
            if self.error:
                return HttpResponse(json.dumps({'error':self.responseMessage}))

        self.generatePortfolios()
        if len(self.portfolios) == 0:
            self.responseMessage = 'Error : Invalid Dates Over Which to Generate Data - Dates probably include weekend or holidays only'
            return HttpResponse(json.dumps({'error': self.responseMessage}))

        ### Initialize Data Report Object
        if self.dataType.lower() == 'static':
            staticDataReport = MissingStaticDataReport(None, portfolios=self.portfolios)
            response = staticDataReport.generate()
        else:
            dynamicDataReport = MissingDynamicDataReport(None, portfolios=self.portfolios)
            response = dynamicDataReport.generate()
        return response

    #############################################
    ### Generates Portfolios for Data Reports
    def generatePortfolios(self):

        loopdates = [self.singleDate]
        if self.rangeUpdate:
            loopdates = self.unique_dates

        models = Portfolio.objects.filter(fund_id=self.fund_id).all()
        portfolio_ids = [model.id for model in models]

        ### Store Portfolios to Generate Data Report From
        self.portfolios = []
        for date in loopdates:
            for port_id in portfolio_ids:
                p = portfolio(port_id, date)
                ### Restrict portfolio data to single day (don't use backtest data for estimation)
                p.restrictToSnapshot = True
                p.categorizationRequired = False

                p.run()

                ### Make Sure Date Valid (i.e. Not Weekend)
                if p.date_error:
                    print 'Invalid Date : ', self.singleDate, ' -> Probably Weekend - '
                    continue

                self.portfolios.append(p)
        return

