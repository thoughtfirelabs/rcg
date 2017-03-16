from app.reporting_modules.tables.exposureReportTables import CategoryExposureTable
from ..lib.csvUtilities import csvResponse
from ..modules.portfolio_module import portfolio
from ..settings import ExposureReportSettings
from app.fields.fields import Fields
from app.fields.categorization import Categorization
#########################################################################
class ManagerExposureReport(ExposureReportSettings,portfolio,csvResponse):
    
    def __init__(self,portfolio_id,snapshot_date):
        
        self.portfolio_id = portfolio_id
        self.snapshot_date = snapshot_date
        self.categoryObjects = []
        
        self.dataSets = [] ### Series of Data Tables
        self.data = [] ### Array Format - Used by csvUtilities to Create CSV Response
        self.reportName = None
        self.numSpaceRows = 3

        ExposureReportSettings.__init__(self)
        portfolio.__init__(self,self.portfolio_id,self.snapshot_date)
        self.filename = str(self.portfolio_name.split(' ')[0])+'.csv'

        ### Get Portfolio Name for Report CSV
        self.reportName = self.portfolio_name
        csvResponse.__init__(self)
        return
    
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
        self.data.append([self.portfolio_name,' ',self.snapshot_date.strftime("%Y-%m-%d")])

        ### Generate Set of Category Object for Each Category Name
        self.categoryObjects = []
        for categoryName in self.categoryNames:

            ### Get Categorization Object from Field Object
            fieldObj = Fields.findStaticFieldObject(categoryName)
            catName = fieldObj.categorizationName
            print catName
            categorization = Categorization(catName)
            self.categoryObjects.append(categorization)
        
        ### Categorize Each Security and Generate Analysis
        for categoryObj in self.categoryObjects:
            categoryObj.categorize(self.securities)
            categoryObj.retrieveAnalysis()
            
            ## Use analyzed categorization to generate data table
            dataTable = CategoryExposureTable(categoryObj)
            dataTable.generate()
            
            self.dataSets.append(dataTable.data)
            self.data.extend(dataTable.data)
            self.space()
        return

