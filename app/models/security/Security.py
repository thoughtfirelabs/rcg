from .fields.fields import Fields
from .ProxySecurity import ProxySecurity
from .UnderlyingSecurity import UnderlyingSecurity
from .securityValidation import SecurityValidation
import pandas as pd

################################################################################
### A single Missing Data Field for a security, can be fatal or non fatal, dynamic or static
### Nonfatal Data Fields can include an assumption
class FieldDataRecord:
    def __init__(self, security, field):

        self.id = None
        self.security = security
        self.field = field

        self.dynamic = False
        self.static = field.static

        if not self.static:
            self.dynamic = True

    ###################################
    ### Generates Unique ID for This Record to Keep Track of Duplicates
    def generateRecordID(self):
        dateString = pd.to_datetime(self.security.snapshot_date).strftime("%Y_%m_%d")
        self.id = self.security.rcg_id + '_' + dateString + self.field.internalFieldName
        return


################################################################################
### Missing Data Fields for Single security (i.e. assortment of fields associated with invalid
### data points for a single security Object)
class securityDataRecords:
    def __init__(self):

        self.missingDataRecords = []

        self.missingUnderlyingRecords = []
        self.missingProxyRecords = []

        self.missingUnderlying = False
        self.missingProxy = False
        return


### Defines default behavior for a base security inherited by each security model.
### These behaviors and flags can be overridden in additional behavior objects.
class DefaultBehaviors:
    
    def __init__(self):
        
        self.proxy_rcg_id = None
        self.underlying_rcg_id = None
        
        self.proxySecurity = None ## Default
        self.underlyingSecurity = None  ## Default
        
        self.valid = True
        self.customNotionalValid = True
        self.deltaNotionalValid = True
        
        return

from .allFields import InstrumentType, SecurityName, SearchName, SSAssetClass, AssetClass, ISIN, SDL, CUSIP, PositionDesignation, MarketPrice, Quantity
from .allFields import UnrealizedPL, SSMarketValue, NumContracts, Issuer, PXMult, Sector, Industry, RCGCustomAssetClass, RCGCustomInstrument,
from .allFields import CountryOfRisk, CountryFullName, Country, MarketType, Region, RCGGeoBucket
from .allFields import PortfolioName, PortfolioID, PortfolioStrategy, Duration, Delta, OptionUnderlyingPrice, BetaMSCI, BetaSP500, Liquidity
from .allFields import WFCash, Restricted, Derivative, ETFFlag, IlliquidFlag, IndexFlag, ComdtyInterestFlag, FXFlag

class AllFields:
    def __init__(self):
        
        self.InstrumentType = InstrumentType()
        
        self.SecurityName = SecurityName()
        self.SearchName = SearchName()
        self.SSAssetClass = SSAssetClass()
        self.AssetClass = AssetClass()

        self.ISIN = ISIN()
        self.SDL = SDL()
        self.CUSIP = CUSIP()

        #### Fields for Holding Position
        self.PositionDesignation = PositionDesignation()
        self.MarketPrice = MarketPrice()
        self.Quantity = Quantity()
        self.UnrealizedPL = UnrealizedPL()
        self.SSMarketValue = SSMarketValue()

        self.NumContracts = NumContracts()
        self.Issuer = Issuer()
        self.PXMult = PXMult()

        self.Sector = Sector()
        self.Industry = Industry()

        self.RCGCustomAssetClass = RCGCustomAssetClass()
        self.RCGCustomInstrument = RCGCustomInstrument()

        ############ Geo Fields
        self.CountryOfRisk = CountryOfRisk()
        self.CountryFullName = CountryFullName()
        self.Country = Country()
        self.MarketType = MarketType()
        self.Region = Region()
        self.RCGGeoBucket = RCGGeoBucket()
        
        ############## Portfolio Field Info
        self.PortfolioName = PortfolioName()
        self.PortfolioID = PortfolioID()
        self.PortfolioStrategy = PortfolioStrategy()
            
        self.geoFieldList = [self.CountryOfRisk,self.CountryFullName,self.Country,self.MarketType,self.Region,self.RCGGeoBucket]
                             
        self.Duration = Duration()
        self.Delta = Delta()
        self.OptionUnderlyingPrice = OptionUnderlyingPrice()

        self.BetaMSCI = BetaMSCI()
        self.BetaSP500 = BetaSP500()

        self.Liquidity = Liquidity()

        ########### Flag Fields
        self.WFCash = WFCash()
        self.Restricted = Restricted()

        self.Derivative = Derivative()
        self.ETFFlag = ETFFlag()
        self.IlliquidFlag = IlliquidFlag()
        self.IndexFlag = IndexFlag()

        self.ComdtyInterestFlag = ComdtyInterestFlag()
        self.FXFlag = FXFlag()
    

        
