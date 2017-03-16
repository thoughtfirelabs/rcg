#####################################
### Fields that are not derived
class RawField:
    def __init__(self):
        self.raw = True
        return

#####################################
class BloombergField(RawField):
    
    def __init__(self):
        RawField.__init__(self)
        
        self.bbFieldName = None
        self.bloombergField = True
        return
        
#####################################
### Fields that are derived
class DerivedField:
    def __init__(self):
        self.raw = False
        return

### Define Specific Behaviors that Fields Can Have
class Suppressable:

    def __init__(self):
        self.suppressed = False
        self.suppressable = True
        self.suppressionValue = 'Other'  ## Default

    ### Suppresses Static Field - Only allow string static fields to be suppressed.
    def suppress(self):
        self.suppressed = True
        self.value = self.suppressionValue
        return

    ## Check if it needs to be suppressed.
    def suppressIfApplicable(self):
        if self.value != None and self.value.lower() == 'suppress':
            self.suppress()
        return


### Defines the behavior that allows the proxy security to be used to supplement the base security.
class ProxySupplement:

    def __init__(self):
        self.canProxySupplement = False
        self.supplementedWithProxy = False
        return

    ### Use proxy data to help support/supplement the data for the security.
    def supplementWithProxy(self, proxySecurity,fieldObj):
        if self.value == None and proxySecurity != None:
            ### Get Proxy Value for Base Field Type
            fieldName = self.__name__
            if getattr(proxySecurity,fieldName) and getattr(proxySecurity,fieldName).value != None:
                self.value = getattr(proxySecurity,fieldName).value
                self.supplementedWithProxy = True


### Defines the behavior that allows the underlying security to be used to help supplement the base security.
class UnderlyingSupplement:

    def __init__(self):
        self.canUnderlyingSupplement = True
        self.supplementedWithUnderlying = False
        self.underlyingBeta = None
        return

    ### Use underlying data to help support/supplement the data for the security.
    def supplementWithUnderlying(self,underlyingSecurity,fieldObj):
        if self.value == None and underlyingSecurity != None:
            ### Get Proxy Value for Base Field Type
            fieldName = self.__name__
            if getattr(underlyingSecurity,fieldName) and getattr(underlyingSecurity,fieldName).value != None:
                self.value = getattr(underlyingSecurity,fieldName).value
                self.supplementedWithUnderlying = True
                    
##############################################
### All fields have to be classified as derived or raw
class Field(ProxySupplement,UnderlyingSupplement):
    
    def __init__(self):
        
        self.valid = True ### Default
        self.required = False ### Default - Won't invalidate security unless this is flagged to True.
        self.applicable = True ### Default
        
        self.ignore = False ### Ignoring field will not try to make any assumptions or validations
                            ### will keep the field vale as None if it is not present.
        self.value = None ### Default
        self.date = None ### Default
        self.bloombergField = False ### Default
        
        ProxySupplement.__init__(self)
        UnderlyingSupplement.__init__(self)

        ### Overrides the complete invalidation of field.
        self.DeltaNotionalSafe = False 
        return
    
    ### Supplement with proxy or underlying fields if child class flagged this as 
    ### acceptable
    def supplement(self,proxySecurity,underlyingSecurity,field):
        if self.canProxySupplement :
            self.supplementWithProxy(proxySecurity,field)
        if self.canUnderlyingSupplement :
            self.supplementWithUnderlying(underlyingSecurity,field)
        
    def makeAssumption(self):
        self.value = self.assumptionValue
        
    def invalidate(self):
        self.valid = False
    
    ### Child Class Determines if Should be Standardized
    def standardize(self):
        
        
        return
    
    ### Logic -> Applicable = No , Ignore, Make assumption as 0.0 or Other but Don't Note it as assumed
    ### Not Applicable -> Required -> Fatal Missing ... Not Required -> Nonfatal Missing (Data Report) and Assumption
    def validate(self,security):
        
        if self.ignore:
            return
            
        if self.raw:
            if self.applicable:
                if self.value == None and self.required:
                    self.invalidate()
                    security.invalidateField(self)
                    
                elif self.value == None and not self.required:
                    self.makeAssumption()
                    security.noteAssumption(self)
            else:
                ### If not applicable, just make assumption but don't note it.
                self.makeAssumption()

        ### Note Assumption if not raw field?
        if not self.raw:
            self.makeAssumption()
            security.noteAssumption(self)
        return
        
    ### Stores a Specific Value to the Field Based on the Fields Type
    def storeValue(self, value, date):

        self.date = date
        funcDict = {str: 'str', float: 'float', int: 'int',bool:'bool'}
        des = funcDict[self.type]
        self.value = eval(des + '("' + str(value) + '")')
        return


##############################################
### Base Classification for Dynamic Fields
class FlagField(Field,DerivedField):
    
    static = True ### Always True
    type = bool  ### Always True
    
    def __init__(self):
        DerivedField.__init__(self)
        self.value = False ## Default
    
    ### Activates flag from being offset from its default value.
    def activate(self):
        self.value = True
        return
    
    ### Override compared to the static and dynamic fields.
    def storeValue(self, value, date):
        pass
    def makeAssumption(self):
        pass

    
##############################################
### Base Classification for Dynamic Fields
class DynamicField(Field):

    static = False
    dynamic = True
    
    def __init__(self):
        RawField.__init__(self)
        
        self.type = float  ### Default
        self.assumptionValue = 0.0
        return
    
##############################################
### Base Classification for Static Fields
class StaticField(Field):

    static = True
    dynamic = False

    def __init__(self):
        Field.__init__(self)
        
        self.type = str  ### Default
        self.assumptionValue = 'Other'

   

