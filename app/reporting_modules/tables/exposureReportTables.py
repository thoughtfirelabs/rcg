from app.settings import  ExposureReportSettings

#########################################################################
### Specific Table Used to Show Exposure Breakdown of Managers
class FundManagerExposureTable(ExposureReportSettings):
	
	def __init__(self,categorization):

		self.ManagerColumns = ['Strategy','Allocation (%)','Long Exposure','Short Exposure','Gross Exposure','Net Exposure']
		ExposureReportSettings.__init__(self)

		self.categorization = categorization
		self.data = [] ### Data in Array Format for csvUtilities to Downloda
		self.columns = [' ']
		self.columns.extend(self.ManagerColumns)

	#################################
	def generate(self,fundNAV,portfolioNames,portfolioStrategies):
	 
		allocation = self.categorization.market_allocation
		netExp = self.categorization.delta_netNotionalNav
		shortExp = self.categorization.delta_shortNotionalNav
		longExp = self.categorization.delta_longNotionalNav
		grossExp = self.categorization.delta_grossNotionalNav

		desiredCols = [portfolioStrategies,allocation,longExp,shortExp,grossExp,netExp]
		self.data = []
		self.data.append(self.columns)
		 
		totals={} ## Indexed by Column Number
		for portID in self.managerIDOrder:
			 
			row = []
			row.append(portfolioNames[str(portID)])
			 
			for measType in desiredCols:
				 
				## Don't Include Totals for Strategy - First Column
				colCount = desiredCols.index(measType)
				if colCount == 0:
					addVal = str(measType[str(portID)])
				else:
				 
				 	### Initialize Add Val and Total Val = 0.0
					if str(portID) not in measType.keys():
						totalVal = 0.0
						addVal = 0.0
					else:
						### Total Val Same Regardless of use_category_na
						totalVal = measType[portID]
						 
						if colCount >= 2:
							navVal = measType[str(portID)]
							addVal = navVal * fundNAV / self.categorization.market_vals[str(portID)]
						else:
							addVal = measType[str(portID)]
						### Add Total Val to Dictionary Keeping Track of Totals
						if colCount not in totals.keys():
							totals[colCount]=0.0
						totals[colCount]+=totalVal
				row.append(addVal)
				
			self.data.append(row)

		### Include Total Row at Bottom
		lastRow = ['Portfolio',' ']
		lastRow.extend(list(totals.values()))
		self.data.append(lastRow)
		
		self.format()
		return

	#######################
	### Rounds and Formats Entries of Table to Percent String
	def format(self):
		for i in range(1,len(self.data)):
			row = self.data[i]
			### Loop Over Row Entries, Skip Row Label
			for j in range(2,len(row)):
				self.data[i][j]=round(self.data[i][j],5)
		return

#########################################################################
### Represents Category Breakdown Table for Single Manager or Subadvisor
class CategoryExposureTable(ExposureReportSettings):

	def __init__(self,categorization):

		ExposureReportSettings.__init__(self)

		self.categorization = categorization
		self.data = [] ### Data in Array Format for csvUtilities to Downloda

		self.columns = [' ']
		self.columns.extend(self.categoryTableColumnLabels)
		return

	######################
	##  Generates a Table from the Category Information
	def generate(self,market_allocation = None,use_category_nav = False, fundNAV = None):

		## Flag to use market allocation instead of gross notional allocation
		if market_allocation != None and market_allocation == True:
			allocation = self.categorization.market_allocation
		else:
			### Get Allocations and NAV Exposures from Category Object Associated with Portfolio
			allocation = self.categorization.delta_notional_allocation

		netExp = self.categorization.delta_netNotionalNav
		shortExp = self.categorization.delta_shortNotionalNav
		longExp = self.categorization.delta_longNotionalNav
		grossExp = self.categorization.delta_grossNotionalNav
		
		desiredCols = [allocation,longExp,shortExp,grossExp,netExp]

		### Exhaustive categories from ExposureReportSettings represent all the categories for the report,
		### regardless of whether or not that category name exists for the manager.
		allCats = self.exhaustiveCategories[self.categorization.fieldName]

		self.data = []
		## Include Columns
		self.data.append(self.columns)

		totals={} ## Indexed by Column Number
		colCount = 0
		for categoryname in allCats:

			### Row corresponding to Category Entry 
			row = []
			row.append(categoryname)

			### Loop Over desired Columns
			for measType in desiredCols:

				colCount = desiredCols.index(measType)

				### Initialize Add Val and Total Val = 0.0
				if categoryname not in measType.keys():
					totalVal = 0.0
					addVal = 0.0
				else:
					### Total Val Same Regardless of use_category_nav
					totalVal = measType[categoryname]
					if use_category_nav:
						### For NAV calculations, if the use_category_nav is specified
						### ### for strategy and manager tables, need to convert NAV to percent
						### of manager and strategy NAV instead of percent of Fund NAV
						if colCount > 0:
							navVal = measType[categoryname]
							addVal = navVal * fundNAV / self.categorization.market_vals[categoryname]
						else:
							addVal = measType[categoryname]
					else:
						addVal = measType[categoryname]

					### Add Total Val to Dictionary Keeping Track of Totals
					if colCount not in totals.keys():
						totals[colCount]=0.0
					totals[colCount]+=totalVal

				row.append(addVal)
			self.data.append(row)

		### Include Total Row at Bottom
		lastRow = ['Portfolio']
		lastRow.extend(list(totals.values()))
		self.data.append(lastRow)

		### Format the Data 
		self.format()
		return 

	#######################
	### Rounds and Formats Entries of Table to Percent String
	def format(self):

		### Loop Over Rows, Skip Headers
		for i in range(1,len(self.data)):
			row = self.data[i]
			### Loop Over Row Entries, Skip Row Label
			for j in range(1,len(row)):
				self.data[i][j]=round(self.data[i][j],5)
		return

