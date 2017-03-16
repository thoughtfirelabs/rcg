import datetime as dt

import pandas as pd

from app.models.models import staticRecord, holdingRecord
from app.dataManage.missingSecurity import MissingSecurity
from app.fields.standardization.standardize import Standardize

class MissingSecurities:

    ## include_proxy_underlying Specifies Whether or Not to Include References to Missng Proxies/Underlyings
    def __init__(self,include_proxy_underlying=False):
        self.include_proxy_underlying = include_proxy_underlying
        self.missingSecurities = []
        return

    ### Generates Missing Security Piece for A Single Holding Model by lookign at whether or not it is
    ### completely missing from static database.
    @staticmethod
    def generateFromHoldingModel(holdingModel):

        missingSecurities = []

        allStaticModels = staticRecord.objects.all()

        completelyMissing = MissingSecurity.isCompletelyMissing(holdingModel.rcg_id,allStaticModels)
        if completelyMissing:
            missingSec = MissingSecurity(str(holdingModel.rcg_id))
            missingSec.storeDataFromHolding(holdingModel)

            if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                missingSecurities.append(missingSec)


        ### If not completely missing, check if the static record is missing fatal information.
        else:
            staticModel = staticRecord.objects.filter(rcg_id = holdingModel.rcg_id).first()
            if MissingSecurity.isMissingData(staticModel):

                missingSec = MissingSecurity(str(holdingModel.rcg_id))
                missingSec.storeDataFromHolding(holdingModel)

                if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                    missingSecurities.append(missingSec)

        return missingSecurities

    ### Generates Missing Security Piece for A Single Static Model (Base, Underlying and Proxy)
    ### This is always at least stage 2, since we are already looking through the seen records in the
    ### static database, so stage 1 doesn't apply.
    @staticmethod
    def generateFromStaticModel(staticModel,include_proxies_underlying):

        missingSecurities = []
        baseMissingData = False
        foundSearchName = False ### Used to determine if search name supplied by proxy, underlying or base
                                ### If none of the 3 have the search name, it will be flagged.
        allStaticModels = staticRecord.objects.all()
        if staticModel.search_name != None:
            foundSearchName = True

        ### Is completely missing will never be flagged here since we are already generating
        ### the missing securities from a seen static model.

        ### Base Security Missing Data
        missingData = MissingSecurity.isMissingData(staticModel)
        if missingData:
            missingSec = MissingSecurity(str(staticModel.rcg_id))
            missingSec.storeDataFromStatic(staticModel)

            if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                missingSecurities.append(missingSec)

            baseMissingData = True

        if include_proxies_underlying:
            ### Proxy Security Missing or Missing Data
            if staticModel.proxy_rcg_id != None:

                ### Check if Proxy Missing Data or Proxy Not Even Present
                proxyMissing = MissingSecurity.isCompletelyMissing(staticModel.proxy_rcg_id,allStaticModels)
                if proxyMissing:
                    missingSec = MissingSecurity(staticModel.proxy_rcg_id)

                    if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                        missingSecurities.append(missingSec)

                ### Check if Proxy Missing Vital Data
                else:
                    proxyStaticModel = staticRecord.objects.filter(rcg_id=str(staticModel.proxy_rcg_id)).first()
                    proxyMissingData = MissingSecurity.isMissingData(proxyStaticModel)
                    if proxyMissingData:
                        missingSec = MissingSecurity(staticModel.proxy_rcg_id)
                        missingSec.storeDataFromStatic(proxyStaticModel)

                        if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                            missingSecurities.append(missingSec)

                    if proxyStaticModel.search_name != None:
                        foundSearchName = True

            ### Underlying Security Missing or Missing Data
            if staticModel.underlying_rcg_id != None:

                ### Check if Proxy Missing Data or Proxy Not Even Present
                underlyingMissing = MissingSecurity.isCompletelyMissing(staticModel.underlying_rcg_id,allStaticModels)
                if underlyingMissing:
                    missingSec = MissingSecurity(staticModel.underlying_rcg_id)

                    if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                        missingSecurities.append(missingSec)

                ### Check if Proxy Missing Vital Data
                else:
                    underlyingStaticModel = staticRecord.objects.filter(rcg_id=str(staticModel.underlying_rcg_id)).first()
                    underlyingMissingData = MissingSecurity.isMissingData(underlyingStaticModel)
                    if underlyingMissingData:
                        missingSec = MissingSecurity(staticModel.underlying_rcg_id)
                        missingSec.storeDataFromStatic(underlyingStaticModel)

                        if missingSec.rcg_id not in [model.rcg_id for model in missingSecurities]:
                            missingSecurities.append(missingSec)

                    if underlyingStaticModel.search_name != None:
                        foundSearchName = True

            ### Check if any of the models had a search name that can be used
            ### If not, check if the base security was already noted for missing data and if it wasn't, add it since
            ### it is missing a search name that is not supplemented by a proxy or underyling.
            if not foundSearchName and not baseMissingData:
                missingSec = MissingSecurity(str(staticModel.rcg_id))
                missingSec.storeDataFromStatic(staticModel)
                missingSecurities.append(missingSec)

        return missingSecurities


    ### Finds missing security data by looking at all securities in the static master, without regard
    ### as to whether or not they are currently being held.
    def findAll(self):

        self.missingSecurities = []
        staticModels = staticRecord.objects.all()
        
        for model in staticModels:
 
            ### Need to inform whether or not we want to include proxies and underlyings.
            missingSecurities = MissingSecurities.generateFromStaticModel(model,self.include_proxy_underlying)
            if len(missingSecurities) != 0:
                for sec in missingSecurities:
                    print sec.security_name
                    print sec.instrument_type
            self.missingSecurities.extend(missingSecurities)
        return

    ### Finds missing securities by comparing data in holding records to
    ### data in static records
    def findForHoldings(self,date=None,start_date = None, end_date = None):

        self.missingSecurities = []

        unique_dates = self.generateLoopDates(date=date, start_date=start_date, end_date=end_date)
        checkedIds = []
        for date in unique_dates:
            addholdingModels = holdingRecord.objects.filter(date_held=date).all()
            for holding in addholdingModels:
                
                ### Make Sure to Standardize First
                holding = Standardize.standardizeHoldingModel(holding)  

                if holding.rcg_id not in checkedIds:
                    checkedIds.append(holding.rcg_id)

                    missingSecurities = MissingSecurities.generateFromHoldingModel(holding)
                    self.missingSecurities.extend(missingSecurities)
        return

    ### Formats the data contained in the missing securities to a JSON format
    ### so that it can be used by the front end.
    def format(self):

        outputData = {}
        for missingSecurity in self.missingSecurities:

            recordData = dict()
            if missingSecurity.id_isin != None:
                recordData['isin'] = missingSecurity.id_isin

            if missingSecurity.security_name != None:
                recordData['securityName'] = missingSecurity.security_name

            if missingSecurity.instrument_type != None:
                recordData['instrument_type'] = missingSecurity.instrument_type

            if missingSecurity.search_name != None:
                recordData['search_name'] = missingSecurity.search_name

            if missingSecurity.proxy_rcg_id != None:
                recordData['proxy_rcg_id'] = missingSecurity.proxy_rcg_id

            if missingSecurity.underlying_rcg_id != None:
                recordData['underlying_rcg_id'] = missingSecurity.underlying_rcg_id

            outputData[missingSecurity.rcg_id] = recordData
        return outputData

    #### Uses the different passed in dates to generate a list of dates to loop over
    def generateLoopDates(self, date=None, start_date=None, end_date=None):

        rangeUpdate = False
        if date == None:
            if start_date != None and end_date != None:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                rangeUpdate = True
            else:
                print 'Date Range Error with Missing Securities'
                return
        else:
            date = pd.to_datetime(date)

        unique_dates = []
        if rangeUpdate:
            ### Get Unique Dates Between Start and End Date
            delta = end_date - start_date
            for i in range(delta.days + 1):
                nextDate = start_date + dt.timedelta(days=i)
                unique_dates.append(nextDate)
        else:
            unique_dates = [date]
        return unique_dates