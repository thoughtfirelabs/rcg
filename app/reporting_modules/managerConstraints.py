class ConstraintSpecs:

        ### Constraints That Can Either Be Calculated Using Market Val % NAV or % Gross Exposure
        multiMeasureConstraints = ['single_security','single_issuer','top10_security','equity_options',
                                    'equity_futures','interest_rate_swaps','currency_forwards','total_return_swaps',
                                    'credit_derivatives','commodity_options','sector','industry']

        marketValOnlyConstraints = ['restricted_securities']

        allConstraints = {'single_security':'Maximum Single Security Position',
                        'single_issuer':'Maximum Single Issuer Exposure',
                        'top10_security':'Maximum Portfolio Concentration (Top 10 Positions)',

                        'restricted_securities':'Restricted Securities',
                        'max_outstanding_etf_shares':'ETF Limit - Max Percent of Outstanding Shares',
                        'illiquid_securities':'Illiquid Securities',

                        'short_exposure':'Short Custom Exposure',
                        'long_exposure':'Long Custom Exposure',
                        'short_exposure_excl_der':'Short Custom Exposure No Derivatives',
                        'long_exposure_excl_der':'Long Custom Exposure No Derivatives',
                        'gross_exposure':'Gross Custom Exposure',
                        'net_exposure':'Net Custom Exposure'

                        'equity_net_exposure':'Total Equity Net Exposure',
                        'bond_net_exposure':'Total Bond Net Exposure',
                        'currency_net_exposure':'Total Individual Currency Net Exposure',

                        'equity_options':'Exposure - Equity Options',
                        'equity_futures':'Exposure - Equity Futures',
                        'interest_rate_swaps':'Exposure - Interest Rate Swaps',
                        'currency_forwards':'Exposure - FX Forwards',
                        'total_return_swaps':'Exposure - Total Return Swaps',
                        'credit_derivatives':'Exposure - Credit Derivatives',
                        'commodity_interest':'Exposure - Commodity Interest Positions',

                        'beta_msci':'Beta MSCI ACWI',
                        'beta_sp500':'Beta S&P500'

                        'sector':'Max Exposure to Single Sector',
                        'industry':'Max Exposure to Single Industry',

                        'frontier':'Geographic Exposure Frontier Markets',
                        'emerging':'Geographic Exposure Emerging Markets',
                        'non_developed':'Geographic Exposure Non-Developed Markets'

                        'developed_non_us':'Geographic Exposure Developed Markets Non US',
                        'developed':'Geographic Exposure Developed Markets',

                        'developed_europe_non_us':'Geographic Exposure Developed Europe Non US',
                        'developed_europe_asia_non_us':'Geographic Exposure Developed Europe & Asia Non US',
                        'non_us_single_country':'Max Geographic Exposure to Single Country - Non US'}

    def __init__(self):



        return



#############################################################################
class ConstraintType:

    def __init__(self):

        self.formalName = ConstraintSpecs.allConstraints[self.name]

        if self.excludeDerivative:
            self.formalName += ' Excl Der.'

        if self.byMarketVal:
            self.formalName += ' by Market Val'

        self.byMarketVal, self.byExposure = False, True ### Default
        if self.name in ConstraintSpecs.multiMeasureConstraints:
            self.byMarketVal, self.byExposure = True, True 
        elif self.name in ConstraintSpecs.marketValOnlyConstraints
            self.byMarketVal, self.byExposure = True, False

        return



### Represents a Single Constraint Specification
class Constraint(ConstraintType):

    def __init__(self,name,upperValue=None,lowerValue=None,equalValue=None, byMarketVal = False, excludeDerivative = False):

        self.name = name
        ConstraintType.__init__(self)

        self.excludeDerivative = excludeDerivative
        self.byMarketVal = byMarketVal

        self.upperValue = upperValue 
        self.lowerValue = lowerValue
        self.equalValue = equalValue

###################################################
class ManagerConstraints:

    def __init__(self):
        self.flagRestricted = True ### Default
        self.prohibitedMarkets = []
        self.prohibitedSecurities = []

########## No Constraints Here
class AQRConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9740
        ManagerConstraints.__init__(self)
        return


