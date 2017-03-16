from .fieldBehaviors import ProxySupplement, UnderlyingSupplement, RawField, DerivedField, Suppressable, BloombergField
from .fieldBehaviors import FlagField, StaticField, DynamicField
from app.fields.standardization.standardize import Standardize
from app.fields.categorization import Categorization
from app.fields.fieldExcelSafeStore import FieldExcelSafeStore

from app.settings import settings


##############################################
### All Flag Fields

##############################################
class WFCash(FlagField):

	internalFieldName = 'wf_cash'
	### Alternates only apply to the data models and not the Bloomberg Data Pulls
	alternates = ['wf_cash']
	def __init__(self):
		FlagField.__init__(self)
		return

##############################################
class Restricted(FlagField):

	internalFieldName = 'restricted'
	alternates = ['restricted']
	def __init__(self):
		FlagField.__init__(self)
		return

##############################################
class Derivative(FlagField):

	internalFieldName = 'derivative'
	alternates = ['derivative','derivative_flag','der_flag']
	def __init__(self):
		FlagField.__init__(self)
		return
  
##############################################
class ETFFlag(FlagField):

	internalFieldName = 'etf_flag'
	alternates = ['etf_flag','ETFFlag','ETF_Flag','etf']
	def __init__(self):
		FlagField.__init__(self)
		return
  
##############################################
class IndexFlag(FlagField):

	internalFieldName = 'index_flag'
	alternates = ['index_flag','index','IndexFlag','Index']
	def __init__(self):
		FlagField.__init__(self)
		return

##############################################
class IlliquidFlag(FlagField):

	internalFieldName = 'illiquid'
	alternates = ['illiquid','liquidity','liquid','illiquid_flag','liquid_flag']
	def __init__(self):
		FlagField.__init__(self)
		return

##############################################
class FXFlag(FlagField):

	internalFieldName = 'fx_flag'
	alternates = ['FXFlag','fx_flag','fx flag']
	def __init__(self):
		FlagField.__init__(self)
		return

##############################################
class ComdtyInterestFlag(FlagField):
    
	internalFieldName = 'comdty_interest_instrument'
	alternates = ['comdty_interest_instrument','comdty_interest_flag','commodity_interest_flag']
	def __init__(self):
		FlagField.__init__(self)
		return


### Dynamic Field Default : Applicable and Required

### Override if the field is not required for delta or custom notional calculations,
### override if it is not a float type field and override if the field doesn't have 0.0 as an assumed/suppress value.
### Override if field is not a raw field, or the field is not applicable (usually in security models)

##############################################
class SSMarketValue(DynamicField):
    
    bbFieldName = None
    internalFieldName = 'ss_market_val'
    modelFieldName = 'ss_market_val'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['ss_market_val', 'ss_market_value','market_val','market_value']

    #############
    def __init__(self):
        self.assumptionValue = None
        DynamicField.__init__(self)
        return

##############################################
class UnrealizedPL(DynamicField):

    bbFieldName = None
    internalFieldName = 'unrealized_gains_losses'
    modelFieldName = 'unrealized_pl'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['unrealized_gains_losses', 'unrealized_pl']

    #############
    def __init__(self):
        self.assumptionValue = None
        DynamicField.__init__(self)
        return

##############################################
class Quantity(DynamicField):

    bbFieldName = None
    internalFieldName = 'quantity'
    modelFieldName = 'quantity'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['quantity']

    #############
    def __init__(self):
        self.assumptionValue = None
        DynamicField.__init__(self)
        return

##############################################
class MarketPrice(DynamicField):

    bbFieldName = None
    internalFieldName = 'market_price'
    modelFieldName = 'market_price'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['market_price', 'price', 'market_px']

    #############
    def __init__(self):
        self.assumptionValue = None
        DynamicField.__init__(self)
        return

##############################################
class BetaMSCI(DynamicField,ProxySupplement,UnderlyingSupplement):

    bbFieldName = 'EQY_BETA_MSCI'
    internalFieldName = 'beta_msci'
    modelFieldName = 'beta_msci'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['beta_msci', 'EQY_BETA_MSCI']

    #############
    def __init__(self):
        DynamicField.__init__(self)
        ProxySupplement.__init__(self)
        UnderlyingSupplement.__init__(self)
        
        self.assumptionValue = 0.0
        
        self.required = False  ### Override
        self.required_for_delta = False  ### Override
        return

    ### Functions for Beta Fields Only - Try to combine delta and underlying beta if available
    def finalize(self, fields):
        if fields.Delta.value != None and self.underlyingBeta != None:
            self.value = self.underlyingBeta * fields.Delta.value



