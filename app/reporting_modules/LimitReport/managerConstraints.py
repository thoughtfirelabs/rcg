from app.reporting_modules.LimitReport.constraintModels import Constraint
from app.reporting_modules.LimitReport.managerConstraintCalculation import ManagerConstraintCalculation
from app.modules.portfolio_module import portfolio
from app.reporting_modules.LimitReport.constraintModels import ExhaustiveConstraints
from app.models.securityModels import EquityFuture, CreditDefaultSwap, EquityOption, FXForward, TRSBondLeg, TRSEquityLeg, FXCurrency, Equity, FXFuture, EquityWarrant, BondOption, BondFuture, Bond
###################################################
### General Manager Constraints Object That is Inherited by All Separate Constraint Objects
class ManagerConstraints(ExhaustiveConstraints):

	def __init__(self):

		self.flagRestricted = True ### Default
		self.prohibitedMarkets = []
		self.prohibitedSecurities = []

		ExhaustiveConstraints.__init__(self)

	## Formal Name for Manager/Portfolio for Table (Not the entire sub advisor name)
	@property
	def formalName(self):

		formalName = self.portfolio_name
		if '-' in self.portfolio_name:
			self.portfolio_name.replace('-','')
		if 'sub advisor' in self.portfolio_name.lower():
			formalName = self.portfolio_name.lower().split('sub advisor')[0].title()
		if 'sub' in self.portfolio_name.lower():
			formalName = self.portfolio_name.lower().split('sub')[0].title()
		return formalName

	### This may return None if there is no constraint for this manager.
	def constraintForID(self,id):
		for constraint in self.constraints:
			if constraint.id == id:
				return constraint
		return None

	### This should never return none, there shoudl always be a reference present.
	def referenceForID(self,id):
		foundRef = None
		for reference in self.exhaustiveReferences:
			if reference.id == id:
				foundRef = reference
				return foundRef
		assert foundRef != None 
		return

	### Stores calculated value to constraint and reference if applicable.
	def storeValue(self,id,value):

		constraint = self.constraintForID(id)
		if constraint != None:
			constraint.value = value

		ref = self.referenceForID(id)
		ref.value = value
		return

	def evaluateConstraints(self):
		for constraint in self.constraints:
			constraint.eval()
			if constraint.breached:
				print 'Breach : '+constraint.id+' for : ',self.port_id
		return

	### Make Calculations and Evaluate Constaints
	def evaluate(self):
		self.run()  ### Create portfolio and sift through securities
		if self.date_error:
			print 'Date Error for Portfolio : ',self.portfolio_id,' on Date : ',self.snapshot_date
			return
		self.performCalculations() ### Make Necessary Calculations
		self.evaluateConstraints()
		return

	### To Do: Can include more data in this response dictionary for later.
	def serialize(self):

		data = {}
		data['port_id']=self.port_id
		data['portfolio_name']=self.formalName
		data['evaluation']={}

		### Loop over references, references is all inclusive, check each
		### reference to see if it is also an applicable constraint for the manager.
		for ref in self.exhaustiveReferences:

			data['evaluation'][ref.id]={}
			data['evaluation'][ref.id]['formalName']=ref.formalName
			data['evaluation'][ref.id]['grouping']=ref.grouping

			### Overwritten if Applicable
			data['evaluation'][ref.id]['applicable'] = False
			data['evaluation'][ref.id]['value']=ref.value

			### Check if the manager has the given constraint
			constraint = self.constraintForID(ref.id)
			
			if constraint != None:
		
				data['evaluation'][ref.id]['applicable'] = True
				data['evaluation'][ref.id]['value']=constraint.value
				data['evaluation'][ref.id]['breached']=constraint.breached

				data['evaluation'][ref.id]['upperBound']=constraint.upperValue
				data['evaluation'][ref.id]['lowerBound']=constraint.lowerValue
				data['evaluation'][ref.id]['equalBound']=constraint.equalValue

		return data

	
