from app.fields.allFields.allFields import *
from .modelStorage import ModelStore
from app.fields.classifications.classification import Classification

##This object groups all of the differetn fields together, which are each defined
## based on different groupings and behaviors based on the field type and parent class of each
## field.

class AllFields:
    
    staticFieldObjects = [SecurityName, SearchName, ISIN, SDL, CUSIP, PositionDesignation, 
                          Sector, Industry, Issuer,
                          CountryOfRisk, CountryFullName, Country, MarketType,Region, RCGGeoBucket, 
                          PXMult, MarketPrice, Quantity, UnrealizedPL, SSMarketValue,NumContracts,
                          AssetClass,SSAssetClass,RCGCustomAssetClass,RCGCustomInstrument,
                          PortfolioName,PortfolioID,PortfolioStrategy]
    
    dynamicFieldObjects = [Duration, Delta, OptionUnderlyingPrice, BetaMSCI, BetaSP500,Liquidity]
    flagFieldObjects = [Derivative, ETFFlag, IndexFlag, FXFlag,
                              ComdtyInterestFlag, Restricted, WFCash, IlliquidFlag]
    allFieldObjects = [InstrumentType] + staticFieldObjects + dynamicFieldObjects + flagFieldObjects
    ######################
    def __init__(self):

        ModelStore.__init__(self)
        Classification.__init__(self)
        
        self.InstrumentType = InstrumentType()
        
        self.SecurityName = SecurityName()
        self.SearchName = SearchName()
        self.SSAssetClass = SSAssetClass()
        self.AssetClass = AssetClass()

        self.ISIN = ISIN()
        self.SDL = SDL()
        self.CUSIP = CUSIP()

        self.underlyingApplicable = False

        #### Fields for Holding Position
        self.PositionDesignation = PositionDesignation()
        self.MarketPrice = MarketPrice()
        self.Quantity = Quantity()
        self.UnrealizedPL = UnrealizedPL()
        self.SSMarketValue = SSMarketValue()

        self.holdingFieldList = [self.PositionDesignation, self.MarketPrice, self.Quantity, self.UnrealizedPL,
                                 self.SSMarketValue]

        self.NumContracts = NumContracts()
        self.Issuer = Issuer()
        self.PXMult = PXMult()

        ### Sector/Industry Fields
        self.Sector = Sector()
        self.Industry = Industry()

        ### Asset Class/Instrument Field Types
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
                             
        ### Static Data Fields
        ### Keep Instrument Type Separate - It is Already Stored on BaseSecurity.__init__ 
                             
        self.staticFieldList = self.geoFieldList + [self.Sector, self.Industry,
                       self.RCGCustomAssetClass, self.RCGCustomInstrument, self.Issuer,
                       self.PXMult,
                       self.MarketPrice, self.Quantity, self.UnrealizedPL, self.SSMarketValue,
                       self.SecurityName, self.SSAssetClass,self.SearchName,
                       self.ISIN, self.SDL, self.CUSIP, self.PositionDesignation, self.NumContracts,self.AssetClass,
                       self.PortfolioName,self.PortfolioID,self.PortfolioStrategy]
        
        ############ Dynamic Fields
        self.Duration = Duration()
        self.Delta = Delta()
        self.OptionUnderlyingPrice = OptionUnderlyingPrice()

        self.BetaMSCI = BetaMSCI()
        self.BetaSP500 = BetaSP500()

        self.Liquidity = Liquidity()
        

        self.dynamicFieldList = [self.Duration, self.Delta, self.OptionUnderlyingPrice, self.BetaMSCI, self.BetaSP500,
                                 self.Liquidity]

        ########### Flag Fields
        self.WFCash = WFCash()
        self.Restricted = Restricted()

        self.Derivative = Derivative()
        self.ETFFlag = ETFFlag()
        self.IlliquidFlag = IlliquidFlag()
        self.IndexFlag = IndexFlag()

        self.ComdtyInterestFlag = ComdtyInterestFlag()
        self.FXFlag = FXFlag()
        
        self.flagFieldList = [self.Derivative, self.ETFFlag, self.IndexFlag, self.FXFlag,
                              self.ComdtyInterestFlag, self.Restricted, self.WFCash, self.IlliquidFlag]
        return

    ######################################
    ### Takes a field name as a string and the non-initialized field object.
    ### Used for accessing static methods of the field objects
    @staticmethod
    def findStaticFieldObject(fieldName):

        for field in Fields.allFieldObjects:
            if fieldName.lower() in [fieldN.lower() for fieldN in field.alternates]:
                return field
        print 'Cannot Find Field Object Associated With : ',fieldName
        return None
        
    ######################################
    ### Takes a field name as a string and returns the object corresponding to the relevant field
    def findField(self, fieldName):
        ## Check Instrument Type First - It is kept separate from other static fields
        if fieldName.lower() in [fieldN.lower() for fieldN in self.InstrumentType.alternates]:
            return self.InstrumentType
            
        for field in self.geoFieldList + self.dynamicFieldList + self.flagFieldList + self.staticFieldList + self.holdingFieldList:
            if fieldName.lower() in [fieldN.lower() for fieldN in field.alternates]:
                return field
        print 'Cannot Find Field Object Associated With : ',fieldName
        return None
    
    ################################################
    ### Gets the earliest date in which dynamic data is stored for models.
    def getEarliestDateOfDynamicData(self):
        
        ### If no dynamic data used, set the earliest date to the snapshot date.
        earliestDateOfDynamicData = self.snapshot_date     

        for field in self.dynamicFieldList:
            if field.value != None:
                if field.date <= earliestDateOfDynamicData:
                    earliestDateOfDynamicData = field.date
        
        return earliestDateOfDynamicData
        


