from app.fields.allFields.dynamic.allDynamicFields import *
from app.fields.allFields.static.allFlagFields import *
from app.fields.allFields.static.allGeoFields import *
from app.fields.allFields.static.allStaticFields import *
from app.models.models import dynamicRecord, staticRecord

from .modelStorage import ModelStore
import pandas as pd
from app.fields.classifications.classification import Classification

####################################################################
### Only care about raw fields and bloomberg fields for the proxy, we don't care
### about holding fields.  We do care about classified fields.

class ProxyFields(ModelStore,Classification):
    
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

        self.geoFieldList = [self.CountryOfRisk,self.CountryFullName,self.Country,self.MarketType,self.Region,self.RCGGeoBucket]
                             
        ### Static Data Fields
        ### Keep Instrument Type Separate - It is Already Stored on BaseSecurity.__init__ 
                             
        self.staticFieldList = self.geoFieldList + [self.Sector, self.Industry,
                       self.RCGCustomAssetClass, self.RCGCustomInstrument, self.Issuer,
                       self.PXMult,
                       self.SecurityName, self.SSAssetClass,self.SearchName,
                       self.ISIN, self.SDL, self.CUSIP, self.NumContracts,self.AssetClass]
        
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
                              

