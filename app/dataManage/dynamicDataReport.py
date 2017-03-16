from app.fields.fields import Fields
from app.lib.csvUtilities import csvResponse
from app.settings import MissingDataReportSettings


###################################################################
class MissingDynamicDataReport(csvResponse, MissingDataReportSettings):

    reportName = 'MissingDynamicDataReport'
    ### Initialize a missing dynamic data report from a list of securities, the missing
    ### data records are accessible from each security.
    def __init__(self, portfolio, portfolios=None):

        self.proxyHelper = {'proxy_rcg_id': 'rcg_id', 'proxy_security_name': 'security_name',
                            'underlying_rcg_id': 'rcg_id', 'proxy_search_name': 'search_name', }

        MissingDataReportSettings.__init__(self)
        csvResponse.__init__(self)

        self.includedDateIDPairs = {}

        self.headers = self.missingDynamicDataReportHeaders
        self.portfolio = portfolio
        self.portfolios = portfolios

        self.loopPortfolios = []
        self.securities = []

        if self.portfolios != None:
            self.combinePortfolios()
            self.loopPortfolios = self.portfolios
        else:
            self.securities = self.portfolio.securities
            self.loopPortfolios = [self.portfolio]

        return

    #########################
    ### Generates a list of field objects that are exhaustive, for securities who could not
    ### be classified.
    def generateAllPossibleFields(self):
        fieldObj = Fields()
        applicableFields = []
        for fieldType in fieldObj.dynamicFieldList:
            if fieldType.bbFieldName != None:
                applicableFields.append(fieldType)
        return applicableFields

    #########################
    def combinePortfolios(self):

        for portfolio in self.portfolios:
            for security in portfolio.securities:

                if portfolio.snapshot_date not in self.includedDateIDPairs.keys():
                    self.includedDateIDPairs[portfolio.snapshot_date] = []

                if security.rcg_id not in self.includedDateIDPairs[portfolio.snapshot_date]:
                    self.includedDateIDPairs[portfolio.snapshot_date].append(security.rcg_id)
                    self.securities.append(security)
        return

    #####################################
    ### Includes Missing Static Models in Report by Noting All Possible Dynamic Fields
    def includeMissingStaticModels(self):

        seenMissingSecurities = []  ### Track so no duplications noted

        ### Loop over all holding models correspondign to missing static models
        for portfolio in self.loopPortfolios:
            ### Loop over all holding models correspondign to missing static models
            for key in portfolio.missingStaticModels.keys():

                ### Retrieve Holding Model Associated with the Missing Static Model
                holdingModel = portfolio.missingStaticModels[key]
                rcg_id = holdingModel.rcg_id
                if rcg_id != None:
                    rcg_id = str(rcg_id)

                ## Only add valid unseen holding models to the data report
                if rcg_id != None and rcg_id not in seenMissingSecurities:
                    ### Get all of the possible applicable static fields that we might want for a missing security
                    allApplicableFields = self.generateAllPossibleFields()
                    for field in allApplicableFields:
                        row = self.createRowFromHoldingModel(field, holdingModel)
                        self.data.append(row)

                    seenMissingSecurities.append(rcg_id)
        return

    ######################################
    ### Creates a Single Row of DataFrame from the Security Model
    def createRowFromSecurity(self, field, security):
        ### Create Row
        date = security.snapshot_date.strftime("%Y-%m-%d")
        row = [date,str(security.rcg_id)]
        for fieldName in self.desiredFieldsForReport_Dynamic[2:]:
            
            ### Get Associated Field Object
            fieldObj = security.findField(fieldName)
            row.append(fieldObj.value)
            
        row.append(field.bbFieldName)
        return row

    ######################################
    ### Creates a Single Row of DataFrame from  Static Model and Field Name
    def createRowFromDynamicModel(self, field, dynamicModel):
        ### Create Row
        date = dynamicModel.date.strftime("%Y-%m-%d")
        row = [date,str(dynamicModel.rcg_id)]
        
        for fieldName in self.desiredFieldsForReport_Dynamic[2:]:
            attr = getattr(dynamicModel, fieldName)
            row.append(attr)
        row.append(field.bbFieldName)
        return row

    ######################################
    ### Creates a Single Row of DataFrame from Holding Model and Field Name
    def createRowFromHoldingModel(self, field, holdingModel):

        skipVals = ['proxy', 'underlying', 'search_name', 'instrument_type']
        ### Create Row
        date = holdingModel.date_held.strftime("%Y-%m-%d")
        row = [date,str(holdingModel.rcg_id)]
        
        row.append(holdingModel.date_held)
        for fieldName in self.desiredFieldsForReport_Dynamic[2:]:
            ### Have to ignore the proxy and underlying fields since rows are created from holding models
            ### before they have static model associated with them.
            validHoldingField = True
            for skipVal in skipVals:
                if skipVal in fieldName.lower():
                    validHoldingField = False
                    attr = ""
            
            if validHoldingField:
                attr = getattr(holdingModel, fieldName)
            else:
                attr = ""
            row.append(attr)

        row.append(field.bbFieldName)
        return row

    ######################################
    ### Loops over securities and checks if the security has any dataRecords, then for each dataRecord in the seecurity
    ### the function will create a row for the report based on the field associated with the record and the security
    ### associated with the record.
    def generate(self):

        self.data = []
        for security in self.securities:
            dataRecords = security.missingDataRecords
            for record in dataRecords:

                ### Only include static fields that are aapplicable to bloomberg.
                if record.dynamic and record.field.bbFieldName != None:
                    row = self.createRowFromSecurity(record.field, record.security)
                    self.data.append(row)

        ### Include data for completely missing static models
        self.includeMissingStaticModels()

        ### Generate CSV Response
        response = self.createCSVResponse()
        return response




