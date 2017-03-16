import numpy as np
from app.settings import settings
from .BaseSecurity import Security
from .securityModelBehaviors import DurationDependent, Option, Forward, Future, Spot

### Default Evaluation Behaviors
class NoExposureSecurity:
    def __init__(self):
        
        self.market_val = None

        self.notional = None
        self.gross_notional = None
        self.net_notional = None

        self.gross_delta_notional = None
        self.net_delta_notional = None

        self.gross_custom_notional = None
        self.net_custom_notional = None
        return
        
    ### General Market Val Calculation - Override if it does not apply.
    def evaluateMarketValue(self):
        self.market_val = self.SSMarketValue.value
    
    def evaluateExposure(self):
        self.notional = 0.0
        self.gross_notional = 0.0
        self.net_notional = 0.0
        return
        
    ###########################
    ### General Exposure Calculation - Override if it does not apply.
    def evaluateDeltaExposure(self):
        self.gross_delta_notional = 0.0
        self.net_delta_notional = 0.0
            
    def evaluateCustomExposure(self):
        self.gross_custom_notional = 0.0
        self.net_custom_notional = 0.0
        return
        
    def evaluate(self):
        self.evaluateMarketValue()
        self.evaluateExposure()
        self.evaluateDeltaExposure()
        self.evaluateCustomExposure()

### Default Evaluation Behaviors
class ModelEvaluation:
    def __init__(self):
        
        self.market_val = None

        self.notional = None
        self.gross_notional = None
        self.net_notional = None

        self.gross_delta_notional = None
        self.net_delta_notional = None

        self.gross_custom_notional = None
        self.net_custom_notional = None
        return
        
    ### General Market Val Calculation - Override if it does not apply.
    def evaluateMarketValue(self):
        self.market_val = self.SSMarketValue.value
    
    def evaluateExposure(self):
        self.notional = self.SSMarketValue.value
        self.gross_notional = np.abs(self.notional)
        self.net_notional = self.notional
        return
        
    ###########################
    ### General Exposure Calculation - Override if it does not apply.
    def evaluateDeltaExposure(self):
        if self.deltaNotionalValid:
            self.gross_delta_notional = self.gross_notional
            self.net_delta_notional = self.net_notional
            
    def evaluateCustomExposure(self):
        if self.customNotionalValid:
            self.gross_custom_notional = self.gross_notional
            self.net_custom_notional = self.net_notional
        return
    
    ### Default Behavior - Only Overriden for Derivatives with Underlying
    def evaluateBeta(self):
        return
        
    def evaluate(self):
        
        self.evaluateMarketValue()
        self.evaluateExposure()
        self.evaluateDeltaExposure()
        self.evaluateCustomExposure()
        
        self.evaluateBeta()
        
    
    #    #######################################
#    ### Calculate Volume and Determine Whether or Not Security is Liquid
#    def evaluateLiquidity(self,fields):
#
#        if self.applicable:
#
#            if self.value != None:
#                sevenDayVolume = 5.0 * self.value
#                ### self.numContracts Represents Number of Shares of Bond Future
#                if sevenDayVolume <= fields.numContracts:
#                    self.illiquidFlag = True
#        return
#
        
##############################################################
### Custom Security for RCG 40 Act Fund - All Cash Sleeeve
class RCG40Act(Spot,Security,NoExposureSecurity,ModelEvaluation):
    
    def __init__(self, rcg_id, snapshot_date, portfolioModel):

        Security.__init__(self, rcg_id, snapshot_date, rcg_id, None, None, None)
        Spot.__init__(self)
        NoExposureSecurity.__init__(self)
        ModelEvaluation.__init__(self)
        
        self.SecurityName.value = 'RCG40Act'
        self.InstrumentType.value = 'Cash'
        self.Issuer.value = 'Suppress'
        self.Sector.value = 'Suppress'
        self.Industry.value = 'Suppress'
        
        ### Other geo classifications should be determined as 'Other' from suppression.
        self.CountryFullName.value = 'Suppress'
        self.CountryOfRisk.value = 'Suppress'
        
        self.RCGCustomInstrument.value = 'Other'
        self.RCGCustomAssetClass.value = 'Other'
        
        ### Default Separately
        self.InstrumentType.value = 'Cash'
        
        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False
        self.Liquidity.applicable = False
        
        self.Liquidity.numContracts = 1
        return

    ##### Override
    def evaluateMarketValue(self):
        self.market_val = 2173253.21
        return
    

