import heapq
import numpy as np
from app.models.securityModels import EquityFuture, CreditDefaultSwap, EquityOption, FXForward, TRSBondLeg, TRSEquityLeg, FXCurrency, Equity, FXFuture, EquityWarrant, BondOption, BondFuture, Bond

### Inherited by Manager Constraints to allow it to be analyzed.
class ManagerConstraintCalculation:

    def __init__(self):

        self.calculations = {}

        self.calculations['beta_msci'] = 0.0
        self.calculations['beta_sp500'] = 0.0

        ### General Exposures
        self.calculations['short_exposure_notional'] = 0.0
        self.calculations['long_exposure_notional'] = 0.0
        self.calculations['net_exposure_notional'] = 0.0
        self.calculations['gross_exposure_notional'] = 0.0

        self.calculations['short_exposure_notional_noderivative'] = 0.0
        self.calculations['long_exposure_notional_noderivative'] = 0.0
        self.calculations['gross_exposure_notional_noderivative'] = 0.0
        self.calculations['net_exposure_notional_noderivative'] = 0.0


        ### Sector Industry
        self.calculations['sector_notional'] = 0.0
        self.calculations['sector_market_val'] = 0.0
        self.calculations['industry_notional'] = 0.0
        self.calculations['industry_market_val'] = 0.0


        ### Concentrations
        self.calculations['single_security_notional'] = 0.0
        self.calculations['single_security_market_val'] = 0.0
        self.calculations['single_issuer_notional'] = 0.0
        self.calculations['single_issuer_market_val'] = 0.0
        self.calculations['top10_security_notional'] = 0.0
        self.calculations['top10_security_market_val'] = 0.0


        ### Geography
        self.calculations['non_us_single_country_notional'] = 0.0
        self.calculations['non_us_single_country_market_val'] = 0.0

        self.calculations['developed_europe_asia_non_us_notional'] = 0.0
        self.calculations['developed_europe_asia_non_us_market_val'] = 0.0

        self.calculations['non_developed_notional'] = 0.0
        self.calculations['non_developed_market_val'] = 0.0

        self.calculations['developed_europe_non_us_notional'] = 0.0
        self.calculations['developed_europe_non_us_market_val'] = 0.0

        self.calculations['developed_notional'] = 0.0
        self.calculations['developed_market_val'] = 0.0

        self.calculations['emerging_notional'] = 0.0
        self.calculations['emerging_market_val'] = 0.0

        self.calculations['frontier_notional'] = 0.0
        self.calculations['frontier_market_val'] = 0.0

        #### Instruments and Asset Classes
        self.calculations['equity_options_notional'] = 0.0
        self.calculations['equity_options_market_val'] = 0.0

        self.calculations['equity_futures_notional'] = 0.0
        self.calculations['equity_futures_market_val'] = 0.0

        self.calculations['interest_rate_swaps_notional'] = 0.0
        self.calculations['interest_rate_swaps_market_val'] = 0.0

        self.calculations['currency_forwards_notional'] = 0.0
        self.calculations['currency_forwards_market_val'] = 0.0

        self.calculations['total_return_swaps_notional'] = 0.0
        self.calculations['total_return_swaps_market_val'] = 0.0

        self.calculations['commodity_interest_notional'] = 0.0
        self.calculations['commodity_interest_market_val'] = 0.0
        self.calculations['commodity_interest_options_notional'] = 0.0
        self.calculations['commodity_interest_options_market_val'] = 0.0

        self.calculations['credit_derivatives_notional'] = 0.0
        self.calculations['credit_derivatives_market_val'] = 0.0

        self.calculations['equity_net_exposure_notional'] = 0.0
        self.calculations['bond_net_exposure_notional'] = 0.0
        self.calculations['equity_net_exposure_market_val'] = 0.0
        self.calculations['bond_net_exposure_market_val'] = 0.0
        
        self.calculations['max_single_currency_notional'] = 0.0
        self.calculations['min_single_currency_notional'] = 0.0
        self.calculations['max_single_currency_market_val'] = 0.0
        self.calculations['min_single_currency_market_val'] = 0.0


        ### Miscelanneous
        self.calculations['restricted_securities'] = 0.0
        self.calculations['max_outstanding_etf_shares'] = 0.0
        self.calculations['illiquid_securities'] = 0.0

        return

    ### Stores the values calculated to the actual constraint object for evaluation.
    def store(self):

        for key in self.calculations.keys():
            self.storeValue(key,self.calculations[key])
        return

    ### Makes all necessary calculation numbers that are goign to be needed.
    def performCalculations(self):

        self.temporarySector = {}
        self.temporarySector['market_val']={}
        self.temporarySector['notional']={}

        self.temporaryIndustry = {}
        self.temporaryIndustry['market_val']={}
        self.temporaryIndustry['notional']={}

        self.temporaryCurrency = {}
        self.temporaryCurrency['market_val']={}
        self.temporaryCurrency['notional']={}

        self.temporaryIssuers = {}
        self.temporaryIssuers['market_val']={}
        self.temporaryIssuers['notional']={}

        self.temporarySecurities = {}
        self.temporarySecurities['market_val']={}
        self.temporarySecurities['notional']={}

        self.calculations['beta_msci']=self.beta_msci
        self.calculations['beta_sp500']=self.beta_sp500

        for security in self.securities:
            if security.valid and security.customNotionalValid:

                self.handleGeneral(security)
                self.handleIlliquid(security)
                self.handleRestricted(security)
                self.handleConcentration(security)

                self.handleIndustry(security)
                self.handleSector(security)

                self.handleCurrency(security)
                self.handleInstrument(security)

                self.handleRestricted(security)
                self.handleGeo(security)

                self.handleNetBond(security)
                self.handleNetEquity(security)
                #self.handleCommodityInterestPosition(security)

        if self.market_val == 0.0:
            print 'Error - Portfolio for : ',self.portfolio_id,' Has Market Val = 0'
            print 'Cannot Calculate Constraints'
            return

        ##### Finalize General Calculations
        self.calculations['long_exposure_notional'] = self.calculations['long_exposure_notional']/self.market_val
        self.calculations['short_exposure_notional'] = self.calculations['short_exposure_notional']/self.market_val
        self.calculations['gross_exposure_notional'] = self.calculations['long_exposure_notional'] + self.calculations['short_exposure_notional']
        self.calculations['net_exposure_notional'] = self.calculations['long_exposure_notional'] - self.calculations['short_exposure_notional']

        self.calculations['long_exposure_notional_noderivative'] = self.calculations['long_exposure_notional_noderivative']/self.market_val
        self.calculations['short_exposure_notional_noderivative'] = self.calculations['short_exposure_notional_noderivative']/self.market_val
        self.calculations['gross_exposure_notional_noderivative'] = self.calculations['long_exposure_notional_noderivative'] + self.calculations['short_exposure_notional_noderivative']
        self.calculations['net_exposure_notional_noderivative'] = self.calculations['long_exposure_notional_noderivative'] - self.calculations['short_exposure_notional_noderivative']

        ##### Finalize Industry/Sector Calculations
        if len(self.temporarySector['market_val'].keys()) != 0.0:
            self.calculations['sector_market_val'] = max(self.temporarySector['market_val'].values())/self.market_val

        if len(self.temporarySector['notional'].keys()) != 0.0:
            self.calculations['sector_notional'] = max(self.temporarySector['notional'].values())/self.market_val

        if len(self.temporaryIndustry['market_val'].keys()) != 0.0:
            self.calculations['industry_market_val'] = max(self.temporaryIndustry['market_val'].values())/self.market_val

        if len(self.temporaryIndustry['notional'].keys()) != 0.0:
            self.calculations['industry_notional'] = max(self.temporaryIndustry['notional'].values())/self.market_val

        ##### Finalize Geography Calculations
        self.calculations['non_us_single_country_market_val'] = self.calculations['non_us_single_country_market_val']/self.market_val
        self.calculations['non_us_single_country_notional'] = self.calculations['non_us_single_country_notional']/self.market_val
        self.calculations['developed_europe_asia_non_us_notional'] = self.calculations['developed_europe_asia_non_us_notional']/self.market_val
        self.calculations['developed_europe_asia_non_us_market_val'] = self.calculations['developed_europe_asia_non_us_market_val']/self.market_val
        self.calculations['non_developed_notional'] = self.calculations['non_developed_notional']/self.market_val
        self.calculations['non_developed_market_val'] = self.calculations['non_developed_market_val']/self.market_val
        self.calculations['developed_europe_non_us_notional'] = self.calculations['developed_europe_non_us_notional']/self.market_val
        self.calculations['developed_europe_non_us_market_val'] = self.calculations['developed_europe_non_us_market_val']/self.market_val

        self.calculations['developed_notional'] = self.calculations['developed_notional']/self.market_val
        self.calculations['developed_market_val'] = self.calculations['developed_market_val']/self.market_val
        self.calculations['emerging_notional'] = self.calculations['emerging_notional']/self.market_val

        self.calculations['emerging_market_val'] = self.calculations['emerging_market_val']/self.market_val
        self.calculations['frontier_notional'] = self.calculations['frontier_notional']/self.market_val
        self.calculations['frontier_market_val'] = self.calculations['frontier_market_val']/self.market_val


        #### Finalize Instruments and Asset Classes
        self.calculations['equity_options_notional'] = self.calculations['equity_options_notional']/self.market_val
        self.calculations['equity_options_market_val'] = self.calculations['equity_options_market_val']/self.market_val

        self.calculations['equity_futures_notional'] = self.calculations['equity_futures_notional']/self.market_val
        self.calculations['equity_futures_market_val'] = self.calculations['equity_futures_market_val']/self.market_val

        self.calculations['interest_rate_swaps_notional'] = self.calculations['interest_rate_swaps_notional']/self.market_val
        self.calculations['interest_rate_swaps_market_val'] = self.calculations['interest_rate_swaps_market_val']/self.market_val

        self.calculations['currency_forwards_notional'] = self.calculations['currency_forwards_notional']/self.market_val
        self.calculations['currency_forwards_market_val'] = self.calculations['currency_forwards_market_val']/self.market_val

        self.calculations['total_return_swaps_notional'] = self.calculations['total_return_swaps_notional']/self.market_val
        self.calculations['total_return_swaps_market_val'] = self.calculations['total_return_swaps_market_val']/self.market_val

        self.calculations['commodity_interest_notional'] = self.calculations['commodity_interest_notional']/self.market_val
        self.calculations['commodity_interest_market_val'] = self.calculations['commodity_interest_market_val']/self.market_val
        self.calculations['commodity_interest_options_notional'] = self.calculations['commodity_interest_options_notional']/self.market_val
        self.calculations['commodity_interest_options_market_val'] = self.calculations['commodity_interest_options_market_val']/self.market_val

        self.calculations['credit_derivatives_notional'] = self.calculations['credit_derivatives_notional']/self.market_val
        self.calculations['credit_derivatives_market_val'] = self.calculations['credit_derivatives_market_val']/self.market_val

        self.calculations['equity_net_exposure_notional'] = self.calculations['equity_net_exposure_notional']/self.market_val
        self.calculations['bond_net_exposure_notional'] = self.calculations['bond_net_exposure_notional']/self.market_val
        self.calculations['equity_net_exposure_market_val'] = self.calculations['equity_net_exposure_market_val']/self.market_val
        self.calculations['bond_net_exposure_market_val'] = self.calculations['bond_net_exposure_market_val']/self.market_val
        
        ##### Handle Maximum and Minimum Currency Values
        if len(self.temporaryCurrency['notional'].keys()) != 0.0:
            self.calculations['max_single_currency_notional'] = max(self.temporaryCurrency['notional'].values())/self.market_val

        if len(self.temporaryCurrency['notional'].keys()) != 0:
            self.calculations['min_single_currency_notional'] = min(self.temporaryCurrency['notional'].values())/self.market_val

        if len(self.temporaryCurrency['market_val'].keys()) != 0:
            self.calculations['max_single_currency_market_val'] = max(self.temporaryCurrency['market_val'].values())/self.market_val

        if len(self.temporaryCurrency['market_val'].keys()) != 0:
            self.calculations['min_single_currency_market_val'] = min(self.temporaryCurrency['market_val'].values())/self.market_val


        ### Concentrations
        if len(self.temporarySecurities['market_val'].keys()) != 0:
            self.calculations['single_security_market_val'] = max(self.temporarySecurities['market_val'].values())/self.market_val
        if len(self.temporarySecurities['notional'].keys()) != 0:
            self.calculations['single_security_notional'] = max(self.temporarySecurities['notional'].values())/self.market_val

        if len(self.temporaryIssuers['market_val'].keys()) != 0:
            self.calculations['single_issuer_market_val'] = max(self.temporaryIssuers['market_val'].values())/self.market_val

        if len(self.temporaryIssuers['notional'].keys()) != 0:
            self.calculations['single_issuer_notional'] = max(self.temporaryIssuers['notional'].values())/self.market_val


        if len(self.temporarySecurities['market_val'].keys()) != 0:
            allSecurityMarketVals = list(self.temporarySecurities['market_val'].values())
            max_10 = heapq.nlargest(10,allSecurityMarketVals)
            self.calculations['top10_security_market_val'] = sum(max_10)/self.market_val

        if len(self.temporarySecurities['notional'].keys()) != 0:
            allSecurityNotionals = list(self.temporarySecurities['notional'].values())
            max_10 = heapq.nlargest(10,allSecurityNotionals)
            self.calculations['top10_security_notional'] = sum(max_10)/self.market_val


        self.calculations['max_outstanding_etf_shares'] = self.calculations['max_outstanding_etf_shares']/self.market_val
        self.calculations['illiquid_securities'] = self.calculations['illiquid_securities']/self.market_val

        ### Temporary for Now
        self.calculations['interest_rate_swaps_notional'] = 0.0
        self.calculations['interest_rate_swaps_market_val'] = 0.0
        self.calculations['max_outstanding_etf_shares'] = 0.0

        self.store()
        # self.maxSharesPctETF = 0.0
        # for security in self.loopSecurities:
        #     if security.ETFFlag.value:
        #         ## Num Shares of ETF
        #         numShares = security.NumContracts.value

    ################################################################################################################
    ################################################################################################################
    ## Calculation Functions Can be Overriden if Deemed Appropriate

    def handleGeneral(self,security):

        if not security.Derivative.value:
            if security.PositionDesignation.value == 'L':
                self.calculations['long_exposure_notional_noderivative']+=security.gross_custom_notional
            else:
                self.calculations['short_exposure_notional_noderivative']+=security.gross_custom_notional

        ### General Exposure Calculations
        ### Have to handle options with put/call signs slightly differently
        if isinstance(security,EquityOption):
            if 'call' in security.SecurityName.value.lower() and security.PositionDesignation.value == 'S':
                self.calculations['long_exposure_notional']-=security.gross_custom_notional
            elif 'put' in security.SecurityName.value.lower() and security.PositionDesignation.value == 'L':
                self.calculations['short_exposure_notional']-=security.gross_custom_notional
            else:
                if security.PositionDesignation.value == 'L':
                    self.calculations['long_exposure_notional']+=security.gross_custom_notional
                else:
                    self.calculations['short_exposure_notional']+=security.gross_custom_notional
        else:
            if security.PositionDesignation.value == 'L':
                self.calculations['long_exposure_notional']+=security.gross_custom_notional
            else:
                self.calculations['short_exposure_notional']+=security.gross_custom_notional

        return

    def handleConcentration(self,security):
        
        ### Note : ETF (Check ETF Flag) and FX Excluded
        if security.FXFlag.value or security.IndexFlag.value or security.ETFFlag.value:
            return

        if security.AssetClass.value != None and security.AssetClass.value.lower() == 'fund':
            return
            
        ### Exclude Derivatives for Wellington
        if str(self.portfolio_id) == '9408':
            if security.Derivative.value == True:
                return
            
        ## Make Sure Domestic Cash Not in Concentration
        if security.InstrumentType.value.lower() == 'cash':
            return
            
        self.temporarySecurities['market_val'][security.rcg_id]=security.market_val
        self.temporarySecurities['notional'][security.rcg_id]=security.gross_custom_notional
            
        if security.Issuer.value != None and security.Issuer.value.lower() != 'other' and security.Issuer.value.lower() != 'suppress':
        
            if security.Issuer.value not in self.temporaryIssuers['market_val'].keys():
                self.temporaryIssuers['market_val'][security.Issuer.value]=0.0
            self.temporaryIssuers['market_val'][security.Issuer.value] += security.market_val

            if security.Issuer.value not in self.temporaryIssuers['notional'].keys():
                self.temporaryIssuers['notional'][security.Issuer.value]=0.0
            self.temporaryIssuers['notional'][security.Issuer.value] += security.gross_custom_notional
        return


    def handleIlliquid(self,security):
        ## Calculates Liquidity Constraints - Portion of NAV Illiquid
        if security.Liquidity.illiquidFlag:
            self.calculations['illiquid_securities_market_val']+= np.abs(security.market_val)

    def handleRestricted(self,security):
        if security.Restricted.value:
            self.calculations['restricted_securities']+=security.gross_custom_notional

    def handleIndustry(self,security):

        ### Note : ETF (Check ETF Flag) and FX Excluded
        if isinstance(security,(FXCurrency,FXForward,FXFuture)) or security.IndexFlag.value or  security.ETFFlag.value:
            return

        ### Exposures by Industry
        if security.Industry.value != None and security.Industry.value != 'Other' and security.Industry.value != 'Suppress':

            if security.Industry.value not in self.temporaryIndustry['notional'].keys():
                self.temporaryIndustry['notional'][security.Industry.value]=0.0
                self.temporaryIndustry['market_val'][security.Industry.value]=0.0

            self.temporaryIndustry['notional'][security.Industry.value]+=security.gross_custom_notional
            self.temporaryIndustry['market_val'][security.Industry.value]+=security.market_val


    def handleSector(self,security):
    
        ### Note : ETF (Check ETF Flag) and FX Excluded
        if isinstance(security,(FXCurrency,FXForward,FXFuture)) or security.IndexFlag.value or  security.ETFFlag.value:
            return
            
        ### Exposures by Sector
        if security.Sector.value != None and security.Sector.value != 'Other' and security.Sector.value != 'Suppress':

            if security.Sector.value not in self.temporarySector['notional'].keys():
                self.temporarySector['notional'][security.Sector.value]=0.0
                self.temporarySector['market_val'][security.Sector.value]=0.0

            self.temporarySector['notional'][security.Sector.value]+=security.gross_custom_notional
            self.temporarySector['market_val'][security.Sector.value]+=security.market_val

    def handleCurrency(self,security):

        ### Need to Use Own Market Val because of Weird Mellon Rules
        fxModels = (FXCurrency,FXForward,FXFuture)

        ### Ignore Invalid Country Names  ### Don't Include Domestic Currency
        if security.Country.value != None:
            if 'united' not in  security.Country.value.lower() and 'states' not in security.Country.value.lower():

                ### Check if Instrument Type in List Designated for FX Types
                if isinstance(security,fxModels):
                    if security.Country.value not in self.temporaryCurrency.keys():
                        self.temporaryCurrency['market_val'][security.Country.value]=0.0
                        self.temporaryCurrency['notional'][security.Country.value]=0.0
                    
                    self.temporaryCurrency['market_val'][security.Country.value]+=security.market_val
                    self.temporaryCurrency['notional'][security.Country.value]+=security.gross_custom_notional

        return

    ### Override for some managers separately.
    def handleCommodityInterestPosition(self,security):
        ### Commodity Interest securitys
        if security.ComdtyInterestFlag.value:
            self.calculations['commodity_interest_notional']+=security.gross_custom_notional
            self.calculations['commodity_interest_market_val']+=security.market_val
            if isinstance(security, (BondOption,EquityOption)):
                self.calculations['commodity_interest_options_notional']+=security.gross_custom_notional
                self.calculations['commodity_interest_options_market_val']+=security.market_val

        return


    def handleInstrument(self,security):
    
        ### Check if Instrument Type is in List of Credit Derivative Instruments
        if isinstance(security, CreditDefaultSwap):
            self.calculations['credit_derivatives_notional']+=security.gross_custom_notional
            self.calculations['credit_derivatives_market_val']+=security.market_val

        ### Equity Futures
        elif isinstance(security, EquityFuture):
            self.calculations['equity_futures_notional']+=security.gross_custom_notional
            self.calculations['equity_futures_market_val']+=security.market_val

        #### Equity Options
        elif isinstance(security, EquityOption):
            self.calculations['equity_options_notional']+=security.gross_custom_notional
            self.calculations['equity_options_market_val']+=security.market_val
        ### FX Forwards
        elif isinstance(security, FXForward):
            self.calculations['currency_forwards_notional']+=security.gross_custom_notional
            self.calculations['currency_forwards_market_val']+=security.market_val

        ### TRS's
        elif isinstance(security, TRSBondLeg) or isinstance(security, TRSEquityLeg):
            self.calculations['total_return_swaps_notional']+=security.gross_custom_notional
            self.calculations['total_return_swaps_market_val']+=security.market_val

        return

    def handleNetBond(self,security):
        if isinstance(security,(Bond,BondOption,BondFuture)):
            self.calculations['bond_net_exposure_notional'] += security.net_custom_notional
            self.calculations['bond_net_exposure_market_val'] += security.market_val

    def handleNetEquity(self,security):
        if isinstance(security,(EquityOption,Equity,EquityFuture,EquityWarrant)):
            self.calculations['equity_net_exposure_notional'] += security.net_custom_notional
            self.calculations['equity_net_exposure_market_val'] += security.market_val


    def handleGeo(self,security):

        if security.MarketType.value == None or security.MarketType.value == 'Other' or security.MarketType.value == 'Suppress':
            return
        if security.Country.value == None or security.Country.value == 'Other' or security.Country.value == 'Suppress':
            return
        if security.Region.value == None or security.Region.value == 'Other' or security.Region.value == 'Suppress':
            return

        marketTypeDict = {'developed market':1,'emerging market':2,'frontier market':3}
        try:
            marketCode = marketTypeDict[security.MarketType.value.lower()]
        except KeyError:
            print 'Invaild Market Type Classification : ',security.MarketType.value,' for : ',security.SecurityName.value
            return

        #### Is Developed Not United States
        if 'united' not in security.Country.value.lower() and 'states' not in security.Country.value.lower():
            ### Developed Markets General (Includes US)
            if marketCode == 1:
                self.calculations['developed_europe_asia_non_us_notional'] += security.gross_custom_notional
                self.calculations['developed_europe_asia_non_us_market_val'] += security.market_val

            ### Max Single Non US Country Exposure
            if security.gross_custom_notional > self.calculations['non_us_single_country_notional']:
                self.calculations['non_us_single_country_notional'] = security.gross_custom_notional

            if security.market_val > self.calculations['non_us_single_country_market_val']:
                self.calculations['non_us_single_country_market_val'] = security.market_val

            ## Developed Markets Asia and Europe but Non US
            if 'euro' in security.Region.value.lower() or 'asia' in security.Region.value.lower():
                self.calculations['developed_europe_asia_non_us_notional'] += security.gross_custom_notional
                self.calculations['developed_europe_asia_non_us_market_val'] += security.market_val

                if 'euro' in security.Region.value.lower():
                    ### Developed Markets Non US but Europe
                    self.calculations['developed_europe_non_us_notional'] += security.gross_custom_notional
                    self.calculations['developed_europe_non_us_market_val'] += security.market_val


        ## Non Developed Markets General
        if marketCode == 1:
            self.calculations['developed_notional'] += security.gross_custom_notional
            self.calculations['developed_market_val'] += security.market_val

        elif marketCode == 2:
            self.calculations['emerging_notional'] += security.gross_custom_notional
            self.calculations['emerging_market_val'] += security.market_val
            self.calculations['non_developed_notional'] += security.gross_custom_notional
            self.calculations['non_developed_market_val'] += security.market_val

        elif marketCode == 3:
            self.calculations['frontier_notional'] += security.gross_custom_notional
            self.calculations['frontier_market_val'] += security.market_val
            self.calculations['non_developed_notional'] += security.gross_custom_notional
            self.calculations['non_developed_market_val'] += security.market_val
        return


    