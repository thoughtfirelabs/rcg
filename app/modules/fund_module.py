from app.fields.standardization.standardize import Standardize
from app.models.models import Portfolio, Fund
from app.models.securityModels import RCG40Act

from fundThreads import fetchHoldingsThread, fetchStaticThread, fetchDynamicThread
from ..settings import settings

from multiprocessing import Process, Queue
import pandas as pd

from app.dataManage.frontEndDataReport import FrontEndDataReport

#############################################################
class SecurityModelManagement:
    def __init__(self):

        self.missingInstrumentTypes = {}  ### Stores dictionary of static models if instrument Types
        self.missingStaticModels = {}  ### Stores dictionary of holding models if static models are missing
        self.securityDataRecords = {}
        return

    ####################################
    ### When a security is missing a static model but there is a holding reference for it 
    ### the security cannot be validated on a per field basis but we must assume that all fields
    ### possible are missing since there is no notion of what type of security the holdingModel is for 
    ### or what data is missing (since there is none).  For the securities stored here, all of the possible
    ### data fields in the missing data report will be included.
    def invalidateMissingStaticModelforSecurity(self, holdingModel):
        rcg_id = holdingModel.rcg_id
        if rcg_id != None:
            rcg_id = str(rcg_id)
            if rcg_id not in self.missingStaticModels.keys():
                self.missingStaticModels[rcg_id] = holdingModel
        else:
            print 'Error Invalidating Missing Static Model for Security : RCGID = None'
        return

    ####################################
    ### When a security has a static model but has an invalid instrument type this function will 
    ### note that.
    def invalidateSecurityInstrumentType(self, staticModel):
        rcg_id = staticModel.rcg_id
        if rcg_id != None:
            rcg_id = str(rcg_id)
            if rcg_id not in self.missingInstrumentTypes.keys():
                self.missingInstrumentTypes[rcg_id] = staticModel
        else:
            print 'Error Invalidating Missing Instrument Type for Security : RCGID = None'

    ############################################
    def createFrontEndErrorReportDetails(self):

        ### Creates Front End Data Report
        dataReport = FrontEndDataReport(self)
        error_report_details = dataReport.generate()
        return error_report_details


