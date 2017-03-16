import threading
import datetime as dt
from app.models.models import staticRecord, holdingRecord, dynamicRecord
from app.settings import settings

#################################################################
class fetchHoldingsThread(threading.Thread):
    
    def __init__(self,portfolio):
        threading.Thread.__init__(self)
        self.portfolio = portfolio
        self.models = None
    ###################################
    ### Query for Securities in Holdings - Determine Which Ones Need Proxy ###
    def run(self):
        self.models = holdingRecord.objects.filter(rcg_portfolio_id = self.portfolio.portfolio_id,date_held=self.portfolio.snapshot_date).all()

#################################################################
class fetchStaticThread(threading.Thread):
    
    def __init__(self,portfolio):
        threading.Thread.__init__(self)
        self.portfolio = portfolio
        self.models = None
    ###################################
    ### Query for Securities in Holdings - Determine Which Ones Need Proxy ###
    def run(self):
        self.models = staticRecord.objects.all()

#################################################################
class fetchDynamicThread(threading.Thread):
    
    def __init__(self,portfolio):
        threading.Thread.__init__(self)

        self.dynamicDateRange = []
        self.portfolio = portfolio
        self.models = None

    ### Returns list of unique dates starting at snapshot and moving backwards
    def generateUniqueDates(self):

        lookback = settings.maximumLookbackDays

        ### Get Unique Dates Between Start and End Date
        self.dynamicDateRange = []
        for i in range(lookback):
            prevDate = self.portfolio.snapshot_date - dt.timedelta(days=i)
            self.dynamicDateRange.append(prevDate)

        return

    #####################
    ### Query for All Needed Historical Data
    def run(self):

        ### Get most recent days of dynamic data
        if self.portfolio.restrictToSnapshot:
            self.models = dynamicRecord.objects.filter(date =self.portfolio.snapshot_date,measurement_type__in=self.portfolio.desired_measurements).all()
        else:
            self.generateUniqueDates()
            self.models = dynamicRecord.objects.filter(date__in = self.dynamicDateRange,measurement_type__in=self.portfolio.desired_measurements).all()