##############################################
class BetaSP500(DynamicField,ProxySupplement,UnderlyingSupplement):

    bbFieldName = 'EQY_BETA_SP'
    internalFieldName = 'beta_sp500'
    modelFieldName = 'beta_sp500'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['beta_sp500', 'EQY_BETA_SP', 'beta']

    #############
    def __init__(self):
        DynamicField.__init__(self)
        ProxySupplement.__init__(self)
        UnderlyingSupplement.__init__(self)
        
        self.assumptionValue = 0.0
        
        self.required = False  ### Override
        self.required_for_delta = False  ### Override
        return

    ### Functions for Beta Fields Only - Try to combine delta and underlying beta if available
    def finalize(self,fields):
        if fields.Delta.value != None and self.underlyingBeta != None:
            self.value = self.underlyingBeta * fields.Delta.value



##############################################
class Duration(DynamicField,ProxySupplement,UnderlyingSupplement):

    bbFieldName = 'DUR_MID'
    internalFieldName = 'duration'
    modelFieldName = 'duration'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['duration', 'dur', 'dur_mid', 'DUR_MID']

    #############
    def __init__(self):

        DynamicField.__init__(self)
        ProxySupplement.__init__(self)
        UnderlyingSupplement.__init__(self)
        
        self.assumptionValue = settings.ten_year_duration ### Override
        
        ### Override These Unless Model Specfies Otherwise
        self.applicable = False
        self.required_for_delta = False
        self.required = False
        
        blah blah blah
        self.DeltaNotionalSafe = True
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):

        if proxyFields.Duration.value != None and self.value == None:
            self.value = proxyFields.Duration.value

        if underlyingFields.Duration.value != None and self.value == None:
            self.value = underlyingFields.Duration.value
        return


##############################################
class Liquidity(DynamicField):

    bbFieldName = 'VOLUME_AVG_30D'
    internalFieldName = 'volume_avg_30d'
    modelFieldName = 'volume_avg_30d'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['volume', 'volume_avg_30d', 'VOLUME_AVG_30D', 'liquidity']
    assumptionValue = 'Liquid'  ### Assumption that seucrity is liquid
    type = str
    #############
    def __init__(self):
        
        DynamicField.__init__(self)

        self.illiquidFlag = False ### Default
        self.value = None
        
        self.required = False  ### Override
        self.required_for_delta = False  ### Override
        return

    #######################################
    ### Calculate Volume and Determine Whether or Not Security is Liquid
    def setup(self,fields):

        if self.applicable:

            if self.value != None:
                sevenDayVolume = 5.0 * self.value
                ### self.numContracts Represents Number of Shares of Bond Future
                if sevenDayVolume <= fields.numContracts:
                    self.illiquidFlag = True
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):
        if proxyFields.Volume.value != None and self.value == None:
            self.value = proxyFields.Volume.value
        return


##############################################
class Delta(DynamicField,ProxySupplement):

    bbFieldName = 'DELTA'
    internalFieldName = 'delta'
    modelFieldName = 'delta'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['delta', 'DELTA']

    #############
    def __init__(self):
        DynamicField.__init__(self)
        ProxySupplement.__init__(self)
        
        self.assumptionValue = 1.0 ### Override
        
        ### Override These Unless Model Specfies Otherwise
        self.applicable = False
        self.required_for_delta = False
        self.required = False
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):
        if proxyFields.Delta.value != None and self.value == None:
            self.value = proxyFields.Delta.value
        return


##############################################
class OptionUnderlyingPrice(DynamicField):

    bbFieldName = 'OPT_UNDL_PX'
    internalFieldName = 'option_underlying_price'
    modelFieldName = 'option_underlying_price'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['option_underlying_price', 'OPT_UNDL_PX', 'opt_undl_price', 'opt_underlying_price',
                  'option_undl_price', 'opt_undl_px', 'option_undl_px',
                  'option_underlying_px', 'opt_underlying_price']
    

    #############
    def __init__(self):
        DynamicField.__init__(self)
        
        self.assumptionValue = None ### Override
        
        ### Override These Unless Model Specfies Otherwise
        self.applicable = False
        self.required_for_delta = False
        self.required = False
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):
        if proxyFields.OptionUnderlyingPrice.value != None and self.value == None:
            self.value = proxyFields.OptionUnderlyingPrice.value
        return



#### Almost all static fields are set to applicable and not required as default,
#### this means that if they are missing the security will not be invalidated and an assumption
#### value will be used.  PXMult is defaulted to required and applicable = False, but if this is set
#### to required and applicable in the security model, it will be necessary for the security to not 
### be invalidated.

