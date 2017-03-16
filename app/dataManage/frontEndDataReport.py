from app.settings import MissingDataReportSettings

###################################################################
class FrontEndDataReport(MissingDataReportSettings):
    def __init__(self, portfolio):

        MissingDataReportSettings.__init__(self)
        self.portfolio = portfolio
        self.securities = self.portfolio.securities

        self.num_assumptions = 0
        self.num_assumption_securities = 0

        self.num_missing_fatal_fields = 0
        self.num_missing_fatal_securities = 0

        self.fatal_data_report = []
        self.nonfatal_data_report = []

        return

    #####################################
    ### Creates a Single Row of DataFrame Corresponding to Missing Data Record
    def createRowFromRecord(self, record):

        constant_fields = [record.security.rcg_id, record.security.SecurityName.value, record.security.InstrumentType.value]

        ### Reference field and assumption value for field
        if record.field.nonfatalMissing:

            ### Only want to include situations in which assumptions were made
            if record.field.assumed:
                constant_fields.append(record.field.internalFieldName)
                ### Include Actual Assumption
                assumption = record.field.assumptionValue
                if type(assumption) == str:
                    assumption = assumption.title()
                constant_fields.append(assumption)

            else:
                return None

        ### Reference missing field
        elif record.field.fatalMissing:
            constant_fields.append(record.field.internalFieldName)

        return constant_fields

    ##########################
    ### Generate data report for front end knowledge of missing securities
    ### or missing data.
    def generate(self):

        self.data = []

        ### Loop over Missing Data Records for Each Portfolio security
        for security in self.securities:
            dataRecords = security.missingDataRecords
            securityAssumptionMade = False
            securityInvalid = False

            ### Loop Over Individual Records -> Row of DF Corresponds to Single Record
            for record in dataRecords:

                ### Find Nonfatal Assumptions Made #################
                constant_fields = self.createRowFromRecord(record)
                if constant_fields != None:
                    if record.field.nonfatalMissing:

                        securityAssumptionMade = True
                        self.num_assumptions += 1
                        self.nonfatal_data_report.append(constant_fields)

                    ### Find Fatal Fields Missing
                    elif record.field.fatalMissing:
                        securityInvalid = True
                        self.num_missing_fatal_fields += 1
                        self.fatal_data_report.append(constant_fields)

            if securityAssumptionMade:
                self.num_assumption_securities += 1
            if securityInvalid:
                self.num_missing_fatal_securities += 1

        error_report_details = {'num_missing_fatal_fields': self.num_missing_fatal_fields,
                            'num_missing_fatal_securities': self.num_missing_fatal_securities,
                            'fatal_data_report': self.fatal_data_report,
                            'num_assumptions': self.num_assumptions,
                            'num_assumption_securities': self.num_assumption_securities,
                            'nonfatal_data_report': self.nonfatal_data_report}

        return error_report_details
