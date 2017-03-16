from app.models.securityModels import TRSBondLeg, TRSEquityLeg, Equity, EquityWarrant, EquityOption, EquityFuture, \
    DomesticCash, FXCurrency, FXFuture, FXForward, Bond, BondOption, BondFuture, CreditDefaultSwap, OptionEmbeddedBond, \
    DefaultFixedIncome, RMBSNONAgency, StructuredProduct, Curve, Index

class SecurityFactory:

    def __init__(self):
        return
        
    ### Need to do: include proxy and underlying models.
    ### This doesn't store any dynamic data.
    @staticmethod
    def generateFromStaticModel(staticModel):
        
        if staticModel.instrument_type == None or staticModel.security_name == None:
            return None
        
        securityClass = SecurityFactory.classifySecurity(staticModel.instrument_type, staticModel.ss_asset_class, staticModel.security_name)
        if securityClass == None:
            return None
        
        securityModel = securityClass(staticModel.rcg_id, None, staticModel.security_name, staticModel.instrument_type, staticModel.ss_asset_class, None)
        ## Setup - only including data from static model
        securityModel.setup(None,staticModel, [])
        
        return securityModel
    
    ############################################
    ### Initializes a Security Model Object for Portfolio
    ### Inherited by portfolio or fund objects.
    def instantiateSecurity(self, rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class, holdingModel, staticModel,dynamicModels,
                            portfolioModel, proxyStaticModel=None, proxyDynamicModels=None, underlyingStaticModel=None, underlyingDynamicModels=None):
        
        securityModel = None

        if staticModel == None:
            print 'Error : Static Model Doesnt Exist for : ', holdingModel.rcg_id, ' - ', holdingModel.security_name
            self.invalidateMissingStaticModelforSecurity(holdingModel)
            return None

        ### Error - Will not be able to classify security
        #if instrument_type == None:
        if instrument_type == None:
            print 'Error : Missing Instrument Type for : '
            print '   -> Security : ', security_name
            print '   -> Instrument : ', instrument_type
            print '   -> Asset Type : ', ss_asset_class
            print '   -> Discarding Security'
            self.invalidateSecurityInstrumentType(staticModel)
            return None
            
        securityModelClass = self.classifySecurity(instrument_type, ss_asset_class, security_name)
        if securityModelClass == None:
            print 'Error Classifying Instrument Type for: '
            print '   -> Security : ', security_name
            print '   -> Instrument : ', instrument_type
            print '   -> Asset Type : ', ss_asset_class
            print '   -> Discarding Security'
            
            ## Don't include in data report here, there isn't missing information its just a misclassification
            return None
            

        securityModel = securityModelClass(rcg_id, snapshot_date, security_name, instrument_type, ss_asset_class,portfolioModel)
        securityModel.setup(holdingModel,staticModel, dynamicModels)
        securityModel.includeProxyData(proxyStaticModel=proxyStaticModel,proxyDynamicModels=proxyDynamicModels)
        securityModel.includeUnderlyingyData(underlyingStaticModel=underlyingStaticModel,underlyingDynamicModels=underlyingDynamicModels)
        
        return securityModel
        
    #### Classifies the security according to the instrument type and asset class attributes and then initializes
    #### a subclass if the classification is vaid.  The subclass is used to model the super class security_module object.
    @staticmethod
    def classifySecurity(instrument_type, ss_asset_class, security_name):
        
        assetName = None
        if ss_asset_class != None:
            assetName = ss_asset_class.lower()

        instrumentName = instrument_type.lower()
        securityName = security_name.lower()
        
        foundClassification = True

        ######## Easy Situations when Security is From State Street ####################
        if assetName != None:
            ##################################
            ### Check if Cash or Foreign Currency Treated as Cash
            if ('short' in assetName and 'term' in assetName) or 'cash' in assetName or 'spot' in assetName:
                if ('us' in securityName and 'dollar' in securityName) or (
                            'wells' in securityName and 'fargo' in securityName and 'govt' in securityName):
                    return DomesticCash
                else:
                    return FXCurrency
                    
            ####################
            elif assetName == 'equity':
                
                ### Sometimes state street classifies cash positions as equity.
                if instrumentName == 'fx' or ('cash' in securityName and 'collateral' in securityName):
                    return FXCurrency
            
                ### Equity ADR, Equity, Preferred Stock, etc.
                equityInstruments = ['equity adr', 'preferred stock', 'callable floater', 'equity', 'internal equity']
                for equityIns in equityInstruments:
                    if instrumentName == equityIns:
                        return Equity
                if 'equity' in instrumentName and 'adr' in instrumentName:
                    return Equity
                    
                ### Equity Leg of TRS
                if instrumentName == 'trs':
                    return TRSEquityLeg
                ### Model Equity Warrants as Equity
                if 'equity' in instrumentName and ('warrant' in instrumentName or 'wrt' in instrumentName):
                    return EquityWarrant
            ########################
            elif assetName == 'forward':
                ### Case when FX Forward
                if 'fx' in instrumentName:
                    return FXForward
            ##########################
            elif assetName == 'future':
                if 'bond' in instrumentName:
                    return BondFuture
                elif 'fx' in instrumentName or 'currency' in instrumentName:
                    return FXFuture
                elif 'equity' in instrumentName:
                    return EquityFuture
            #######################################
            elif assetName == 'option':
                if 'bond' in instrumentName:
                    return BondOption
                elif 'equity' in instrumentName:
                    return EquityOption
                elif 'embedded' in instrumentName and 'bond' in instrumentName:
                    return OptionEmbeddedBond
            ########################################
            elif assetName == 'bond':
                if instrumentName == 'bond':
                    return Bond
                ##############
                elif 'rmbs' in instrumentName and 'non' in instrumentName and 'agency' in instrumentName:
                    return RMBSNONAgency
                ##############
                elif 'embedded' in instrumentName and 'option' in instrumentName:
                    return OptionEmbeddedBond
                ### Bond Leg of TRS
                elif 'trs' in instrumentName:
                    return TRSBondLeg
                ### Bond Leg of CDS
                elif 'credit' in instrumentName and 'default' in instrumentName and 'swap' in instrumentName:
                    return CreditDefaultSwap
                ##############
                elif 'defaulted' in instrumentName and 'fixed' in instrumentName and 'income' in instrumentName:
                    return DefaultFixedIncome
                ##############
                elif 'structured' in instrumentName and 'product' in instrumentName:
                    return StructuredProduct

            else:
                foundClassification = False

        ######## Situations when Security is Possibly Not From State Street ####################
        if foundClassification == False:
            ### Index and Curve First
            if instrumentName == 'curve':
                return Curve

            elif instrumentName == 'index':
                return Index
            ### Weird Exceptions with State Street Classifications
            elif 'cash' in instrumentName or 'fx' in instrumentName:
                return FXCurrency
            ##############
            elif 'equity' in instrumentName:
                ##############
                if instrumentName == 'equity':
                    return Equity

                ##############
                if 'option' in instrumentName:
                    return EquityOption
                ##############
                elif 'future' in instrumentName:
                    return EquityFuture

                    ##############
                elif 'warrant' in instrumentName or 'wrt' in instrumentName:
                    return EquityWarrant
                    ##############
            elif 'bond' in instrumentName:
                if instrumentName == 'bond':
                    return Bond
                if 'option' in instrumentName:
                    return BondOption
                elif 'future' in instrumentName:
                    return BondFuture
            ##############
            elif 'future' in instrumentName and ('currency' in instrumentName or 'fx' in instrumentName):
                return FXFuture
            ##############
            elif 'embedded' in instrumentName and 'bond' in instrumentName:
                return OptionEmbeddedBond
            ##############
            elif 'rmbs' in instrumentName and 'non' in instrumentName and 'agency' in instrumentName:
                return RMBSNONAgency
            ##############
            elif 'defaulted' in instrumentName and 'fixed' in instrumentName and 'income' in instrumentName:
                return DefaultFixedIncome
            ##############
            elif 'structured' in instrumentName and 'product' in instrumentName:
                return StructuredProduct
            ##############
            else:
                return None
        return