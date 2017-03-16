import sys
sys.dont_write_bytecode = True

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

from app.lib.excelSafeRead import excelBoolSafeLoad, excelStringSafeLoad
import json

from app.connections import Connection
from app.settings import settings
from app.models.models import  staticRecord

from app.views.dataUpdateBase import DataUpdate
from app.fields.fields import Fields

from app.directoryUtilities import importDF
from app.lib.safeRead import safeReadString
from app.lib.errorLog import ErrorLog
from app.lib.csvUtilities import csvResponse
from app.fields.standardization.standardize import Standardize

### Represents the CSV Downloadable Static Master File
class StaticMasterTable(csvResponse):

    def __init__(self):

        self.reportName = 'StaticMaster'
        self.headers = settings.staticMasterHeaders
        self.data = []

        csvResponse.__init__(self)
        return

    ### Get static models and create the table, then create
    ### downloadable response
    def generate(self):

        current_static_models = staticRecord.objects.all()
        if len(current_static_models) == 0:
            print "No Currently Stored Static Data"
            return

        for staticModel in current_static_models:
            row = []
            for field in settings.staticMasterHeaders:
                data = safeReadString(field, model=staticModel)
                if data != None:
                    row.append(data)
                else:
                    row.append('')

            self.data.append(row)

        response = self.createCSVResponse()
        return response


########################################################################
class StaticUpdateView(View,Connection,DataUpdate):

    def __init__(self):

        Connection.__init__(self)
        DataUpdate.__init__(self)

        self.portfolios = []
        self.missingSecurityResponse = {}
        self.command = None

        self.portIDMappings = settings.port_id_mapping
        self.portNameMapping = settings.port_name_mapping
        self.assetClassMapping = settings.asset_class_mapping

        self.errors = ErrorLog()
        return

    #### Directs the process of the view based on the request data
    def get(self, request):

        ### Don't need to verify user here becuase user would not have been able to access this page
        ### if they were not an administrator.
        self.command = str(request.GET['command'])
        if self.command == 'update':
            response = self.update()
            return response
        elif self.command == 'download':
            response = self.download()
            return response
        else:
            return HttpResponseNotFound("<h1>Invalid Command</h1>")

        return response

    #### Reads CSV file for updating static data and stores updated data to securities in static master database
    #### on transparency.
    def update(self):

        static_update_data = importDF('static_update', 'data', subdirPath='update_data')
        static_update_data = static_update_data.fillna('')

        count = 0
        ############ Loop Over Securities and Add Data to Dictionary #############
        for i in range(len(static_update_data.index)):
            row = static_update_data.iloc[i, :]
            
            #### Safeload RCG ID ##########################
            rcg_id = excelStringSafeLoad(row, 'rcg_id')
            if rcg_id == None:
                self.errors.add('Found Invalid Format for ID at Row : '+str(i)+' -> Removed from Update')
                continue

            updateString = "Security : " + rcg_id + "... " + str(count) + "/" + str(len(static_update_data.index))
            print updateString

            ### If Not a Valid Update - Still Want to Update Search Name or Proxy Information

            ### Check if Record Exists in Database Already
            static_record = staticRecord.objects.filter(rcg_id = rcg_id).first()
            if static_record == None:
                static_record = staticRecord()  ### Initialize
                static_record.rcg_id = rcg_id
            
            
            ###  Determine Field to Update
            missing_field = excelStringSafeLoad(row, 'missing_field')
            if missing_field == None:
                self.errors.add('Missing or Invalid Field Name at Row : ' + str(i) + ' -> Removed from Update')
                continue
            
             ### Temporary - To replace the proxy or underlying situation in the front end
            ### and make proxies / underlyings addable from the data reports.
            if missing_field.lower() == 'proxy':
                missingValue = excelStringSafeLoad(row,'missing_value')
                if missingValue != None:
                    static_record.underlying_rcg_id = missingValue
                    static_record.save()
                    continue
                
                
                
            ### Get Field Obj Associated with Missing Field
            fieldObj = Fields.findStaticFieldObject(missing_field)
            if fieldObj == None:
                self.errors.add('Invalid Field Name : ' + str(missing_field) + ' at Row : '+str(i))
                continue

            ### Value will only be stored to record if it is valid
            internalFieldName = fieldObj.modelFieldName
            if internalFieldName == None:
                self.errors.add('No Model Field for  : ' + str(fieldObj.internalFieldName))
                continue
            
            
            missingValue = excelStringSafeLoad(row,'missing_value')
            if missingValue != None:
                setattr(static_record,internalFieldName,missingValue)

                ### Update Ticker
                searchName = excelStringSafeLoad(row,'search_name')
                if searchName != None:
                    static_record.search_name = searchName

                print '   ->  Adding Static Record'
                static_record = Standardize.standardizeStaticModel(static_record)
                static_record.save()
            
            count += 1
        
        self.errors.noteSuccess('Static Update Successful with : '+str(self.errors.numErrors)+' Errors')
        responseData = self.errors.createResponseJson()
        responseData = json.dumps({'response':responseData})
        
        return HttpResponse(responseData)

    #############################################################
    ### Outputs Static Master as CSV in Table Format to Downloads
    def download(self):
        table = StaticMasterTable()
        response = table.generate()
        return response
