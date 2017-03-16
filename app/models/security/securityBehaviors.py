### Defines Specific Behaviors That Define Security Models
import numpy as np
from app.settings import settings

###########################
class Defaults:
    
    def __init__(self):
        
        self.fixedincome = False
        self.future = False
        self.forward = False
        self.option = False
        
        self.PXMult.required = False ### Default
        self.Delta.required = False ### Default
        self.OptionUnderlyingPrice.required = False ### Default
        
        self.Liquidity.applicable = True ### Default
        return


###########################
### Cash and currency instrument behaviors defined here.
class Spot(Defaults):
    
    def __init__(self):
        
        Defaults.__init__(self)
        
        self.BetaSP500.value = 0.0
        self.BetaMSCI.value = 0.0
        self.Liquidity.applicable = False
        
        ### RCGCustomAssetClass will either be currency or other,depending on whether or not 
        ### it is cash or fx currency.
        self.RCGCustomInstrument.value = 'Other'
        self.NumContracts.value = 1.0
        return
    
    ### Overrides from General Calculations
    def evaluateExposure(self):
        self.notional = self.SSMarketValue.value
        self.gross_notional = np.abs(self.notional)
        self.net_notional = self.notional
        return
    
    ### Overrides from General Calculations
    def evaluateCustomExposure(self):
        if self.customNotionalValid:
            if 'usd' in self.SecurityName.value.lower() or self.rcg_id.lower() == 'rcgusd999999':
                self.gross_custom_notional = 0.0
                self.net_custom_notional = 0.0
                return
                
            self.gross_custom_notional = np.abs(self.gross_delta_notional)
            self.net_custom_notional = self.net_delta_notional
        return
    
    ### Overrides from General Calculations
    def evaluateDeltaExposure(self):
        if self.deltaNotionalValid:
            if 'usd' in self.SecurityName.value.lower() or self.rcg_id.lower() == 'rcgusd999999':
                self.gross_delta_notional = 0.0
                self.net_delta_notional = 0.0
                return
                
            self.gross_delta_notional = np.abs(self.notional)
            self.net_delta_notional = self.notional
        return
        

###########################    
class DurationDependent(Defaults):
    
    def __init__(self):
        Defaults.__init__(self)
        self.Duration.applicable = True
        self.Duration.required = True ### Override
        return
    
    ### Override Custom Exposure for Duration Equivalent
    def evaluateCustomExposure(self):
        
        if self.customNotionalValid:
            
            ### Duration should not be None if required since it would have been invalidated.
            if self.Duration.required == True:
                duration_ratio = self.Duration.value / settings().ten_year_duration
                self.gross_custom_notional = self.gross_delta_notional * duration_ratio
                self.net_custom_notional = self.net_delta_notional * duration_ratio
            
            ### If not required, can use duration ratio of 1 if duration is missing.
            else:
                if self.Duration.value == None:
                     duration_ratio = 1.0
                else:
                     duration_ratio = self.Duration.value / settings().ten_year_duration
                self.gross_custom_notional = self.gross_delta_notional * duration_ratio
                self.net_custom_notional = self.net_delta_notional * duration_ratio
        return
            
###########################    
class Option(Defaults):
    
    def __init__(self):
        
        Defaults.__init__(self)
        
        self.option = True
        self.Delta.required = True ### Override
        self.Delta.applicable = True ### Override
        
        self.PXMult.required = True ### Override
        self.OptionUnderlyingPrice.required = True ### Override
        self.OptionUnderlyingPrice.applicable = True ### Override
        
        self.PXMult.applicable = True
        self.PXMult.required = True
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'

        return
    
    ### Override from General Exposure Calculation
    def evaluateExposure(self):
        self.notional = self.OptionUnderlyingPrice.value * self.Quantity.value
        self.gross_notional = np.abs(self.notional)
        self.net_notional = self.notional
        
    def evaluateDeltaExposure(self):
        if self.deltaNotionalValid:
            self.gross_delta_notional = np.abs(self.gross_notional * self.Delta.value)
            self.net_delta_notional = self.net_notional * self.Delta.value
    
    ### Validates Field to Determine Whether or Not It Is Needed - Makes Assumption if Not Needed
    ### If assumption made, the date associated with the field is the snapshot date of the portfolio.
    def validateDynamicFields(self):
        ### Equity warrant has delta not required.
        if self.Delta.value == None and self.Delta.required:
            self.valid, self.deltaNotionalValid, self.customnotionalValid = False, False, False
            self.Delta.invalidateField()
            
            
###########################
### Almost exactly the same as the Future object.
class Forward(Defaults):
    
    def __init__(self):
        
        Defaults.__init__(self)
        
        self.forward = True
        self.Delta.required = True       
        self.Delta.value = 1.0
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        
        return
    
    ###########################
    def evaluateMarketValue(self):
        self.market_val = self.UnrealizedPL.value
        
    ###########################
    def evaluateExposure(self):
        
        ### These two should always be equal for a future
        if self.deltaNotionalValid and self.customNotionalValid:

            self.notional = self.SSMarketValue.value
            self.gross_notional = np.abs(self.notional)
            self.net_notional = self.notional

            self.gross_delta_notional = self.gross_notional * self.Delta.value
            self.net_delta_notional = self.net_notional * self.Delta.value

            self.gross_custom_notional = self.gross_delta_notional
            self.net_custom_notional = self.net_delta_notional
            
    ### Validates Field to Determine Whether or Not It Is Needed - Makes Assumption if Not Needed
    ### If assumption made, the date associated with the field is the snapshot date of the portfolio.
    def validateDynamicFields(self):
        ### Only want to validate applicable fields with missing data
        if self.Delta.value == None:
            self.valid, self.deltaNotionalValid, self.customnotionalValid = False, False, False
            self.Delta.invalidateField()
    
       
###########################
### Almost exactly the same as the forward object.
class Future(Defaults):
    
    def __init__(self):
        
        Defaults.__init__(self)
        
        self.future = True
        
        self.Delta.required = True       
        self.Delta.applicable = True
        self.Delta.value = 1.0
        
        self.PXMult.required = True ### Override
        self.PXMult.applicable = True
        
                
        
        self.Derivative.activate()
        self.RCGCustomInstrument.value = 'Derivatives'
        
        return
    
    ####### Override General Calculation
    def evaluateMarketValue(self):
        self.market_val = self.UnrealizedPL.value
    
    ###### Override General Calculation
    def evaluateDeltaExposure(self):
        if self.deltaNotionalValid:
            self.gross_delta_notional = self.gross_notional * self.Delta.value
            self.net_delta_notional = self.net_notional * self.Delta.value
        
    ###### Override General Calculation
    def evaluateCustomExposure(self):
        if self.customNotionalValid:
            self.gross_custom_notional = self.gross_notional * self.Delta.value
            self.net_custom_notional = self.net_notional * self.Delta.value
        

    ### Validates Field to Determine Whether or Not It Is Needed - Makes Assumption if Not Needed
    ### If assumption made, the date associated with the field is the snapshot date of the portfolio.
    def validateDynamicFields(self):
        ### Only want to validate applicable fields with missing data
        if self.Delta.value == None:
            self.valid, self.deltaNotionalValid, self.customnotionalValid = False, False, False
            self.Delta.invalidateField()
        
        
