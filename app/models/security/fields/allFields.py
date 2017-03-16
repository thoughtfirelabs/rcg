from .fieldBehaviors import ProxySupplement, UnderlyingSupplement, RawField, DerivedField, Suppressable, BloombergField
from .fieldBehaviors import FlagField, StaticField, DynamicField
from app.fields.standardization.standardize import Standardize
from app.fields.categorization import Categorization
from app.fields.fieldExcelSafeStore import FieldExcelSafeStore

from app.settings import settings


############################################################################################
### All Flag Fields

##############################################
class WFCash(FlagField):

    __name__ = 'WFCash'
    internalFieldName = 'wf_cash'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class Restricted(FlagField):

    __name__ = 'Restricted'
    internalFieldName = 'restricted'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class Derivative(FlagField):

    __name__ = 'Derivative'
    internalFieldName = 'derivative'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class ETFFlag(FlagField):

    __name__ = 'ETFFlag'
    internalFieldName = 'etf_flag'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class IndexFlag(FlagField):

    __name__ = 'IndexFlag'
    internalFieldName = 'index_flag'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class IlliquidFlag(FlagField):
    
    __name__ = 'IlliquidFlag'
    internalFieldName = 'illiquid'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class FXFlag(FlagField):
    
    __name__ = 'FXFlag'
    internalFieldName = 'fx_flag'
    def __init__(self):
        FlagField.__init__(self)
        return

##############################################
class ComdtyInterestFlag(FlagField):
    
    __name__ = 'ComdtyInterestFlag'
    internalFieldName = 'comdty_interest_instrument'
    def __init__(self):
        FlagField.__init__(self)
        return




############################################################################################
### Dynamic Fields

##############################################
class SSMarketValue(DynamicField,RawField):
    
    __name__ = 'SSMarketValue'
    internalFieldName = 'ss_market_val'
    modelFieldName = 'ss_market_val'
    
    def __init__(self):
        DynamicField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class UnrealizedPL(DynamicField,RawField):

    __name__ = 'UnrealizedPL'
    internalFieldName = 'unrealized_gains_losses'
    modelFieldName = 'unrealized_pl'

    def __init__(self):
        DynamicField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class Quantity(DynamicField,RawField):

    __name__ = 'Quantity'
    internalFieldName = 'quantity'
    modelFieldName = 'quantity'

    def __init__(self):
        DynamicField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class MarketPrice(DynamicField,RawField):

    __name__ = 'MarketPrice'
    internalFieldName = 'market_price'
    modelFieldName = 'market_price'

    def __init__(self):
        DynamicField.__init__(self)
        RawField.__init__(self)
        return

##############################################
### Default Assumption Value = 0.0
class UnderlyingBetaMSCI(DynamicField):
    
    __name__ = 'UnderlyingBetaMSCI'
    def __init__(self):
        DynamicField.__init__(self)
        self.canProxySupplement = True ## Override
    
##############################################
### Default Assumption Value = 0.0
class UnderlyingBetaSP500(DynamicField):
    
    __name__ = 'UnderlyingBetaSP500'
    def __init__(self):
        DynamicField.__init__(self)
        self.canProxySupplement = True ## Override
    
##############################################
### Default Assumption Value = 0.0
class BetaMSCI(DynamicField,BloombergField):
    
    __name__ = 'BetaMSCI'
    internalFieldName = 'beta_msci'
    modelFieldName = 'beta_msci'

    def __init__(self):
        DynamicField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        
        self.bbFieldName = 'EQY_BETA_MSCI'
        self.required = False  ### Override
        return
    

##############################################
### Don't Allow These to be Directly Supplemented by Underlying - Only Proxy
class BetaSP500(DynamicField,BloombergField):
    
    __name__ = 'BetaSP500'
    internalFieldName = 'beta_sp500'
    modelFieldName = 'beta_sp500'

    def __init__(self):
        DynamicField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        
        self.bbFieldName = 'EQY_BETA_SP'
        self.required = False  ### Override
        return


##############################################
class Duration(DynamicField,BloombergField):
    
    __name__ = 'Duration'
    bbFieldName = 'DUR_MID'
    internalFieldName = 'duration'
    modelFieldName = 'duration'

    #############
    def __init__(self):

        DynamicField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        self.canUnderlyingSupplement = True ## Override
        
        self.assumptionValue = settings.ten_year_duration ### Override
        self.DeltaNotionalSafe = True
        return


##############################################
class Volume(DynamicField,BloombergField):
    
    __name__ = 'Volume'
    internalFieldName = 'volume_avg_30d'
    modelFieldName = 'volume_avg_30d'

    def __init__(self):
        DynamicField.__init__(self)
        BloombergField.__init__(self)
        self.assumptionValue = 1000000000  # Override for Liquidity - Large Value Ensures Default is Liquid if Volume Not Founds
        self.bbFieldName = 'VOLUME_AVG_30D'
        return

