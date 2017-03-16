from app.fields.allFields.static.allStaticFields import  InstrumentType
from app.fields.fields import Fields
from app.lib.csvUtilities import csvResponse
from app.settings import MissingDataReportSettings

###################################################################
class MissingStaticDataReport(csvResponse, MissingDataReportSettings):
    reportName = 'MissingStaticDataReport'

    ### Initialize a missing static data report from a list of securities, the missing
    ### data records are accessible from each security.
    def __init__(self, portfolio, portfolios=None):

        MissingDataReportSettings.__init__(self)
        csvResponse.__init__(self)

        self.headers = self.missingStaticDataReportHeaders
        self.portfolio = portfolio
        self.portfolios = portfolios

        self.loopPortfolios = []
        self.includedRecords = []  ### Used to track records
        self.securities = []

        if self.portfolios != None:
            self.combinePortfolios()
            self.loopPortfolios = self.portfolios
        else:
            self.securities = self.portfolio.securities
            self.loopPortfolios = [self.portfolio]
        return
    
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
                if record.static and record.field.bbFieldName != None:
                    row = self.createRowFromSecurity(record.field, record.security)
                    self.data.append(row)

        ### Include data for completely missing static models
        self.includeMissingStaticModels()
        ## Include data for securities missing an instrument type and thus cannot be classified.
        self.includeMissingInstrumentTypes()
        
        ### Generate CSV Response
        response = self.createCSVResponse()
        return response
        
    #########################
    ### Generates a list of field objects that are exhaustive, for securities who could not
    ### be classified - Non instance field objects, they have not been initialized to security yet.
    def generateAllPossibleFields(self):
        
        fieldObjects = Fields.staticFieldObjects
        fieldObj = Fields()
        applicableFields = []
        for fieldObj in fieldObjects:
            if fieldObj.static and fieldObj.bbFieldName != None:
                applicableFields.append(fieldObj)

        ### Manually Include Instrument Type Since its Not a Standard BB Field
        applicableFields.append(InstrumentType)
        return applicableFields
    
    #########################
    def combinePortfolios(self):

        for portfolio in self.portfolios:
            for security in portfolio.securities:
                if security.rcg_id not in [sec.rcg_id for sec in self.securities]:
                    self.securities.append(security)
        return
    
    #####################################
    ## Includes securities missing instrument types
    def includeMissingInstrumentTypes(self):
        
        seenMissingInstrumentTypes = []  ### Track so no duplications noted

        ### Loop over all holding models correspondign to missing static models
        for portfolio in self.loopPortfolios:
            ### Loop over all static models correspondign to missing instrument types
            for key in portfolio.missingInstrumentTypes.keys():
                
                staticModel = portfolio.missingInstrumentTypes[key]
                rcg_id = staticModel.rcg_id
                if rcg_id != None:
                    rcg_id = str(rcg_id)
                
                ## Only add valid unseen holding models to the data report
                if rcg_id != None and rcg_id not in seenMissingInstrumentTypes:
                    ### Get all of the possible applicable static fields that we might want for a missing security
                    allApplicableFields = self.generateAllPossibleFields()
                    for field in allApplicableFields:
                        
                        modelName = field.modelFieldName
                        attrVal = getattr(staticModel,modelName)
                        if attrVal == None:
                            
                            row = self.createRowFromStaticModel(field, staticModel)
                            self.data.append(row)

                    seenMissingInstrumentTypes.append(rcg_id)
        return
        
    #####################################
    ### Includes Missing Static Models in Report by Noting All Possible Static Fields
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
    def createRowFromSecurity(self,field,security):
        ### Create Row
        row = [security.rcg_id]
        for fieldName in self.desiredFieldsForReport_Static[1:]:
            ### Get Associated Field Object
            fieldObj = security.findField(fieldName)
            row.append(fieldObj.value)
        row.append(field.bbFieldName)
        return row

    ######################################
    ### Creates a Single Row of DataFrame from  Static Model and Field Name
    def createRowFromStaticModel(self, field, staticModel):
        ### Create Row
        row = [staticModel.rcg_id]
        for fieldName in self.desiredFieldsForReport_Static[1:]:
            attr = getattr(staticModel,fieldName)
            row.append(attr)
        row.append(field.bbFieldName)
        return row

    ######################################
    ### Creates a Single Row of DataFrame from Holding Model and Field Name
    def createRowFromHoldingModel(self,field,holdingModel):

        skipVals = ['proxy','underlying','search_name','instrument_type']
        ### Create Row
        row = []
        for fieldName in self.desiredFieldsForReport_Static:
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

    
