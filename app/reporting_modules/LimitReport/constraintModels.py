
constraintFormalNames = {'single_security':'Max Single Security',
                        'single_issuer':'Max Single Issuer',
                        'top10_security':'Max Top 10 Concentration',

                        'restricted_securities':'Restricted Securities',
                        'max_outstanding_etf_shares':'ETF Limit',
                        'illiquid_securities':'Illiquid Securities',

                        'short_exposure':'Short Exposure',
                        'long_exposure':'Long Exposure',
                        'gross_exposure':'Gross Exposure',
                        'net_exposure':'Net Exposure',

                        'equity_net_exposure':'Equity Net Exposure',
                        'bond_net_exposure':'Bond Net Exposure',
                        'max_single_currency':'Max Exposure Single Currency',
                        'min_single_currency':'Min Exposure Single Currency',

                        'equity_options':'Equity Options',
                        'equity_futures':'Equity Futures',
                        'interest_rate_swaps':'Interest Rate Swaps',
                        'currency_forwards':'FX Forwards',
                        'total_return_swaps':'Total Return Swaps',
                        'credit_derivatives':'Credit Derivatives',
                        'commodity_interest':'Commodity Interest Positions',
                        'commodity_interest_options':'Options on Commodity Int. Pos.',

                        'beta_msci':'Beta MSCI ACWI',
                        'beta_sp500':'Beta S&P500',

                        'sector':'Max Exposure to Single Sector',
                        'industry':'Max Exposure to Single Industry',

                        'frontier':'Frontier Markets',
                        'emerging':'Emerging Markets',
                        'non_developed':'Non-Developed Markets',

                        'developed_non_us':'Developed Markets Non US',
                        'developed':'Developed Markets',

                        'developed_europe_non_us':'Developed Europe Non US',
                        'developed_europe_asia_non_us':'Developed Europe & Asia Non US',
                        'non_us_single_country':'Max Exposure to Single Country - Non US'}

###################################################################################
class ConstraintIdentifier:

    notionalValueAddOn = ' (Exposure/NAV)'
    marketValueAddOn = ' (Market Value/NAV)'
    noDerivativeAddOn = ' Excl. Derv.'

    def __init__(self):
        return
    def generateID(self):
        self.id = self.type ## Ex: industry_notional or sector_market_val
        if self.notional:
            self.id += '_notional'
        if self.marketValue and not self.notional:
            self.id += '_market_val'
        if self.excludeDerivative:
            self.id += '_noderivative'
    @property
    def formalName(self):

        ### Format the Formal Name
        formalName = constraintFormalNames[self.type]
        if self.notional:
            formalName += ConstraintIdentifier.notionalValueAddOn
        elif self.marketValue:
            formalName += ConstraintIdentifier.marketValueAddOn

        if self.excludeDerivative:
            formalName += ConstraintIdentifier.noDerivativeAddOn

        return formalName

###################################################################################
class ConstraintEvaluation:

    def __init__(self,upperValue = None, lowerValue = None, equalValue = None):
        self.upperValue = upperValue
        self.lowerValue = lowerValue
        self.equalValue = equalValue
        self.breached = False 
        return

    ### Evaluates Constraint to See if it Falls Within Bounds 
    def eval(self):
        ### If equal value specified, this is the only thing we care about.
        if self.equalValue != None and round(self.equalValue,2) != round(self.value,2):
            self.breached = True
            return
        
        if self.lowerValue != None and self.value < self.lowerValue:
            self.breached = True
        if self.upperValue != None and self.value > self.upperValue:
            self.breached = True
        return



### Represents a Single Constraint Specification with Identifier and Formal Names
### Does not necessarily represent the constraint quantiative limits that must be evaluated.
### This is referenced from both constraints that we want to evaluate and actual constraints
### with numbers with manager.
class Constraint(ConstraintIdentifier,ConstraintEvaluation):

    def __init__(self, type, upperValue=None, lowerValue=None, equalValue=None, notional=True, marketValue=False, excludeDerivative=False, override_id = None):

        self.type = type
        self.formalName = constraintFormalNames[self.type]
        self.id = None ## Ex: industry_notional or sector_market_val
        self.value = None

        self.notional = notional ### Defaults to True
        self.marketValue = marketValue
        if self.marketValue:
            self.notional = False

        self.excludeDerivative = excludeDerivative

        ConstraintEvaluation.__init__(self,upperValue = upperValue, lowerValue = lowerValue, equalValue = equalValue)
        ConstraintIdentifier.__init__(self)

        if override_id == None:
            self.generateID()
        else:
            self.id = override_id


#### Same thing as a constraint but without the Evaluation
class ConstraintReference(ConstraintIdentifier):

    def __init__(self, type, notional=True, marketValue=False, excludeDerivative=False):

        self.type = type
        self.id = None ## Ex: industry_notional or sector_market_val
        self.value = None 
        self.grouping = None
        
        self.notional = notional ### Defaults to True
        self.marketValue = marketValue
        if self.marketValue:
            self.notional = False

        self.excludeDerivative = excludeDerivative
        ConstraintIdentifier.__init__(self)

    def identify(self):
        self.generateID()


