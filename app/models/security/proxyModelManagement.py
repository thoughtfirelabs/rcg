#############################################################
class ProxyModelManagement:
    def __init__(self):

        self.missingInstrumentTypes = {}  ### Stores dictionary of static models if instrument Types
        self.missingStaticModels = {}  ### Stores dictionary of holding models if static models are missing
        self.securityDataRecords = {}
        return

    ####################################
    # ### When a security is missing a static model but there is a holding reference for it
    # ### the security cannot be validated on a per field basis but we must assume that all fields
    # ### possible are missing since there is no notion of what type of security the holdingModel is for
    # ### or what data is missing (since there is none).  For the securities stored here, all of the possible
    # ### data fields in the missing data report will be included.
    # def invalidateMissingStaticModelforSecurity(self, holdingModel):
    #     rcg_id = holdingModel.rcg_id
    #     if rcg_id != None:
    #         rcg_id = str(rcg_id)
    #         if rcg_id not in self.missingStaticModels.keys():
    #             self.missingStaticModels[rcg_id] = holdingModel
    #     else:
    #         print 'Error Invalidating Missing Static Model for Security : RCGID = None'
    #     return
    #
    # ####################################
    # ### When a security has a static model but has an invalid instrument type this function will
    # ### note that.
    # def invalidateSecurityInstrumentType(self, staticModel):
    #     rcg_id = staticModel.rcg_id
    #     if rcg_id != None:
    #         rcg_id = str(rcg_id)
    #         if rcg_id not in self.missingInstrumentTypes.keys():
    #             self.missingInstrumentTypes[rcg_id] = staticModel
    #     else:
    #         print 'Error Invalidating Missing Instrument Type for Security : RCGID = None'
    #
    # #####################################
    # #### This notes all missing data for a given security, regardless of whether or not it has been
    # #### invalidated.  If the security data records contain a fatal missing field, the security will be invalidated.
    # def finalValidate(self, security):
    #     securityDataRecords = security.missingDataRecords
    #     if security.rcg_id not in self.securityDataRecords.keys():
    #         self.securityDataRecords[security.rcg_id] = securityDataRecords
    #
    #     for record in securityDataRecords:
    #         if record.fatal:
    #             security.valid = False
    #             return
    #     return
    #
    # ############################################
    # def createFrontEndErrorReportDetails(self):
    #
    #     ### Creates Front End Data Report
    #     dataReport = FrontEndErrorReportDetails(self)
    #     error_report_details = dataReport.generate()
    #     return error_report_details

    ############################################
    ### Initializes a Security Model Object for Portfolio
    def instantiateProxy(self, rcg_id, security_name, instrument_type, ss_asset_class, holdingModel, staticModel,
                            dynamicModels,
                            portfolio=None, fund=None, proxyStaticModel=None, proxyDynamicModels=None,
                            underlyingStaticModel=None, underlyingDynamicModels=None):

        securityModel = None

        if staticModel == None:
            self.invalidateMissingStaticModelforSecurity(holdingModel)
            return None

        ### Error - Will not be able to classify security
        if instrument_type == None:
            print 'Error Trying to Classify Security Type for: '
            print '   -> Security : ', security_name
            print '   -> Instrument : ', instrument_type
            print '   -> Asset Type : ', ss_asset_class
            print '   -> Discarding Security'
            self.invalidateSecurityInstrumentType(staticModel)
            return None

        securityModelClass = self.classifySecurity(instrument_type, ss_asset_class, security_name)
        if securityModelClass != None:
            securityModel = securityModelClass(rcg_id, security_name, instrument_type, ss_asset_class, holdingModel,
                                               staticModel, dynamicModels,
                                               portfolio=portfolio, fund=fund, proxyStaticModel=None,
                                               proxyDynamicModels=None, underlyingStaticModel=None,
                                               underlyingDynamicModels=None)
        else:
            print 'Error Trying to Classify Security Type for: '
            print '   -> Security : ', security_name
            print '   -> Instrument : ', instrument_type
            print '   -> Asset Type : ', ss_asset_class
            print '   -> Discarding Security'

        return securityModel

    ############################################
    #### Classifies the security according to the instrument type and asset class attributes and then initializes
    #### a subclass if the classification is vaid.  The subclass is used to model the super class security_module object.
    def classifySecurity(self, instrument_type, ss_asset_class, security_name):

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
                ### Equity ADR, Equity, Preferred Stock, etc.
                equityInstruments = ['equity adr', 'preferred stock', 'callable floater', 'equity', 'internal equity']
                for equityIns in equityInstruments:
                    if instrumentName == equityIns:
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
