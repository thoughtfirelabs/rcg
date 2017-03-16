###############################################################################
#### Represents the ability of fields to be categorized based on notioanl and other 
### quantitative measures.
class Categorization:
    
    def __init__(self,fieldName):
        
        self.fieldName = fieldName
        self.trackedFieldNames = [] ### Used to Track Field Names
        
        self.grossNotionals = {}
        self.netNotionals = {}
        self.shortNotionals = {}
        self.longNotionals = {}

        self.delta_grossNotionals = {}
        self.delta_netNotionals = {}
        self.delta_shortNotionals = {}
        self.delta_longNotionals = {}
        
        self.position_count = {}
        self.notional_allocation  = {}
        self.delta_notional_allocation = {}
        self.market_vals = {}
        self.market_allocation = {}
        
        self.grossNotionalNav = {}
        self.netNotionalNav = {}
        self.shortNotionalNav = {}
        self.longNotionalNav = {}

        self.delta_grossNotionalNav = {}
        self.delta_netNotionalNav = {}
        self.delta_shortNotionalNav = {}
        self.delta_longNotionalNav = {}
    
    ### Initializes dictionaries for new field name found.
    def initializeForFieldValue(self,fieldValue):
        
        self.trackedFieldNames.append(fieldValue)
        
        self.grossNotionals[fieldValue]=0.0
        self.netNotionals[fieldValue]=0.0
        self.shortNotionals[fieldValue]=0.0
        self.longNotionals[fieldValue]=0.0

        self.delta_grossNotionals[fieldValue]=0.0
        self.delta_netNotionals[fieldValue]=0.0
        self.delta_shortNotionals[fieldValue]=0.0
        self.delta_longNotionals[fieldValue]=0.0
        
        self.position_count[fieldValue]=0
        self.notional_allocation[fieldValue]=0.0
        self.delta_notional_allocation[fieldValue]=0.0
        self.market_vals[fieldValue]=0.0
        self.market_allocation[fieldValue]=0.0
        
        self.grossNotionalNav[fieldValue]=0.0
        self.netNotionalNav[fieldValue]=0.0
        self.shortNotionalNav[fieldValue]=0.0
        self.longNotionalNav[fieldValue]=0.0

        self.delta_grossNotionalNav[fieldValue]=0.0
        self.delta_netNotionalNav[fieldValue]=0.0
        self.delta_shortNotionalNav[fieldValue]=0.0
        self.delta_longNotionalNav[fieldValue]=0.0
        
        return
    
    ### Formats data into a presentable dictionary for front end after calculating
    ### final calculatiosn that encompass all securities
    def retrieveAnalysis(self):
        
        ### Consolidated/Summed/Percent Calculations over Fields
        for fieldValue in self.trackedFieldNames:
            
            self.grossNotionals[fieldValue]=self.shortNotionals[fieldValue]+self.longNotionals[fieldValue]
            self.netNotionals[fieldValue]=self.longNotionals[fieldValue]-self.shortNotionals[fieldValue]
            
            self.delta_grossNotionals[fieldValue]=self.delta_shortNotionals[fieldValue]+self.delta_longNotionals[fieldValue]
            self.delta_netNotionals[fieldValue]=self.delta_longNotionals[fieldValue]-self.delta_shortNotionals[fieldValue]
            
        totalNAV = sum(list(self.market_vals.values()))
        totalGrossCustom = sum(list(self.grossNotionals.values()))
        totalGrossDelta = sum(list(self.delta_grossNotionals.values()))
        
        for fieldValue in self.trackedFieldNames:
            if totalGrossCustom != 0.0:
                self.notional_allocation[fieldValue]=self.grossNotionals[fieldValue]/totalGrossCustom
            if totalGrossDelta != 0.0:
                self.delta_notional_allocation[fieldValue]=self.delta_grossNotionals[fieldValue]/totalGrossDelta

            if totalNAV != 0.0:
                self.market_allocation[fieldValue]=self.market_vals[fieldValue]/totalNAV
                
                self.delta_grossNotionalNav[fieldValue]=self.delta_grossNotionals[fieldValue]/totalNAV
                self.delta_netNotionalNav[fieldValue]=self.delta_netNotionals[fieldValue]/totalNAV
                self.delta_shortNotionalNav[fieldValue]=self.delta_shortNotionals[fieldValue]/totalNAV
                self.delta_longNotionalNav[fieldValue]=self.delta_longNotionals[fieldValue]/totalNAV
                
                self.grossNotionalNav[fieldValue]=self.grossNotionals[fieldValue]/totalNAV
                self.netNotionalNav[fieldValue]=self.netNotionals[fieldValue]/totalNAV
                self.shortNotionalNav[fieldValue]=self.shortNotionals[fieldValue]/totalNAV
                self.longNotionalNav[fieldValue]=self.longNotionals[fieldValue]/totalNAV
                
                

        exposure_analysis = {'notional_allocation':self.notional_allocation,
                        'position_count':self.position_count,
                        'gross_notional_nav':self.grossNotionalNav,
                        'net_notional_nav':self.netNotionalNav,
                        'long_notional_nav':self.longNotionalNav,
                        'short_notional_nav':self.shortNotionalNav,
                        'market_vals':self.market_vals,
                        'gross_exposures':self.grossNotionals,
                        'net_exposures':self.netNotionals,
                        'long_exposures':self.longNotionals,
                        'short_exposures':self.shortNotionals}

        return exposure_analysis
    
        
    #### Adds a security to the cateogization
    def addSecurity(self,security):
        
        if not security.valid:
            print 'Cannot Categorize : ',security.rcg_id,' - Invalid'
            return 
            
        fieldObj = security.findField(self.fieldName)
    
        if fieldObj.value != None:
            
            ### Initialize Dictionaries if Needed
            if str(fieldObj.value) not in self.trackedFieldNames:
                self.initializeForFieldValue(str(fieldObj.value))
                
            self.position_count[str(fieldObj.value)]+=1
            self.market_vals[str(fieldObj.value)]+=security.market_val

            if security.PositionDesignation.value == 'L':
                self.longNotionals[str(fieldObj.value)]+=security.gross_custom_notional
                self.delta_longNotionals[str(fieldObj.value)]+=security.gross_custom_notional
                
            else:
                self.shortNotionals[str(fieldObj.value)]+=security.gross_custom_notional
                self.delta_shortNotionals[str(fieldObj.value)]+=security.gross_custom_notional
        return
        
    ### Category factor is a string  representing what we want to group the securities
    ### by (i.e. market value, notional, etc.)
    def categorize(self,securities):
        
        for security in securities:
            self.addSecurity(security)
        return 
        