##############################################################
class TRSBondLeg(DurationDependent,NoExposureSecurity,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DurationDependent.__init__(self)
        NoExposureSecurity.__init__(self)
        ModelEvaluation.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False
        
        ## Will force custom exposure to 0.0
        self.Duration.value = 0.0 
        
        self.Liquidity.applicable = False
        ### NumShares/Num Contracts
        if self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value)
        return
    
    ### Override
    def evaluateDeltaExposure(self):
        if self.deltaNotionalValid:
            self.gross_delta_notional = np.abs(self.market_val)
            self.net_delta_notional = self.market_val


##############################################################
class TRSEquityLeg(Security,ModelEvaluation):
    
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Equity'
        
        ### NumShares/Num Contracts
        if self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value)
        return
    


##############################################################
class Equity(Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.RCGCustomInstrument.value = 'Equities'
        self.RCGCustomAssetClass.value = 'Equity'

        ### NumShares/Num Contracts
        if self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value)
        return

##############################################################
### Option class methods override base security class methods.
class EquityWarrant(Option,Security,ModelEvaluation):
    
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Option.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.RCGCustomAssetClass.value = 'Equity'
        self.Delta.value = 1.0 ### Forces delta notional to be notional amount
        #self.Delta.required = False ### Override
        #self.OptionUnderlyingPrice.required = False ### Override
        
        ### NumShares/Num Contracts
        if self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value)
        
        return

##############################################################
### Option class methods override base security class methods.
class EquityOption(Option, Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Option.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel) 
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.RCGCustomAssetClass.value = 'Equity'

        ### NumShares/Num Contracts
        if self.PXMult.value != None and self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value / self.PXMult.value)
        return

##############################################################
### Future class methods override base security class methods.
class EquityFuture(Future, Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Future.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.RCGCustomAssetClass.value = 'Equity'
        
        ### NumShares/Num Contracts
        if self.PXMult.value != None and self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value / self.PXMult.value)
        return
    