### Canyon Sub Advisor Constraints
class CanyonConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9604
        ManagerConstraints.__init__(self)

        self.prohibitedMarkets = ['frontier','emerging']

        ##'total_return_swaps_gross_exposure':{'upper':0.30}, Previous Spec
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps']
        self.constraints = [ 

            Constraint('developed_europe_asia_non_us',upperValue = 0.30), 
            Constraint('single_security',upperValue = 0.05),
            Constraint('single_issuer',upperValue = 0.10), 
            Constraint('top10_security',upperValue = 0.60),

            Constraint('short_exposure',upperValue = 0.60),
            Constraint('long_exposure',upperValue = 1.0, excludeDerivative = True),
            Constraint('short_exposure',upperValue = 0.40, excludeDerivative = True),

            Constraint('gross_exposure',upperValue = 1.60),
            Constraint('net_exposure',upperValue = 1.0),

            Constraint('beta_sp500',upperValue = 0.75),

            Constraint('sector',upperValue = 0.45),
            Constraint('industry',upperValue = 0.25),

            Constraint('equity_options',upperValue = 0.05),
            Constraint('equity_futures',upperValue = 0.25),
            Constraint('credit_derivatives',upperValue = 0.40),

            Constraint('currency_forward',upperValue = 0.20),
            Constraint('credit_derivatives',upperValue = 0.40),

            Constraint('commodity_interest',upperValue = 1.05),

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('restricted_securities',upperValue = 1.00),
            Constraint('illiquid_securities',upperValue = 0.15),
        ]

        return


### Chilton Sub Advisor Constraints
class ChiltonConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9731
        ### Not allowed to trade options, warrants, futures, fixed income, swaps, privates and other things.
        ##  TO DO : Add More
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures','equity_options',
                                        'credit_derivatives']
        ### Include Warrants, Bond Options and Futures, Fixed Income
        self.constraints = [ 

            Constraint('developed_europe_asia_non_us',upperValue = 0.30), 
            Constraint('non_developed',upperValue = 0.10), 
            Constraint('single_issuer',upperValue = 0.15), 
            Constraint('single_security',upperValue = 0.15),
            Constraint('top10_security',upperValue = 0.65),

            Constraint('sector',upperValue = 0.40),
            Constraint('industry',upperValue = 0.25),

            Constraint('beta_sp500',upperValue = 0.75),

            Constraint('gross_exposure',upperValue = 2.4),
            Constraint('long_exposure',upperValue = 1.4),
            Constraint('short_exposure',upperValue = 1.0),

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.0)
        ]

        return



### Passport Sub Advisor Constraints
class PassportConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9591

        ### Can only engage in derivatives that are equity options or currency forwards
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures',
                                        'credit_derivatives']

         ### Include Warrants, Bond Options and Futures, Fixed Income
        self.constraints = [ 

            Constraint('non_developed',upperValue = 0.30), 

            Constraint('single_issuer',upperValue = 0.05),
            Constraint('single_issuer',upperValue = 0.10,  byMarketVal = True), 
            Constraint('single_security',upperValue = 0.05)
            Constraint('single_security',upperValue = 0.10,  byMarketVal = True),

            Constraint('top10_security',upperValue = 0.60),

            Constraint('sector',upperValue = 0.25),
            Constraint('industry',upperValue = 0.25),

            Constraint('beta_msci',upperValue = 0.70),

            Constraint('gross_exposure',upperValue = 1.5), ### Excel Doc says 2.3
            Constraint('long_exposure',upperValue = 1.0),
            Constraint('net_exposure',upperValue = 1.0, lowerValue = 0.0),

            ### Need to include with and without option constraints.
            Constraint('short_exposure',upperValue = 0.40),

            Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?
            Constraint('currency_forward',upperValue = 0.20),

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.05)
        ]
        return


### Mellon Sub Advisor Constraints
class MellonConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9733

        ### Include the currency forwards and options, other things in doc.
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps',
                                        'credit_derivatives']

         ### Can trade equity futures, options and currency forwards
        self.constraints = [ 

            Constraint('equity_net_exposure',upperValue = 0.65, lowerValue = -0.65),
            Constraint('bond_net_exposure',upperValue = 1.0, lowerValue = -1.0),
            Constraint('currency_net_exposure',upperValue = 0.8, lowerValue = -0.8),

            Constraint('non_developed',upperValue = 0.30), 

            Constraint('single_issuer',upperValue = 0.05),
            Constraint('single_issuer',upperValue = 0.10,  byMarketVal = True), 
            Constraint('single_security',upperValue = 0.05)
            Constraint('single_security',upperValue = 0.10,  byMarketVal = True),

            Constraint('top10_security',upperValue = 0.60),

            Constraint('sector',upperValue = 0.25),
            Constraint('industry',upperValue = 0.25),

            Constraint('beta_sp500',upperValue = 0.20),

            Constraint('gross_exposure',upperValue = 5.0), ### Excel Doc says 6.25
            Constraint('net_exposure',upperValue = 2.5, lowerValue = -2.5),

            Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?
            Constraint('equity_futures',upperValue = 0.20), ### Not sure if this is right, there might not be a spec for equity futures
            Constraint('commodity_interest',upperValue = 4.0), ### In excel sheet but not PDF Doc

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.00)
        ]

        return