#############################################################################
### Reference of a Constraint That We Want to Analyze for Each Manager
class ConstraintGroupReference:

    def __init__(self, type, grouping = None, notional = False, marketValue = False, excludeDerivative = False, override_id = None):

        self.type = type

        self.override_id = override_id
        self.excludeDerivative = excludeDerivative
        self.notional = notional
        self.marketValue = marketValue

        self.grouping = grouping
        if self.grouping == None:
            self.grouping = 'general'

    ### Returns a list of references with each one directly analogous to a constraint object.
    def generateReferences(self):

        references = []

        if self.override_id != None:

            newRef = ConstraintReference(self.override_id,notional=False,marketValue=False)
            newRef.id = self.override_id
            newRef.grouping = self.grouping
            references.append(newRef)

            return [newRef]

        ### Generate Notional Constraint Ref
        if self.notional:

            newRef = ConstraintReference(self.type)
            newRef.identify()
            newRef.grouping = self.grouping
            references.append(newRef)

            if self.excludeDerivative:
                newRef = ConstraintReference(self.type,excludeDerivative = True)
                newRef.grouping = self.grouping
                newRef.identify()
                references.append(newRef)

        ### Generate Market V Constraint Ref
        if self.marketValue:

            newRef = ConstraintReference(self.type,notional=False,marketValue=True)
            newRef.identify()
            newRef.grouping = self.grouping
            references.append(newRef)

            if self.excludeDerivative:

                newRef = ConstraintReference(self.type,notional=False,marketValue=True, excludeDerivative = True)
                newRef.identify()
                newRef.grouping = self.grouping
                references.append(newRef)

        ### Miscelanneous Constraint (Like betas)
        if not self.marketValue and not self.notional:
            newRef = ConstraintReference(self.type,notional=False,marketValue=False)
            newRef.grouping = self.grouping
            newRef.identify()
            return [newRef]

        return references

###################################################
### Represents All Constraints That We Want in Limit Report
class ExhaustiveConstraints:

    ### Want to get a complete list of all possible constraint references so that we can include those calculations
    ### even if they are not directly applicable to that manager.
    referenceGroups = [ConstraintGroupReference('single_security',notional=True, marketValue=True, grouping='concentration'),
                        ConstraintGroupReference('single_issuer',notional=True, marketValue=True, grouping='concentration'),
                        ConstraintGroupReference('top10_security',notional=True, marketValue=True, grouping='concentration'),

                        ConstraintGroupReference('short_exposure',notional=True, excludeDerivative = True),
                        ConstraintGroupReference('long_exposure',notional=True, excludeDerivative = True),
                        ConstraintGroupReference('gross_exposure',notional=True, excludeDerivative = True),
                        ConstraintGroupReference('net_exposure',notional=True, excludeDerivative = True),

                        ConstraintGroupReference('beta_sp500',grouping='beta',override_id = 'beta_sp500'),
                        ConstraintGroupReference('beta_msci', grouping='beta',override_id = 'beta_msci'),

                        ConstraintGroupReference('sector',notional=True, marketValue=True, grouping='sector_industry'),
                        ConstraintGroupReference('industry',notional=True, marketValue=True, grouping='sector_industry'),

                        ConstraintGroupReference('frontier',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('emerging',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('non_developed',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('developed',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('developed_europe_non_us',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('developed_europe_asia_non_us',notional=True, marketValue=True, grouping='geo'),
                        ConstraintGroupReference('non_us_single_country',notional=True, marketValue=True, grouping='geo'),

                        ConstraintGroupReference('restricted_securities',grouping='misc',override_id = 'restricted_securities'),
                        ConstraintGroupReference('max_outstanding_etf_shares',grouping='misc',override_id = 'max_outstanding_etf_shares'),
                        ConstraintGroupReference('illiquid_securities',grouping='misc',override_id = 'illiquid_securities'),

                        ConstraintGroupReference('equity_net_exposure',notional=True,marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('bond_net_exposure',notional=True,marketValue=True,grouping='instrument'),

                        ConstraintGroupReference('max_single_currency',notional=True,marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('min_single_currency',notional=True,marketValue=True, grouping='instrument'),

                        ConstraintGroupReference('equity_options',notional=True, marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('equity_futures',notional=True, marketValue=True,  grouping='instrument'),
                        ConstraintGroupReference('interest_rate_swaps',notional=True,marketValue=True,  grouping='instrument'),
                        ConstraintGroupReference('currency_forwards',notional=True,marketValue=True,  grouping='instrument'),
                        ConstraintGroupReference('total_return_swaps',notional=True, marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('commodity_interest',notional=True, marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('commodity_interest_options',notional=True, marketValue=True, grouping='instrument'),
                        ConstraintGroupReference('credit_derivatives',notional=True, marketValue=True, grouping='instrument'),
            ]

    def __init__(self):
        self.exhaustiveReferences = []
        self.initializeReferences()
        return

    def initializeReferences(self):
        for group in ExhaustiveConstraints.referenceGroups:
            self.exhaustiveReferences.extend(group.generateReferences())
        return 