### If field is required - override, if field is not raw - override, if field is not applicable - override (in security
### model).

### Subclass FieldSafeStore to safely store data to this field and let this field be stored in models
class InstrumentType(RawField):

    internalFieldName = 'instrument_type'
    modelFieldName = 'instrument_type'
    alternates = ['instrument_type','InstrumentType','instrument']
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

    internalFieldName = 'security_name'
    modelFieldName = 'security_name'
    alternates = ['security_name', 'sec_name']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class SearchName(RawField,StaticField,ProxySupplement):

    internalFieldName = 'search_name'
    modelFieldName = 'search_name'
    alternates = ['search_name']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        ProxySupplement.__init__(self)
        return


##############################################
class PortfolioName(RawField,StaticField):

    internalFieldName = 'portfolio_name'
    categorizationName = 'PortfolioName'
    alternates = ['portfolio_name', 'manager','PortfolioName']

    #############
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

    internalFieldName = 'portfolio_id'
    categorizationName = 'PortfolioID'
    alternates = ['portfolio_id','port_id','PortfolioID']

    #############
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

    internalFieldName = 'strategy'
    categorizationName = 'PortfolioStrategy'
    alternates = ['strategy', 'portfolio_strategy','manager_strategy','PortfolioStrategy']

    #############
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

    internalFieldName = 'id_isin'
    modelFieldName = 'id_isin'
    alternates = ['id_isin', 'isin', 'isn']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_isin'
        self.ignore = True
        return

##############################################
class CUSIP(BloombergField,RawField,StaticField):

    internalFieldName = 'id_cusip'
    modelFieldName = 'id_cusip'
    alternates = ['id_cusip', 'ssid', 'cusip','id_cusip']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_cusip'
        self.ignore = True
        return


##############################################
class SDL(BloombergField,RawField,StaticField):

    bbFieldName = 'id_sedol1'
    internalFieldName = 'id_sedol1'
    modelFieldName = 'ss_asset_class'

    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['id_sedol1', 'id_sedol', 'sedol','sdl']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'id_isin'
        self.ignore = True
        return

##############################################
class SSAssetClass(RawField,StaticField):

    internalFieldName = 'ss_asset_class'
    modelFieldName = 'ss_asset_class'
    alternates = ['ss_asset_class','SSAssetClass']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class AssetClass(BloombergField,RawField,StaticField):

    internalFieldName = 'asset_class'
    modelFieldName = 'bpipe_reference_security_class'
    categorizationName = 'AssetClass'
    alternates = ['asset_class','bpipe_reference_security_class','AssetClass']

    #############
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

    internalFieldName = 'position_designation'
    modelFieldName = 'position'
    alternates = ['position_designation', 'position']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        return

##############################################
class PXMult(RawField,BloombergField,StaticField):

    internalFieldName = 'px_pos_mult_factor'
    modelFieldName = 'px_pos_mult_factor'
    alternates = ['px_pos_mult_factor', 'px_mult', 'PXMult', 'position_multiplier', 'pos_multiplier', 'px_multiplier',
                  'PX_POS_MULT_FACTOR']

    #############
    def __init__(self):
        StaticField.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.type = float  ### Override
        self.applicable = False ### Override
        self.bbFieldName = 'PX_POS_MULT_FACTOR' 
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):
        if proxyFields.PXMult.value != None and self.value == None:
            self.value = proxyFields.PXMult.value
        return


##############################################
class RCGCustomInstrument(DerivedField,StaticField):

    internalFieldName = 'rcgCustomInstrument'
    categorizationName = 'RCGCustomInstrument'
    alternates = ['RCGCustomInstrument','rcgCustomInstrument']

    #############
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

    internalFieldName = 'rcgCustomAssetClass'
    categorizationName = 'RCGCustomAssetClass'
    alternates = ['RCGCustomAssetClass','rcgCustomAssetClass']

    #############
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

    internalFieldName = 'num_contracts'
    alternates = ['num_contracts','numContracts']
    assumptionValue = 1

    #############
    def __init__(self):
        StaticField.__init__(self)
        DerivedField.__init__(self)
        return

##############################################
class Issuer(RawField,StaticField,BloombergField,Suppressable):

    internalFieldName = 'issuer'
    modelFieldName = 'issuer'
    alternates = ['issuer']

    #############
    def __init__(self):
        StaticField.__init__(self)
        Suppressable.__init__(self)
        RawField.__init__(self)
        BloombergField.__init__(self)
        
        self.bbFieldName = 'ISSUER'
        return