########## No Constraints Here
class AQRConstraints(ManagerConstraints):

	def __init__(self):

		self.port_id = 9740
		ManagerConstraints.__init__(self)
		return


###################################################################################
class CanyonConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9604
	prohibitedMarkets = ['frontier','emerging']
	##'total_return_swaps_gross_exposure':{'upper':0.30}, Previous Spec
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps']

	def __init__(self,snapshot_date):

		self.constraints = [ 

			Constraint('developed_europe_asia_non_us', upperValue=0.30), 
			Constraint('single_security',upperValue = 0.10, marketValue=True),
			Constraint('single_issuer',upperValue = 0.15, marketValue=True), 
			Constraint('top10_security',upperValue = 0.60),

			Constraint('emerging',equalValue = 0.0),
			Constraint('frontier',equalValue = 0.0),

			Constraint('short_exposure',upperValue = 0.60),
			Constraint('short_exposure',upperValue = 0.40, excludeDerivative = True),

			Constraint('long_exposure',upperValue = 1.4),
			Constraint('long_exposure',upperValue = 1.0, excludeDerivative = True),
			
			Constraint('gross_exposure',upperValue = 1.60),
			Constraint('net_exposure',upperValue = 1.0),

			Constraint('beta_sp500',upperValue = 0.75,override_id = 'beta_sp500'),

			Constraint('sector',upperValue = 0.45),
			Constraint('industry',upperValue = 0.25),

			Constraint('equity_options',upperValue = 0.5),
			Constraint('equity_futures',upperValue = 0.25),
			Constraint('credit_derivatives',upperValue = 0.30),

			Constraint('interest_rate_swaps',upperValue = 0.20), ### Need to implement
			Constraint('total_return_swaps',upperValue = 0.30),
			Constraint('currency_forwards',upperValue = 0.30),

			Constraint('commodity_interest',equalValue = 1.05),

			Constraint('commodity_interest_options',equalValue = 0.0),
			Constraint('commodity_interest_options',equalValue = 0.0,marketValue=True),

			Constraint('max_outstanding_etf_shares',upperValue = 0.03, override_id = 'max_outstanding_etf_shares'),
			Constraint('restricted_securities',upperValue = 1.00, override_id = 'restricted_securities'),
			Constraint('illiquid_securities',upperValue = 0.15, override_id = 'illiquid_securities'),
		]

		portfolio.__init__(self,CanyonConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)
		
		return

	### Override for Base Commodity Interest Calculation
	### Need to include interest rate swaps
	def handleCommodityInterestPosition(self,security):
		## Canyon defines commodity interest positions as equity index futures,credit derivatives, interest rate swaps 
		## and total returns on indices
		if isinstance(security,(EquityFuture,CreditDefaultSwap,TRSEquityLeg)):
			if security.IndexFlag.value:
				self.calculations['commodity_interest_notional']+=security.gross_custom_notional
				self.calculations['commodity_interest_market_val']+=security.market_val

		### Not sure if this is right : 
		if isinstance(security, (BondOption,EquityOption)):
			self.calculations['commodity_interest_options_notional']+=security.gross_custom_notional
			self.calculations['commodity_interest_options_market_val']+=security.market_val

		return

###################################################################################
class ChiltonConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9731
	prohibitedMarkets = []
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures','equity_options',
										'credit_derivatives']

	def __init__(self,snapshot_date):

		### Include Warrants, Bond Options and Futures, Fixed Income
		self.constraints = [ 

			Constraint('developed_europe_asia_non_us',upperValue = 0.30), ### Change to general Non US Exposure
			Constraint('non_developed',upperValue = 0.10), 
			Constraint('single_issuer',upperValue = 0.15, marketValue=True), ### Excluding ETFS and Indices
			Constraint('single_security',upperValue = 0.15, marketValue=True),
			Constraint('top10_security',upperValue = 0.65),

			Constraint('sector',upperValue = 0.40),
			Constraint('industry',upperValue = 0.25),

			Constraint('beta_sp500',upperValue = 0.75,override_id = 'beta_sp500'),

			Constraint('gross_exposure',upperValue = 2.4),
			Constraint('long_exposure',upperValue = 1.4),
			Constraint('short_exposure',upperValue = 1.0),
			Constraint('net_exposure',upperValue = 1.0, lowerValue=0.0),

			Constraint('currency_forwards',upperValue = 0.3),

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.0,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,ChiltonConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)
		

		return

