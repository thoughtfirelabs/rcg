from app.reporting_modules.tables.exposureReportTables import CategoryExposureTable, FundManagerExposureTable
from ..lib.csvUtilities import csvResponse
from ..modules.fund_module import fund
from ..settings import ExposureReportSettings
from app.fields.fields import Fields
from app.fields.categorization import Categorization
###################################################################################
class ExposureReport(ExposureReportSettings,fund,csvResponse):

    def __init__(self,fund_id,snapshot_date):

        self.fund_id = fund_id
        self.snapshot_date = snapshot_date
        self.categoryObjects = []
        
        self.dataSets = [] ### Series of Data Tables
        self.data = [] ### Array Format - Used by csvUtilities to Create CSV Response
        self.reportName = None
        self.numSpaceRows = 3

        ExposureReportSettings.__init__(self)
        fund.__init__(self,self.fund_id,self.snapshot_date)
        self.filename = str(self.fund_name.split(' ')[0])+'.csv'

        ### Get Portfolio Name for Report CSV
        self.reportName = self.fund_name
        csvResponse.__init__(self)

    #######################
    ### Applies Spacing
    def space(self):
        for i in range(self.numSpaceRows):
            self.data.append([])
        return
    #######################
    ### Generates Data Tables for Each Category
    def generate(self):

        self.run()
        ### Give Dataset Top Row
        self.data.append([self.fund_name,' ',self.snapshot_date.strftime("%Y-%m-%d")])

        ### First generate manager table
        ### Get Categorization Object from Field Object
        fieldObj = Fields.findStaticFieldObject('portfolio_id')
        catName = fieldObj.categorizationName
        categorization = Categorization(catName)
        
        categorization.categorize(self.securities)
        categorization.retrieveAnalysis()

        managerTable = FundManagerExposureTable(categorization)
        
        ### Get Portfolio Attributes from Fund
        portfolioStrategies = {}
        portfolioNames = {}
        for port_id in self.portfolios.keys():
            portfolio = self.portfolios[str(port_id)]
            portfolioNames[str(port_id)]=str(portfolio.portfolio_name)
            portfolioStrategies[str(port_id)]=str(portfolio.strategy)

        managerTable.generate(self.market_val,portfolioNames,portfolioStrategies) ### Pass In Fund NAV to Generate Manager Table

        self.dataSets.append(managerTable.data)
        self.data.extend(managerTable.data)
        self.space()
        
        ### Add Strategy to Category Names and Generate Other Category Tables
        categories = self.categoryNames[:]
        categories.insert(0,'strategy')
        
        self.categoryObjects = []
        ### Generate Data Table for Each Category
        for categoryName in categories:
            
            ### Get Categorization Object from Field Object
            fieldObj = Fields.findStaticFieldObject(categoryName)
            catName = fieldObj.categorizationName
            categorization = Categorization(catName)
            self.categoryObjects.append(categorization)
    
        ### Categorize Each Security and Generate Analysis
        for categoryObj in self.categoryObjects:
            categoryObj.categorize(self.securities)
            categoryObj.retrieveAnalysis()
            
            categoryName = categoryObj.fieldName
            ## Use analyzed categorization to generate data table
            dataTable = CategoryExposureTable(categoryObj)

            print '########################'
            print categoryName
            ### Generate Table of Exposures from Category
            if 'strategy' in categoryName.lower():
                dataTable.generate(market_allocation=True,use_category_nav = True, fundNAV = self.market_val)
            else:
                dataTable.generate()
                
            self.dataSets.append(dataTable.data)
            self.data.extend(dataTable.data)
            self.space()
            
        return
