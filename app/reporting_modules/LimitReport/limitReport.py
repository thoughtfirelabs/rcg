from app.reporting_modules.LimitReport.managerConstraints import CanyonConstraints,ChiltonConstraints,PassportConstraints,MellonConstraints,PineRiverConstraints,SiriosConstraints,WellingtonConstraints
#################################################################################
### Limit Report for All Managers in Fund
class LimitReport:
    
    categoryFormalNames = {'geo':'Geographical Exposures',
                            'instrument':'Instrument and Asset Class Exposures','misc':'Other Constraints',
                            'misc':'Other Constraints','sector_industry':'Sector and Industry Concentration',
                            'beta':'Portfolio Betas','concentration':'Portfolio Concentrations','general':'Overview Exposures'}
    
    categoryOrder = ['general','concentration','beta','geo','instrument','sector_industry','misc']
    ManagerConstraints = [CanyonConstraints,ChiltonConstraints,PassportConstraints,MellonConstraints,PineRiverConstraints,SiriosConstraints,WellingtonConstraints]

    ### Don't need Fund ID Anymore Since we are Explicitly Giving the Constraints Portfolio IDS
    def __init__(self,snapshot_date):
        
        self.snapshot_date = snapshot_date
        self.date_error = False ## Keeps track of whether or not valid data exists
        self.data = []

        self.managerConstraints = []
        for constraint in LimitReport.ManagerConstraints:
            self.managerConstraints.append(constraint(self.snapshot_date))
        return
    
    ###############################################################################################
    ### Generates Limit Reports, Threading and None Threading Options
    def generate(self):

        self.data = []
        for managerConstraint in self.managerConstraints:
            managerConstraint.evaluate()
            ### Make Sure No Errors Encountered
            if managerConstraint.date_error:
                self.date_error = True
                return

            managerData = managerConstraint.serialize() 
            self.data.append(managerData)

    ### Formats table data into dictionary that can be easily manipulated by Javascript and drawn in a data table.
    ### Tables are grouped by the constraint group type so the tables can be easily separated on the front end.
    ### Each group constaints all of the associated constraints, applicable and not, and then the manager data for 
    ### each constaint
    ## Ex:  tables['general'] = {'long_exposure':{9601:{'value':3,'breached':false,'applicable':true}}
    def serialize(self):

        managerNameConv = {}
        formalConstraintNameConv = {}
        portIDs = []
        groupingNames = []

        ### Tables indexed by table names, then by the constraint id (row of table) and then by
        ### the specific manager its referring to.
        tables = {}
        applicableOnlyTables = {}

        ### Get Column Headers/Manager Names
        for managerData in self.data:

            port_id = managerData['port_id']
            portfolio_name = managerData['portfolio_name']

            portIDs.append(port_id)
            managerNameConv[port_id]=portfolio_name

            for refID in managerData['evaluation'].keys():
                refData = managerData['evaluation'][refID]

                ### Store Formal Name Conversions
                if refID not in formalConstraintNameConv.keys():
                    formalConstraintNameConv[refID]=refData['formalName']

                ### Store Unique Group References
                group = refData['grouping']
                if group not in groupingNames:
                    groupingNames.append(group)

                if group not in tables.keys():
                    tables[group]={}

                if refID not in tables[group].keys():
                    tables[group][refID]={}

                ### Store Table Data for Associated Group
                tables[group][refID][port_id]={'value':refData['value'],'applicable':refData['applicable']}
                if refData['applicable']:
                    tables[group][refID][port_id]['breached']=refData['breached']
                    tables[group][refID][port_id]['upperBound']=refData['upperBound']
                    tables[group][refID][port_id]['lowerBound']=refData['lowerBound']
                    tables[group][refID][port_id]['equalBound']=refData['equalBound']

        serializedData = {'tables':tables,'portIDs':portIDs,'groupingNames':groupingNames,
                            'formalConstraintNameConv':formalConstraintNameConv,'managerNameConv':managerNameConv,
                            'table_settings':{'categoryFormalNames':LimitReport.categoryFormalNames,'categoryOrder':LimitReport.categoryOrder}}
        return serializedData
       