##############################################
class Delta(DynamicField,BloombergField,ProxySupplement):
    
    __name__ = 'Delta'
    internalFieldName = 'delta'
    modelFieldName = 'delta'

    #############
    def __init__(self):
        DynamicField.__init__(self)
        BloombergField.__init__(self)
        ProxySupplement.__init__(self)
        
        self.assumptionValue = 1.0 ### Override - Equity Warrants Applicable Not Required
        self.bbFieldName = 'DELTA'
        
        return


##############################################
class OptionUnderlyingPrice(DynamicField,BloombergField):
    
    __name__ = 'OptionUnderlyingPrice'
    internalFieldName = 'option_underlying_price'
    modelFieldName = 'option_underlying_price'

    def __init__(self):
        DynamicField.__init__(self)
        BloombergField.__init__(self)
        self.bbFieldName = 'OPT_UNDL_PX'
        return


############################################################################################
### Static Fields

### Subclass FieldSafeStore to safely store data to this field and let this field be stored in models
class InstrumentType(RawField,StaticField):
    
    __name__ = 'InstrumentType'
    internalFieldName = 'instrument_type'
    modelFieldName = 'instrument_type'
    categorizationName = 'InstrumentType'
    
    def __init__(self):
        RawField.__init__(self)
        StaticField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = Categorization(InstrumentType.categorizationName)
        categorization.categorize(securities)
        return categorization



##############################################
class SecurityName(RawField,StaticField):
    
    __name__ = 'SecurityName'
    internalFieldName = 'security_name'
    modelFieldName = 'security_name'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class SearchName(RawField,StaticField,ProxySupplement):
    
    __name__ = 'SearchName'
    internalFieldName = 'search_name'
    modelFieldName = 'search_name'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        ProxySupplement.__init__(self)
        return


##############################################
class PortfolioName(RawField,StaticField):
    
    __name__ = 'PortfolioName'
    internalFieldName = 'portfolio_name'
    categorizationName = 'PortfolioName'

    def __init__(self): 
        StaticField.__init__(self)
        RawField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = PortfolioName.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class PortfolioID(RawField,StaticField):
    
    __name__ = 'PortfolioID'
    internalFieldName = 'portfolio_id'
    categorizationName = 'PortfolioID'

    def __init__(self): 
        StaticField.__init__(self)
        RawField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = PortfolioID.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class PortfolioStrategy(RawField,StaticField):
    
    __name__ = 'PortfolioStrategy'
    internalFieldName = 'strategy'
    categorizationName = 'PortfolioStrategy'

    def __init__(self): 
        StaticField.__init__(self)
        RawField.__init__(self)
        return
    
    @staticmethod
    def categorizeSecurities(securities):
        categorization = PortfolioStrategy.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class ISIN(BloombergField,RawField,StaticField):
    
    __name__ = 'ISIN'
    internalFieldName = 'id_isin'
    modelFieldName = 'id_isin'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_isin'
        self.ignore = True ### Override - won't make assumption or flag as missing.
        return

##############################################
class CUSIP(BloombergField,RawField,StaticField):
    
    __name__ = 'CUSIP'
    internalFieldName = 'id_cusip'
    modelFieldName = 'id_cusip'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_cusip'
        self.ignore = True ### Override - won't make assumption or flag as missing.
        return


##############################################
class SDL(BloombergField,RawField,StaticField):
    
    __name__ = 'SDL'
    internalFieldName = 'id_sedol1'
    modelFieldName = 'ss_asset_class'
    
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_sedol1'
        self.ignore = True ### Override - won't make assumption or flag as missing.
        return

##############################################
class SSAssetClass(RawField,StaticField):
    
    __name__ = 'SSAssetClass'
    internalFieldName = 'ss_asset_class'
    modelFieldName = 'ss_asset_class'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class AssetClass(BloombergField,RawField,StaticField):
    
    __name__ = 'AssetClass'
    internalFieldName = 'asset_class'
    modelFieldName = 'bpipe_reference_security_class'
    categorizationName = 'AssetClass'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        self.bbFieldName = 'bpipe_reference_security_class'
        
    @staticmethod
    def categorizeSecurities(securities):
        categorization = AssetClass.categorization
        categorization.categorize(securities)
        return categorization


##############################################
class PositionDesignation(RawField,StaticField):
    
    __name__ = 'PositionDesignation'
    internalFieldName = 'position_designation'
    modelFieldName = 'position'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class PXMult(RawField,BloombergField,StaticField):
    
    __name__ = 'PXMult'
    internalFieldName = 'px_pos_mult_factor'
    modelFieldName = 'px_pos_mult_factor'

    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.type = float  ### Override
        self.bbFieldName = 'PX_POS_MULT_FACTOR' 
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):
        if proxyFields.PXMult.value != None and self.value == None:
            self.value = proxyFields.PXMult.value
        return