###################################################################################
class PassportConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9591
	prohibitedMarkets = []
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures',
										'credit_derivatives']

	def __init__(self,snapshot_date):

		 ### Include Warrants, Bond Options and Futures, Fixed Income
		self.constraints = [ 

			Constraint('non_developed',upperValue = 0.30), 

			Constraint('single_issuer',upperValue = 0.10,  marketValue = True), 
			Constraint('single_security',upperValue = 0.10,  marketValue = True),

			Constraint('top10_security',upperValue = 0.60),

			Constraint('sector',upperValue = 0.35),
			Constraint('industry',upperValue = 0.25),

			Constraint('beta_msci',upperValue = 0.70,override_id = 'beta_msci'),

			Constraint('gross_exposure',upperValue = 2.3), 
			Constraint('long_exposure',upperValue = 1.3),
                    Constraint('long_exposure',upperValue = 1.0, excludeDerivative = True),
                    Constraint('short_exposure',upperValue = 1.0),
                    Constraint('short_exposure',upperValue = 0.4, excludeDerivative = True),
			Constraint('net_exposure',upperValue = 1.0, lowerValue = 0.0),

			Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?
			Constraint('currency_forwards',upperValue = 0.20),

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.05,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,PassportConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)

		return

###################################################################################
class MellonConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9733
	prohibitedMarkets = []
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps',
										'credit_derivatives']

	def __init__(self,snapshot_date):

		 ### Can trade equity futures, options and currency forwards
		self.constraints = [ 

			Constraint('equity_net_exposure',upperValue = 0.65, lowerValue = -0.65),
			Constraint('bond_net_exposure',upperValue = 1.0, lowerValue = -1.0),

			Constraint('max_single_currency',upperValue = 0.8),
			Constraint('min_single_currency',lowerValue = -0.8),

			Constraint('gross_exposure',upperValue = 6.25), 
			Constraint('net_exposure',upperValue = 2.5, lowerValue = -2.5),

			Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?

			### Commodity Interest Positions
			Constraint('equity_futures',upperValue = 4.0), 
			###Constraint('bond_futures',upperValue = 4.0), ## Need to add in
			Constraint('commodity_interest',upperValue = 4.0), 

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.00,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,MellonConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)

		return

###################################################################################
class PineRiverConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 10008
	prohibitedMarkets = ['frontier']
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps',
										'credit_derivatives']

	def __init__(self,snapshot_date):

		 ### Include Warrants, Bond Options and Futures, Fixed Income
		self.constraints = [ 

			Constraint('non_us_single_country',upperValue = 0.20), 

			Constraint('single_issuer',upperValue = 0.20), 
			Constraint('single_security',upperValue = 0.15), ## Market val or gross notional?
			Constraint('top10_security',upperValue = 0.50),

			Constraint('sector',upperValue = 0.35),
			Constraint('industry',upperValue = 0.25),

			Constraint('beta_sp500',upperValue = 0.20,override_id = 'beta_sp500'),

			### Exclusion of Derivatives Means Options
			Constraint('gross_exposure',upperValue = 2.85),

			Constraint('long_exposure',upperValue = 1.35, excludeDerivative = True),
			Constraint('long_exposure',upperValue = 1.50),

			Constraint('short_exposure',upperValue = 1.50, excludeDerivative = True),
			Constraint('short_exposure',upperValue = 1.50),

			Constraint('net_exposure',upperValue = 0.20, lowerValue = -0.20),

			Constraint('equity_futures',upperValue = 0.15),
			Constraint('equity_options',upperValue = 0.20), ### NAV or Gross?
			Constraint('currency_forwards',upperValue = 0.30),

			### No Swaps
			Constraint('total_return_swaps',equalValue = 0.0), 
			Constraint('interest_rate_swaps',equalValue = 0.0), 

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.10,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,PineRiverConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)

		return