##############################################################
class DomesticCash(Spot,NoExposureSecurity,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Spot.__init__(self)
        NoExposureSecurity.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.RCGCustomAssetClass.value = 'Other' 
        self.CountryFullName.value = 'United States'
        self.Country.value = 'United States'
        self.CountryOfRisk.value = 'US'
        self.Region.value = 'North America'
        self.MarketType.value = 'Developed Market'
        self.RCGGeoBucket.value = 'Other'
        
        self.Issuer.value = 'Suppress'
        self.Sector.value = 'Suppress'
        self.Industry.value = 'Suppress'
        
        self.NumContracts.value = 1.0
        return


##############################################################
class FXCurrency(Spot, Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.FXFlag.activate()
        self.RCGCustomAssetClass.value = 'Currency'
        return
    
    ## Override Exposure Calculations
    def evaluateExposure(self):

        if 'usd' in self.SecurityName.value.lower() or self.rcg_id.lower() == 'rcgusd999999':
            self.zeroNotional()
            return

        if self.deltaNotionalValid:
            self.notional = self.SSMarketValue.value
            self.gross_notional = np.abs(self.notional)
            self.net_notional = self.notional

            self.gross_delta_notional = self.gross_notional
            self.net_delta_notional = self.net_notional

            if self.customNotionalValid:

                self.gross_custom_notional = self.gross_delta_notional
                self.net_custom_notional = self.net_delta_notional
        return
    

##############################################################
class FXFuture(Future,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Future.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.FXFlag.activate()

        self.NumContracts.value = 1.0
        self.RCGCustomAssetClass.value = 'Currency'
        
        return


##############################################################
class FXForward(Forward,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Forward.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)                          
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.FXFlag.activate()
        
        self.RCGCustomAssetClass.value = 'Currency'
        self.NumContracts.value = 1.0
        self.Liquidity.applicable = False ### Override

        return
        


##############################################################
class Bond(DurationDependent,Security,ModelEvaluation):
    
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DurationDependent.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)                                                                             
        ModelEvaluation.__init__(self)
        
        self.RCGCustomAssetClass.value = 'Fixed Income' 
        self.RCGCustomInstrument.value = 'Fixed Income' 
        
        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return
    
    ##### Override to Exclude Treasury Bills
    def evaluateDeltaExposure(self):

        if 'treasury' in self.SecurityName.value.lower() and 'bill' in self.SecurityName.value.lower():
            self.gross_delta_notional = 0.0
            self.net_delta_notional = 0.0
            self.Duration.required = False
            return
        
        if self.deltaNotionalValid:
            self.gross_delta_notional = np.abs(self.SSMarketValue.value)
            self.net_delta_notional = self.SSMarketValue.value
    
    ##### Override to Exclude Treasury Bills
    def evaluateCustomExposure(self):
        
        if 'treasury' in self.SecurityName.value.lower() and 'bill' in self.SecurityName.value.lower():
            self.gross_delta_notional = 0.0
            self.net_delta_notional = 0.0
            self.Duration.required = False
            return
        
        if self.customNotionalValid:
            duration_ratio = self.Duration.value / settings().ten_year_duration
            self.gross_custom_notional = np.abs(self.SSMarketValue.value) * duration_ratio
            self.net_custom_notional = self.SSMarketValue.value * duration_ratio
                
        
##############################################################
class BondOption(Option,DurationDependent,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Option.__init__(self)
        DurationDependent.__init__(self) ### Gives Custom Exposure Calculation Method
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        if self.PXMult.value != None and self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value / self.PXMult.value)
        return


##############################################################
class BondFuture(Future,DurationDependent,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        Future.__init__(self)
        DurationDependent.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.ComdtyInterestFlag.activate()
        self.RCGCustomAssetClass.value = 'Fixed Income'
    
        if self.PXMult.value != None and self.Quantity.value != None:
            self.Liquidity.numContracts = np.abs(self.Quantity.value / self.PXMult.value)
        return
    

##############################################################
class CreditDefaultSwap(ModelEvaluation,Security):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        ModelEvaluation.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return


##############################################################
class OptionEmbeddedBond(ModelEvaluation,Security):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        ModelEvaluation.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return


##############################################################
class DefaultFixedIncome(DurationDependent,ModelEvaluation,Security):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DurationDependent.__init__(self)
        ModelEvaluation.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        
        self.RCGCustomInstrument.value = 'Fixed Income'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        self.Duration.required = False
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0

        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return


##############################################################
class RMBSNONAgency(DurationDependent,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DurationDependent.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0
        
        self.Duration.required = False

        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False

        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return


##############################################################
class StructuredProduct(DurationDependent,Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
        
        DurationDependent.__init__(self)
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
                                 
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        self.RCGCustomAssetClass.value = 'Fixed Income'
        
        self.Duration.required = False
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0
        
        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False

        if self.Quantity.value != None:
            self.Liquidity.numContracts = self.Quantity.value
        return


##############################################################
class Curve(Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.RCGCustomInstrument.value = 'Other'
        self.RCGCustomAssetClass.value = 'Other'
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0
        
        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False
        
        self.Liquidity.applicable = False
        return

##############################################################
class Index(Security,ModelEvaluation):
    def __init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel):
                 
        Security.__init__(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, portfolioModel)
        ModelEvaluation.__init__(self)
        
        self.RCGCustomInstrument.value = 'Other'
        self.RCGCustomAssetClass.value = 'Other'
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0
        
        self.BetaSP500.applicable = False
        self.BetaMSCI.applicable = False
        
        self.Liquidity.applicable = False
        return