############################################################################################################################
### Fields object inherited by security object to allow all of the differetn security models to have control over their
### field designations, defaults and values.
class Security(DefaultBehaviors,AllFields,securityDataRecords,SecurityValidation):
    
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DefaultBehaviors.__init__(self)
        AllFields.__init__(self)
        
        self.rcg_id = rcg_id
        self.snapshot_date = snapshot_date
        self.earliestDateOfDynamicData = None ### Tracked by individual dynamic models
        
        self.portfolioModel = portfolioModel
        
        SecurityValidation.__init__(self)
        
        ### Store Data to Fields
        if self.portfolioModel != None:
            self.PortfolioID.value = self.portfolioModel.id
            self.PortfolioName.value = self.portfolioModel.portfolio_name
            self.PortfolioStrategy.value = self.portfolioModel.strategy
        
        self.SecurityName.value = security_name
        self.InstrumentType.value = instrument_type  ### Include Immediately
        self.SSAssetClass.value = ss_asset_class
        
        securityDataRecords.__init__(self)
        
        #################### Dynamic Data
        self.crncy_adj_mkt_cap = None
        self.volatility_162w = None

        return
    
    ### Validates the security based on the data provided by the models
    def validate(self):
        for key, field in self.__dict__.items():
            if isinstance(field,Field) and field.requiresValidation:
                field.validate(self)
                
    ####### Outputs the Security Data in Dictionary Format
    def retrieveData(self):
        
        outputData = {}
        objects = ['InstrumentType','SecurityName','SearchName','SSAssetClass','AssetClass','ISIN',
                   'SDL','CUSIP','PositionDesignation','Quantity','UnrealizedPL',
                   'SSMarketValue','NumContracts','Issuer','PXMult','Industry',
                   'MarketType','Country','RCGGeoBucket','Region','PortfolioName',
                   'CountryOfRisk','CountryFullName','Sector',
                   'PortfolioID','PortfolioStrategy','Duration','Delta','OptionUnderlyingPrice',
                   'BetaMSCI','BetaSP500','Liquidity','WFCash','Restricted',
                   'Derivative','ETFFlag','IlliquidFlag','IndexFlag','RCGCustomAssetClass','RCGCustomInstrument']
        
        for objectName in objects:
            obj = getattr(self,objectName)
            if obj.value != None:
                outputData[obj.internalFieldName]=obj.value
        
        return outputData
        
    
    ##### Proxies and Underlyings ##################
    def includeUnderlyingyData(self,underlyingStaticModel=None,underlyingDynamicModels=None):
        self.underlyingStaticModel = underlyingStaticModel
        self.underlyingDynamicModels = underlyingDynamicModels
        ### Initialize Underlying Securities
        if self.underlyingStaticModel != None:
            self.underlyingSecurity = UnderlyingSecurity(underlyingStaticModel, underlyingDynamicModels)
        return
        
    def includeProxyData(self,proxyStaticModel=None,proxyDynamicModels=None):
        self.proxyStaticModel = proxyStaticModel
        self.proxyDynamicModels = proxyDynamicModels
        ### Initialize Proxy Securities
        if self.proxyStaticModel != None:
            self.proxySecurity = ProxySecurity(proxyStaticModel, proxyDynamicModels)
        return
        
    ### Sets up security model data and associates it with underlying and proxy securities
    def setup(self,holdingModel,staticModel, dynamicModels):
        
        self.holdingModel = holdingModel
        self.staticModel = staticModel
        self.dynamicModels = dynamicModels
        
        ### Store Model Data
        self.storeModel(self.holdingModel)
        self.storeModel(staticModel)
        if dynamicModels != None:
            for dynamicModel in dynamicModels:
                self.storeModel(dynamicModel)
                
        ### Store Data to Possible Proxy Security and Underlying Security
        if self.proxySecurity != None:
            self.proxySecurity.setup()
        if self.underlyingSecurity != None:
            self.underlyingSecurity.setup()

        ############ Setup Base Security Fields

        ### (1) Supplement - Supplement missing data with possible data from proxy or underlyings first.
        for field in self.staticFieldList:
            if field.canSupplementWithProxy:
                field.supplementWithProxy(self.proxySecurity,field)
            if field.canSupplementWithUnderlying:
                field.supplementWithUnderlying(self.underlyingSecurity,field)

        for field in self.dynamicFieldList:
            if field.canSupplementWithProxy:
                field.supplementWithProxy(self.proxySecurity,field)
            if field.canSupplementWithUnderlying:
                field.supplementWithUnderlying(self.underlyingSecurity,field)

        ### Finalize Supplement of Complicated Dynamic Fields.
        self.BetaMSCI.finalize(self)
        self.BetaSP500.finalize(self)
        
        
        ### (2) Standardize and Classify Static Data

        ### Standardize Raw Data First
        self.Sector.standardize()
        self.CountryFullName.standardize()
        
        ### Classify and Standardize Derived Data
        self.classifyGeography()

        ### (3) Classify Flags
        self.classifyWFCash()
        self.classifyRestricted()
        self.classifyETF()
        self.classifyIndex()

        ### (4) Suppress if Allowed - Suppress Fields if Applicable
        ### Suppression needs to be done before validation so that missing data that is not required is not noted.
        ### Suppression also needs to be doen after standardization and classification.
        for field in self.staticFieldList:
            if field.suppressable:
                field.suppressIfApplicable()

        ### (5) Make Assumptions

        ### If country full name is suppressed and country of risk is missing, then we have to assume
        ### that other geographical fields are 'Other'
        if self.CountryFullName.suppressed and self.CountryOfRisk.value == None:
            self.Region.assume()
            self.MarketType.assume()
            self.RCGGeoBucket.assume()
        return