##############################################
class Sector(StaticField,Suppressable,ProxySupplement,Standardize,UnderlyingSupplement):

    bbFieldName = 'GICS_SECTOR_NAME'
    internalFieldName = 'sector'
    modelFieldName = 'gics_sector_name'

    categorizationName = 'Sector'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['sector', 'gics_sector_name', 'GICS_SECTOR_NAME']

    #############
    def __init__(self):
        StaticField.__init__(self)
        Suppressable.__init__(self)
        ProxySupplement.__init__(self)
        Standardize.__init__(self)
        UnderlyingSupplement.__init__(self)
        
        return
    
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Sector.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class Industry(StaticField,Suppressable,ProxySupplement,UnderlyingSupplement):

    bbFieldName = 'BICS_LEVEL_3_INDUSTRY_NAME'
    internalFieldName = 'industry'
    modelFieldName = 'bics_level_3_industry_name'

    categorizationName = 'Industry'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['bics_level_3_industry_name', 'industry', 'BICS_LEVEL_3_INDUSTRY_NAME']

    #############
    def __init__(self):

        StaticField.__init__(self)
        Suppressable.__init__(self)
        ProxySupplement.__init__(self)
        UnderlyingSupplement.__init__(self)

        return
    
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Industry.categorization
        categorization.categorize(securities)
        return categorization
        
        
##############################################
class CountryFullName(StaticField,Suppressable,Standardize):

    bbFieldName = 'COUNTRY_FULL_NAME'
    internalFieldName = 'country_full_name'
    modelFieldName = 'country_full_name'

    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['country_full_name']
    assumptionValue = 'Other'
    suppressionValue = 'Other'

    #############
    def __init__(self):
        StaticField.__init__(self)
        Suppressable.__init__(self)
        Standardize.__init__(self)
        return

    #######################################
    ### Called After Setup
    def supplement(self, fields, proxyFields, underlyingFields):

        if not self.suppressed:
            if proxyFields.CountryFullName.value != None and self.value == None:
                self.value = proxyFields.CountryFullName.value
            if underlyingFields.CountryFullName.value != None and self.value == None:
                self.value = proxyFields.CountryFullName.value
        return
    
##############################################
class CountryOfRisk(RawField,StaticField):

    bbFieldName = 'CNTRY_OF_RISK'
    internalFieldName = 'cntry_of_risk'
    modelFieldName = 'cntry_of_risk'

    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['cntry_of_risk']

    #############
    def __init__(self):
        RawField.__init__(self)
        StaticField.__init__(self)
        return

    #######################################
    def supplement(self, fields, proxyFields, underlyingFields):

        if proxyFields.CountryOfRisk.value != None and self.value == None:
            self.value = proxyFields.CountryOfRisk.value
        if underlyingFields.CountryOfRisk.value != None and self.value == None:
            self.value = proxyFields.CountryOfRisk.value
        return


##############################################
class Region(StaticField):

    bbFieldName = None
    internalFieldName = 'region'
    modelFieldName = None

    categorizationName = 'Region'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['region']

    #############
    def __init__(self):
        
        StaticField.__init__(self)
        self.rawField = False ### Override
        return
    
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Region.categorization
        categorization.categorize(securities)
        return categorization
        
##############################################
class MarketType(StaticField):

    bbFieldName = None
    internalFieldName = 'market_tp'
    modelFieldName = None

    categorizationName = 'MarketType'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['market_type', 'market_tp','MarketType']

    #############
    def __init__(self):
        StaticField.__init__(self)
        self.rawField = False ### Override
        return
    
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = MarketType.categorization
        categorization.categorize(securities)
        return categorization

##############################################
class RCGGeoBucket(StaticField):

    bbFieldName = None
    internalFieldName = 'rcg_geo_bucket'
    modelFieldName = None

    categorizationName = 'RCGGeoBucket'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['rcg_geo_bucket','rcg_bucket','RCGGeoBucket']

    #############
    def __init__(self):
        
        StaticField.__init__(self)
        self.rawField = False
        return
    
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = RCGGeoBucket.categorization
        categorization.categorize(securities)
        return categorization

##############################################
class Country(StaticField):

    bbFieldName = None
    internalFieldName = 'country'
    modelFieldName = None

    categorizationName = 'Country'
    ### Alternates only apply to the data models and not the Bloomberg Data Pulls
    alternates = ['country']

    #############
    def __init__(self):
        
        StaticField.__init__(self)
        self.rawField = False
        return

    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    @staticmethod
    def categorizeSecurities(securities):
        categorization = Country.categorization
        categorization.categorize(securities)
        return categorization
        
        
        
        
        
        
        