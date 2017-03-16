import json

import pandas as pd
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

from app.connections import Connection
from app.dataManage.missingSecurities import MissingSecurities
from app.directoryUtilities import exportDF
from app.lib.safeRead import safeReadString, safeReadFloat, safeReadBool, safeReadInt
from app.models.models import holdingRecord, staticRecord
from app.settings import settings
from app.views.dataUpdateBase import DataUpdate
from app.fields.standardization.standardize import Standardize

########################################################################
class HoldingsUpdateView(View,Connection,DataUpdate):

    def __init__(self):

        Connection.__init__(self)
        DataUpdate.__init__(self)

        self.portfolios = []
        self.missingSecurityResponse = {}

        self.portIDMappings = settings.port_id_mapping
        self.portNameMapping = settings.port_name_mapping
        self.assetClassMapping = settings.asset_class_mapping
        return

    #### Directs the process of the view based on the request data
    def get(self, request):

        self.startDate = str(request.GET['startDate'])
        self.endDate = str(request.GET['endDate'])
        self.singleDate = str(request.GET['singleDate'])

        self.refreshType = str(request.GET['refreshType'])

        ### Update the holdings depending on the update type
        if self.refreshType != 'single_date' and self.refreshType != 'between_dates':
            return HttpResponseNotFound("<h1>Error with Date Formatting</h1>")


        ### Prepare if Needed - Send Respond Message on Error
        if not self.prepared:
            self.prepare()
            if self.error:
                return HttpResponse(self.responseMessage)

        ### Pull Data From Transparency
        self.generateLoopDates()
        self.enterTransparencySession()

        ### Update Rows for Each Day Iteratively
        responseMessage = ""
        for date in self.unique_dates:
            rows = self.retrieveFromTransparency(date)
            if len(rows)==0:
                responseMessage += "No Holdings on Date : " + date.strftime("%Y-%m-%d") + '\n'
            else:
                responseMessage += self.update(date,rows)

        self.leaveTransparencySession()
        response = json.dumps({'responseMessage': responseMessage})
        return HttpResponse(response)

    ### Initializes a static record from a holding record if the static record does not exist yet.
    def createStaticRecordFromHolding(self,holdingRecord):

        static_record = staticRecord()
        static_record.rcg_id = holdingRecord.rcg_id
        
        ### Don't want to update security name for models, just want to have the 
        ### Security name establish for the first static model created
        static_record.security_name = holdingRecord.sec_name
        static_record.ss_asset_class = holdingRecord.ss_asset_class
        static_record.id_cusip = holdingRecord.ssid
        static_record.id_isin = holdingRecord.isin
        static_record.id_sedol1 = holdingRecord.sdl

        static_record.save()

        return

    #### Pulls data from transparency and updates holdings internally to application - updates the rows in database
    ### for a single day
    def update(self,date,updateRows):

        ### Delete Holdings Data for Date That is Already Present
        holdingRecord.objects.filter(date_held=date).delete()
        holdingModelsToArchive = []

        ### Get Static Records to Tell if New Record Should be Initiated from Holding Record
        static_records = staticRecord.objects.all()
        static_ids = [model.rcg_id for model in static_records]

        responseMessage = ""

        #### Filter Through Holdings Records ###############
        count = 0
        for row in updateRows:

            print 'Updating Holding on : ',date.strftime("%Y-%m-%d"),' Number : ', count
            count += 1

            ### Only Keep SS Portfolio Holdings
            ssportid = str(row[2])
            if ssportid not in self.portIDMappings.keys():
                continue

            ssid = str(row[1])
            rcg_id = 'RCG' + ssid
            date_held = pd.to_datetime(row[0])

            ### Initialize New Holding Record
            holding_record = holdingRecord(rcg_id=rcg_id, date_held=date_held)

            #### Attribute Data to Holding Record
            holding_record.ssid = ssid
            holding_record.sec_name = str(row[3])
            holding_record.ss_portfolio_id = str(row[2])
            holding_record.rcg_portfolio_id = str(self.portIDMappings[holding_record.ss_portfolio_id])
            holding_record.port_name = str(self.portNameMapping[int(holding_record.rcg_portfolio_id)])

            holding_record.ss_asset_class = str(self.assetClassMapping[str(row[8])])
            holding_record.sdl = str(row[10])
            holding_record.isin = str(row[9])

            holding_record.date_held = pd.to_datetime(row[0])

            holding_record.position = str(row[4])
            holding_record.quantity = float(row[5])
            holding_record.market_val = float(row[6])
            holding_record.price = float(row[7])
            holding_record.unrealized_gains_losses = float(row[11])
            
            holding_record.save()
            holdingModelsToArchive.append(holding_record)  ### For Archive Holding Files
            
            ### Standardize Holding Record Before Proceeding to Initialize a Separate Static Model               
            standardized_holding_record = Standardize.standardizeHoldingModel(holding_record)
            
            ### Determine if Static Record Needs to be Initialized
            if standardized_holding_record.rcg_id not in static_ids:
                self.createStaticRecordFromHolding(standardized_holding_record)
                responseMessage += "New Security, Static Record Initialized : " + str(holding_record.rcg_id) + '\n'


            count += 1
        responseMessage += "Holdings Successfully Updated : " + date.strftime("%Y-%m-%d") + '\n'

        ### Archive Holding Files
        print 'Archiving Holding Models on  : ', date
        self.archive(date, holdingModelsToArchive)

        return responseMessage


    ### Gets the holdings from the transparency database so they can be stored for this application
    def retrieveFromTransparency(self,date):

        query = """SELECT CAST(AsOfDate AS DATE), CUSIP, SSFundId, SecurityLongName, PositionTypeCode, Quantity,
                                             MarketValue, Price, AssetClassCode, ISIN, SEDOL, PL
                                FROM Research.dbo.SSDailySummaryLevelHoldings
                                WHERE CAST(AsOfDate AS DATE)  = '%s'
                                """ % date

        rows = self.engine.execute(query).fetchall()
        return rows


    ### Archives Holding Data on Date
    def archive(self, date, holdingModels):

        holding_type_dict = settings.holding_type_dict
        dateString = date.strftime("%m-%d-%Y")
        outputData = []

        for holding in holdingModels:
            row = []
            ### Safely Retrieve Data for Each Row
            for colname in settings.holding_headers:
                if colname in holding_type_dict.keys():

                    if holding_type_dict[colname] == 'float':
                        entry = safeReadFloat(colname, model=holding)
                    elif holding_type_dict[colname] == 'int':
                        entry = safeReadInt(colname, model=holding)
                    elif holding_type_dict[colname] == 'bool':
                        entry = safeReadBool(colname, model=holding)
                    else:
                        entry = safeReadString(colname, model=holding)
                else:
                    entry = safeReadString(colname, model=holding)

                if entry != None:
                    row.append(entry)
                else:
                    row.append("")

            outputData.append(row)
        outputData = pd.DataFrame(outputData)
        outputData.columns = settings.holding_headers

        outputFileName = "HoldingsFile_" + dateString + '.csv'
        exportDF(outputData, outputFileName, 'data', 'holdings_archive')
        return

    #### Includes missing securities in the response for populating the security HTML Field
    def getMissingSecurities(self):

        missingSecurityData = {}

        missingSecurities = MissingSecurities()
        if self.refreshType == 'single_date':
            ### Find Missing Securities On Date
            missingSecurities.find(date=self.singleDate, start_date=None, end_date=None)
            missingSecurityData = missingSecurities.format()

        elif self.refreshType == 'between_dates':
            ### Find Missing Securities Between Dates
            missingSecurities.find(date=None,start_date=self.startDate,end_date=self.endDate)
            missingSecurityData = missingSecurities.format()

        return missingSecurityData