##############################################
class RCGCustomInstrument(DerivedField,StaticField):
    
    __name__ = 'RCGCustomInstrument'
    internalFieldName = 'rcgCustomInstrument'
    categorizationName = 'RCGCustomInstrument'

    def __init__(self):
        StaticField.__init__(self)
        DerivedField.__init__(self)
        return
    
    @staticmethod
    def categorizeSecurities(securities):
        categorization = RCGCustomInstrument.categorization
        categorization.categorize(securities)
        return categorization

##############################################
class RCGCustomAssetClass(DerivedField,StaticField):
    
    __name__ = 'RCGCustomAssetClass'
    internalFieldName = 'rcgCustomAssetClass'
    categorizationName = 'RCGCustomAssetClass'

    def __init__(self):
        StaticField.__init__(self)
        DerivedField.__init__(self)
        return
    
    @staticmethod
    def categorizeSecurities(securities):
        categorization = RCGCustomAssetClass.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class NumContracts(DerivedField,StaticField):
    
    __name__ = 'NumContracts'
    internalFieldName = 'num_contracts'

    def __init__(self):
        StaticField.__init__(self)
        DerivedField.__init__(self)
        
        self.assumptionValue = 1 ### Override
        return

##############################################
class Issuer(RawField,StaticField,BloombergField,Suppressable):
    
    __name__ = 'Issuer'
    internalFieldName = 'issuer'
    modelFieldName = 'issuer'

    def __init__(self):
        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'ISSUER'
        return


##############################################
class Sector(RawField,StaticField,BloombergField,Suppressable,Standardize):
    
    __name__ = 'Sector'
    internalFieldName = 'sector'
    modelFieldName = 'gics_sector_name'
    categorizationName = 'Sector'

    def __init__(self):
        
        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        self.canUnderlyingSupplement = True ## Override
        
        Standardize.__init__(self)

        
        self.bbFieldName = 'GICS_SECTOR_NAME'
        return
    
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Sector.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class Industry(RawField,StaticField,BloombergField,Suppressable,Standardize):
    
    __name__ = 'Industry'
    internalFieldName = 'industry'
    modelFieldName = 'bics_level_3_industry_name'
    categorizationName = 'Industry'

    def __init__(self):

        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        self.canUnderlyingSupplement = True ## Override
        
        self.bbFieldName = 'BICS_LEVEL_3_INDUSTRY_NAME'
        return
    
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Industry.categorization
        categorization.categorize(securities)
        return categorization
        
        
##############################################
class CountryFullName(RawField,StaticField,BloombergField,Suppressable,Standardize):
    
    __name__ = 'CountryFullName'
    internalFieldName = 'country_full_name'
    modelFieldName = 'country_full_name'

    def __init__(self):
        
        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        self.canUnderlyingSupplement = True ## Override
        
        self.bbFieldName = 'COUNTRY_FULL_NAME'
        return

    
##############################################
class CountryOfRisk(RawField,StaticField,BloombergField,Suppressable,Standardize):
    
    __name__ = 'CountryOfRisk'
    internalFieldName = 'cntry_of_risk'
    modelFieldName = 'cntry_of_risk'

    def __init__(self):
        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.canProxySupplement = True ## Override
        self.canUnderlyingSupplement = True ## Override
        
        self.bbFieldName = 'CNTRY_OF_RISK'
        return


##############################################
class Region(DerivedField,StaticField):
    
    __name__ = 'Region'
    internalFieldName = 'region'
    categorizationName = 'Region'

    def __init__(self):
        DerivedField.__init__(self)
        StaticField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = Region.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class MarketType(DerivedField,StaticField):
    
    __name__ = 'MarketType'
    internalFieldName = 'market_tp'
    categorizationName = 'MarketType'

    def __init__(self):
        DerivedField.__init__(self)
        StaticField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = MarketType.categorization
        categorization.categorize(securities)
        return categorization

##############################################
class RCGGeoBucket(DerivedField,StaticField):
    
    __name__ = 'RCGGeoBucket'
    internalFieldName = 'rcg_geo_bucket'
    categorizationName = 'RCGGeoBucket'

    def __init__(self):
        DerivedField.__init__(self)
        StaticField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = RCGGeoBucket.categorization
        categorization.categorize(securities)
        return categorization

##############################################
class Country(DerivedField,StaticField):
    
    __name__ = 'Country'
    internalFieldName = 'country'
    categorizationName = 'Country'

    def __init__(self):
        DerivedField.__init__(self)
        StaticField.__init__(self)
        return

    @staticmethod
    def categorizeSecurities(securities):
        categorization = Country.categorization
        categorization.categorize(securities)
        return categorization
        
        
        
        
        
        
        