### PineRiver Sub Advisor Constraints
class PineRiverConstraints(ManagerConstraints):


    def __init__(self):

        self.port_id = 10008

        self.prohibitedMarkets = ['frontier']

        ### Can only engage in common equity, preferred equity, options and ETFS
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures',
                                        'credit_derivatives']

         ### Include Warrants, Bond Options and Futures, Fixed Income
        self.constraints = [ 

            Constraint('non_us_single_country',upperValue = 0.20), 

            Constraint('single_issuer',upperValue = 0.20), 
            Constraint('single_security',upperValue = 0.15) ## Market val or gross notional?
            Constraint('top10_security',upperValue = 0.50),

            Constraint('sector',upperValue = 0.35),
            Constraint('industry',upperValue = 0.25),

            Constraint('beta_sp500',upperValue = 0.20),

            ### Exclusion of Derivatives Means Options
            Constraint('gross_exposure',upperValue = 2.85),

            Constraint('long_exposure',upperValue = 1.35, excludeDerivative = True),
            Constraint('long_exposure',upperValue = 1.50)

            Constraint('short_exposure',upperValue = 1.50, excludeDerivative = True),
            Constraint('short_exposure',upperValue = 1.50)

            Constraint('net_exposure',upperValue = 0.20, lowerValue = -0.20),

            Constraint('equity_futures',upperValue = 0.15),
            Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?
            Constraint('currency_forward',upperValue = 0.30),

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.10)
        ]

        return


### PineRiver Sub Advisor Constraints
class SiriosConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9512
        ### PDF says emerging as well, but the excel does doesn't exclude emerging markets.
        self.prohibitedMarkets = ['frontier']
        ### Can only engage in common equity, preferred equity, options and ETFS
        self.prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures',
                                        'credit_derivatives']

         ### Include Warrants, Bond Options and Futures, Fixed Income
        self.constraints = [ 

            Constraint('developed_europe_asia_non_us',upperValue = 0.35), ### PDF says 0.30
            Constraint('emerging',upperValue = 0.20), 

            Constraint('single_issuer',upperValue = 0.10, byMarketVal = True), 
            Constraint('single_security',upperValue = 0.10, byMarketVal = True),
            Constraint('top10_security',upperValue = 0.50),

            Constraint('sector',upperValue = 0.40),
            Constraint('industry',upperValue = 0.25),

            ### Excel Doc Says Irrelevant
            Constraint('beta_sp500',upperValue = 0.90),

            ### Exclusion of Derivatives Means Options
            Constraint('gross_exposure',upperValue = 1.60),

            Constraint('long_exposure',upperValue = 1.00, excludeDerivative = True),
            Constraint('long_exposure',upperValue = 1.40)

            Constraint('short_exposure',upperValue = 0.40, excludeDerivative = True),
            Constraint('short_exposure',upperValue = 0.60)

            Constraint('net_exposure',upperValue = 1.00, lowerValue = 0.0),

            Constraint('equity_options',upperValue = 0.35), ### PDF Different
            Constraint('currency_forward',upperValue = 0.35), ### PDF Different

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.00)
        ]

        return

### Wellington Sub Advisor Constraints
class WellingtonConstraints(ManagerConstraints):

    def __init__(self):

        self.port_id = 9408
        ### PDF says emerging as well, but the excel does doesn't exclude emerging markets.
        self.prohibitedMarkets = []
        ### Can only engage in common equity, preferred equity, options and ETFS
        self.prohibitedSecurities = ['credit_derivatives','interest_rate_swaps']

         ### Include Warrants, Bond Options and Futures, Fixed Income
        self.constraints = [ 

            Constraint('single_issuer',upperValue = 0.08, byMarketVal = True), 
            Constraint('single_security',upperValue = 0.08, byMarketVal = True), 
            Constraint('top10_security',upperValue = 0.50),

            Constraint('sector',lowerValue = -0.20, upperValue = 0.20, excludeDerivative = True), ### Discrepancy, this is a slightly modified measurement compared to other managers.
            Constraint('industry',upperValue = 0.25),

            ### Excel Doc Says Irrelevant
            Constraint('beta_sp500',lowerValue = 0.30,upperValue = 0.60),

            ### Exclusion of Derivatives Means Options
            Constraint('gross_exposure',upperValue = 3.50),

            Constraint('long_exposure',upperValue = 1.00, excludeDerivative = True),
            Constraint('long_exposure',upperValue = 2.00)

            Constraint('short_exposure',upperValue = 0.75, excludeDerivative = True),
            Constraint('short_exposure',upperValue = 2.00)

            Constraint('net_exposure',upperValue = 1.00, lowerValue = 0.0),

            Constraint('equity_options',upperValue = 1.00), ### PDF says exposure less than 20%
            Constraint('equity_futures',upperValue = 1.00),
            Constraint('total_return_swaps',upperValue = 0.35), 

            Constraint('max_outstanding_etf_shares',upperValue = 0.03),
            Constraint('illiquid_securities',upperValue = 0.10)
        ]

        return