###################################################################################
class SiriosConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9512
	prohibitedMarkets = ['frontier']
	prohibitedSecurities = ['total_return_swaps','interest_rate_swaps','equity_futures',
										'credit_derivatives']

	def __init__(self,snapshot_date):

		 ### Include Warrants, Bond Options and Futures, Fixed Income
		self.constraints = [ 

			Constraint('developed_europe_asia_non_us',upperValue = 0.35), ### PDF says 0.30
			Constraint('emerging',upperValue = 0.20), 

			Constraint('single_issuer',upperValue = 0.15, marketValue = True), 
			Constraint('single_security',upperValue = 0.10, marketValue = True),
			Constraint('top10_security',upperValue = 0.60),

			Constraint('sector',upperValue = 0.40),
			Constraint('industry',upperValue = 0.25),

			### Excel Doc Says Irrelevant
			Constraint('beta_sp500',upperValue = 0.90,override_id = 'beta_sp500'),

			### Exclusion of Derivatives Means Options
			Constraint('gross_exposure',upperValue = 1.60),

			Constraint('long_exposure',upperValue = 1.00, excludeDerivative = True),
			Constraint('long_exposure',upperValue = 1.40),

			Constraint('short_exposure',upperValue = 0.40, excludeDerivative = True),
			Constraint('short_exposure',upperValue = 0.60),

			Constraint('net_exposure',upperValue = 1.00, lowerValue = 0.0),

			Constraint('equity_options',upperValue = 0.35), ### PDF Different
			Constraint('currency_forwards',upperValue = 0.35), ### PDF Different

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.00,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,SiriosConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)

		return

###################################################################################
class WellingtonConstraints(portfolio,ManagerConstraints,ManagerConstraintCalculation):

	port_id = 9408
	prohibitedMarkets = []
	prohibitedSecurities = ['credit_derivatives','interest_rate_swaps']

	def __init__(self,snapshot_date):
		### Include Warrants, Bond Options and Futures, Fixed Income
		self.constraints = [ 

			Constraint('single_issuer',upperValue = 0.08, marketValue = True), 
			Constraint('single_security',upperValue = 0.08, marketValue = True), 
			Constraint('top10_security',upperValue = 0.50),

			Constraint('sector',lowerValue = -0.20, upperValue = 0.20, excludeDerivative = True), ### Discrepancy, this is a slightly modified measurement compared to other managers.
			Constraint('industry',upperValue = 0.25),

			### Excel Doc Says Irrelevant
			Constraint('beta_msci',lowerValue = 0.20,upperValue = 0.60,override_id = 'beta_sp500'),

			### Exclusion of Derivatives Means Options
			Constraint('gross_exposure',upperValue = 3.50),

			Constraint('long_exposure',upperValue = 1.00, excludeDerivative = True),
			Constraint('long_exposure',upperValue = 2.00),

			Constraint('short_exposure',upperValue = 0.75, excludeDerivative = True),
			Constraint('short_exposure',upperValue = 2.00),

			Constraint('net_exposure',upperValue = 1.00, lowerValue = 0.0),

			Constraint('equity_options',upperValue = 1.00), 

					### Equity Futures and Total Swaps Bucketed into Same Category
			Constraint('equity_futures',upperValue = 1.00),
			Constraint('total_return_swaps',upperValue = 0.35), 

			Constraint('max_outstanding_etf_shares',upperValue = 0.03,override_id = 'max_outstanding_etf_shares'),
			Constraint('illiquid_securities',upperValue = 0.10,override_id = 'illiquid_securities')
		]

		portfolio.__init__(self,WellingtonConstraints.port_id,snapshot_date)
		ManagerConstraintCalculation.__init__(self)
		ManagerConstraints.__init__(self)
		

		return














