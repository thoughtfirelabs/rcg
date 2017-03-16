import threading
from app.settings import settings
from app.models.models import staticRecord, holdingRecord, dynamicRecord
import datetime as dt

#################################################################
class fetchHoldingsThread(threading.Thread):
    
    def __init__(self,fund):
        threading.Thread.__init__(self)
        self.fund = fund
        self.models = None
    ###################################
    ### Query for Securities in Holdings - Determine Which Ones Need Proxy ###
    def run(self):
        portfolio_ids = list(self.fund.portfolios.keys())
        self.models = holdingRecord.objects.filter(rcg_portfolio_id__in = portfolio_ids,date_held=self.fund.snapshot_date).all()

#################################################################
class fetchStaticThread(threading.Thread):
    
    def __init__(self,fund):
        threading.Thread.__init__(self)
        self.fund = fund
        self.models = None
    ###################################
    ### Query for Securities in Holdings - Determine Which Ones Need Proxy ###
    def run(self):
        self.models = staticRecord.objects.all()

#################################################################
class fetchDynamicThread(threading.Thread):
    
    def __init__(self,fund):
        threading.Thread.__init__(self)
        self.fund = fund
        self.models = None
        self.dynamicDateRange = []

    ### Returns list of unique dates starting at snapshot and moving backwards
    def generateUniqueDates(self):
        lookback = settings.maximumLookbackDays

        ### Get Unique Dates Between Start and End Date
        self.dynamicDateRange = []
        for i in range(lookback):
            prevDate = self.fund.snapshot_date - dt.timedelta(days=i)
            self.dynamicDateRange.append(prevDate)

        return

    #####################
    ### Query for All Needed Historical Data
    def run(self):

        ### Get most recent days of dynamic data
        if self.fund.restrictToSnapshot:
            self.models = dynamicRecord.objects.filter(date=self.fund.snapshot_date,
                                                       measurement_type__in=self.fund.desired_measurements).all()
        else:
            self.generateUniqueDates()
            self.models = dynamicRecord.objects.filter(date__in=self.dynamicDateRange,
                                                       measurement_type__in=self.fund.desired_measurements).all()