####################################################################
## Represents a Snapshot in Time of a Portfolio
class fund(SecurityModelManagement):
    def __init__(self, fund_id, snapshot_date):

        if type(fund_id) is int:
            fund_id = str(fund_id)

        self.snapshot_date = snapshot_date

        if type(self.snapshot_date) is unicode:
            self.snapshot_date = str(self.snapshot_date)
            self.snapshot_date = pd.to_datetime(self.snapshot_date)

        if type(self.snapshot_date) is str:
            self.snapshot_date = pd.to_datetime(self.snapshot_date)

        ### Makes sure that portfolio only uses dynamic data for the snapshot day and no previous days
        ### (Used for missing data reporting).
        self.restrictToSnapshot = True
        self.categorization = None ### Used to cateogorize securities
        
        ### Date Error Referenced When Date Not Available in Holdings File
        self.date_error = False
        self.calculation_needed = True

        self.fund_id = fund_id
        self.fund_name = None
        self.snapshot_date = snapshot_date

        SecurityModelManagement.__init__(self)

        ### Create a New Instance of the Scoped Session
        self.holdingThread = fetchHoldingsThread(self)
        self.staticThread = fetchStaticThread(self)
        self.dynamicThread = fetchDynamicThread(self)
        self.threads = [self.holdingThread, self.staticThread, self.dynamicThread]

        ##############################################
        ### Getting Description of Fund
        model = Fund.objects.filter(id=self.fund_id).all()[0]
        self.fund_name = str(model.name)
        self.description = str(model.description)

        ##############################################
        ### Security Level Data
        self.securities = []

        self.needed_proxy_ids = {}
        self.desired_measurements = settings.dynamicFieldsToRetrieve

        ##############################################
        ### Portfolio Level Data
        self.beta_msci = 0.0
        self.revised_beta_msci = 0.0
        self.beta_sp500 = 0.0
        self.vol = 0.0

        self.delta_notional_exposure_gross = 0
        self.delta_notional_exposure_short = 0
        self.delta_notional_exposure_long = 0
        self.delta_notional_exposure_net = 0

        self.custom_notional_exposure_long = 0
        self.custom_notional_exposure_short = 0
        self.custom_notional_exposure_gross = 0
        self.custom_notional_exposure_net = 0

        self.market_val = 0
        self.wf_cash = 0.0  ### WFA Cash Holdings
        self.num_positions = 0

        self.earliestDateOfDynamicData = None
        self.dynamicDateRange = []

        self.holdingModels = []
        self.staticModels = []
        self.dynamicModels = []

        ##############################################
        ## Miscellaneous Custom Exposures Needed for Reporting
        self.issuer_gross_custom_notional_exposures = {}
        self.security_name_gross_custom_notional_exposures = {}

        ### Portfolio Level Data #####
        self.portfolios = {}
        return

    ############### Data Collection and Default Calculations ################
    def run(self,categorization=None):
        self.get_portfolios()
        self.categorization = categorization
        self.get_dataWithThreads()
        return

    ###############################################################################################
    ## For some reporting schemes, the 40 Act Fund needs to be included as a manager, so this function
    ## will include the RCG 40 Act Manager / Security in the fund.  Only include after analysis is done
    ## with fund.
    def includeRCG40Act(self):
        
        fakePortfolio = Portfolio() ### Initialize as placeholder for initialization
        fakePortfolio.id = 'RCG40Act'
        fakePortfolio.portfolio_name = 'Rock Creek 40 Act Sub-Adviser'
        fakePortfolio.strategy = 'Rock Creek Group'

        newSecurity = RCG40Act('RCG40Act',self.snapshot_date,fakePortfolio)
        newSecurity.PositionDesignation.value = 'L'
        newSecurity.evaluate()  ## Evaluation performed by indidivudal security models
        self.num_positions += 1
        self.securities.append(newSecurity)
        
        self.portfolios[str(fakePortfolio.id)]=fakePortfolio
        
        ### Perform General Calculations Based on Position
        self.market_val += newSecurity.market_val
        if self.categorization != None:
            self.categorization.addSecurity(newSecurity)       
        return

    ###############################################################################################
    ### In the Case of Being Treated Like Fund - Gets Portfolios Associated with Fund
    def get_portfolios(self):
        ### Getting Description
        models = Portfolio.objects.filter(fund_id=self.fund_id).all()
        for model in models:
            self.portfolios[str(model.id)]=model
        return

    ###############################################################################################
    ### Runs the Queries in Threads to Get All Required Data
    def get_dataWithThreads(self):

        ## Run 3 Query Threads Simultaneously
        for thread in self.threads:
            thread.start()
        ### Wait for Threads to Finish
        for thread in self.threads:
            thread.join()

        self.holdingModels = self.holdingThread.models
        self.staticModels = self.staticThread.models
        self.dynamicModels = self.dynamicThread.models
        
        self.handleQueryResults()
        return

    ###############################################################################################
    ### Sifts Through Results of Query to Create Position Instances - Construction of Position Object from
    ### Static Database Objects and Holding Database Objects - Populates Position Object Securities with Static Models
    ### and then Handles Dynamic Query Results - Populating the Dynamic Query Model Results for Securities in Position Object
    def handleQueryResults(self):

        ###### Flag Date Error if Missing Holdings Information for Date
        numHoldingModels = len(self.holdingModels)
        if numHoldingModels == 0:
            self.date_error = True
            return

        ######## Takes the given valid position and uses it to perform iterative
        ####### calculations on portfolio object.
        def calculateGeneralMetrics(security):

            self.market_val += security.market_val
            
            if self.categorization != None:
                self.categorization.addSecurity(security)       
            
            ####### Calculate Notional Value - Always Use Position Market Val (Never the case where its unrealized_gains_losses)
            gross_custom_notional = security.gross_custom_notional
            gross_delta_notional = security.gross_delta_notional
            pos = security.PositionDesignation.value

            ## Store Info Depending on Position
            if pos == 'L':  ### Long Positions
                self.custom_notional_exposure_long += gross_custom_notional
                self.delta_notional_exposure_long += gross_delta_notional
            else:  ### Short Positions
                self.custom_notional_exposure_short += gross_custom_notional
                self.delta_notional_exposure_short += gross_delta_notional

            self.calculate_betas()
            return

        ####################################################################
        ### Creates a Security from Given Holding Model
        def createSecurity(holdingModel):

            ### Standardize Holding Model
            holdingModel = Standardize.standardizeHoldingModel(holdingModel)
            
            static_records = [a for a in self.staticModels if str(a.rcg_id) == str(holdingModel.rcg_id)]
            if len(static_records) == 0:
                return None

            staticModel = static_records[0]

            security_name = str(staticModel.security_name)
            rcg_id = str(staticModel.rcg_id)
            ss_asset_class = str(staticModel.ss_asset_class)
            
            instrument_type = staticModel.instrument_type

            proxy_rcg_id = staticModel.proxy_rcg_id
            underlying_rcg_id = staticModel.underlying_rcg_id

            proxyModel = None
            ### Find Proxy Model ####################
            if proxy_rcg_id != None:
                ### Get Static Model Associated with Proxy Model
                proxyModels = [a for a in self.staticModels if a.rcg_id == proxy_rcg_id]
                if len(proxyModels) == 0:
                    print 'Proxy Static Security Doesnt Exist  : ', security_name, ' - ', rcg_id, ' Proxy : ', proxy_rcg_id
                else:
                    proxyModel = proxyModels[0]

            underlyingModel = None
            ### Find Underlying Model ####################
            if underlying_rcg_id != None:
                ### Get Static Model Associated with Underlying Model
                underlyingModels = [a for a in self.staticModels if a.rcg_id == underlying_rcg_id]
                if len(underlyingModels) == 0:
                    print 'Underlying Static Security Doesnt Exist  : ', security_name, ' - ', rcg_id, ' Underlying : ', underlying_rcg_id
                else:
                    underlyingModel = underlyingModels[0]

            ############ Handling of Dynamic Data for Base, Proxy and Underlying Securities ################

            #################### Handling of Base Position ##############################
            dynamicModels = [model for model in self.dynamicModels if model.rcg_id == rcg_id]
            underlyingModels = [model for model in self.dynamicModels if model.rcg_id == underlying_rcg_id]
            proxyModels = [model for model in self.dynamicModels if model.rcg_id == proxy_rcg_id]

            ### Initialize Model
            portfolio_id = str(holdingModel.rcg_portfolio_id)
            portfoioModel = self.portfolios[portfolio_id] ## Pass in portfolio model
        
            newSecurity = self.instantiateSecurity(rcg_id, self.snapshot_date, security_name, instrument_type, ss_asset_class,
                                                   holdingModel, staticModel, dynamicModels,
                                                   portfoioModel, proxyStaticModel=proxyModel,
                                                   proxyDynamicModels=proxyModels,
                                                   underlyingStaticModel=underlyingModel,
                                                   underlyingDynamicModels=underlyingModels)

            return newSecurity

        ######## Generator to create positions from holding models and store in object
        ####### memory but not storing at each iteration step for faster performance.
        def securityGenerator():

            for holdingModel in self.holdingModels:

                newSecurity = createSecurity(holdingModel)
                ### New position will be None if there is no static record for base security
                if newSecurity == None:
                    continue

                newSecurity.setup()

                ### Override Setup AQR
                if 'AQR MANAGED FUTURES' in newSecurity.SecurityName.value.upper():
                    newSecurity.RCGCustomInstrument.value = 'Other'
                    newSecurity.RCGCustomAssetClass.value = 'Other'
                    newSecurity.RCGGeoBucket.value = 'Other'
                    newSecurity.Country.value = 'Other'
                    newSecurity.Region.value = 'Other'

                if newSecurity.valid:
                    newSecurity.evaluate()  ## Evaluation performed by indidivudal security models
                    self.num_positions += 1
                    calculateGeneralMetrics(newSecurity)  ### Perform General Calculations Based on Position
                    
                    ### Track Earliest Date of Dynamic Data
                    securityEarlyDate = newSecurity.getEarliestDateOfDynamicData()
                    if self.earliestDateOfDynamicData == None:
                        self.earliestDateOfDynamicData = securityEarlyDate
                    elif securityEarlyDate < self.earliestDateOfDynamicData:
                        self.earliestDateOfDynamicData = securityEarlyDate
                        
                ## Always include regardless of whether or not it is completely valid.
                yield newSecurity

        ### Conglomerate Positions with Generator
        self.securities = list(securityGenerator())
        self.includeRCG40Act()

        self.custom_notional_exposure_gross = self.custom_notional_exposure_long + self.custom_notional_exposure_short
        self.custom_notional_exposure_net = self.custom_notional_exposure_long - self.custom_notional_exposure_short
        self.delta_notional_exposure_gross = self.delta_notional_exposure_long + self.delta_notional_exposure_short
        self.delta_notional_exposure_net = self.delta_notional_exposure_long - self.delta_notional_exposure_short

        ### Perform Calculations That Need Entier List of Positions
        self.calculate_betas()
        return

    ########################################
    ### Congolmerate Beta's and Vols for Portfolio
    def calculate_betas(self):

        ###### Date Error Flagged : Return
        if self.date_error:
            return

        self.beta_sp500 = 0.0
        self.beta_msci = 0.0

        weightedBetaMSCI = 0.0
        weightedBetaSP500 = 0.0
        #################### Congolmerate Beta's and Vols for Portfolio
        total_weight = 0.0
        for securityModel in self.securities:
            
            if securityModel.valid:
                if securityModel.Derivative.value:
                    weight = securityModel.net_notional
                else:
                    weight = securityModel.market_val

                total_weight += weight
                addBetaMsci, addSP500 = 0.0, 0.0
                if securityModel.BetaMSCI.value != None:
                    addBetaMsci = securityModel.BetaMSCI.value
                if securityModel.BetaSP500.value != None:
                    addSP500 = securityModel.BetaSP500.value

                weightedBetaMSCI += addBetaMsci * weight
                weightedBetaSP500 += addSP500 * weight

        if total_weight != 0.0:
            self.beta_sp500 = weightedBetaSP500 / total_weight
            self.beta_msci = weightedBetaMSCI / total_weight

        return