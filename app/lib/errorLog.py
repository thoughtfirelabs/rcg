########################################################################
class ErrorLog:

    def __init__(self):

        self.numErrors = 0
        self.errors = []
        self.successMessage = None
        return

    ### Store error in log
    def add(self,errorString):
        self.errors.append(errorString)
        self.numErrors = self.numErrors + 1

    ### Notes Success Message at Beginning of Log
    def noteSuccess(self,message):
        self.successMessage = message

    ### Format data in error log to response format that can be outputted to front end
    def createResponseJson(self):

        responseData = {}

        if self.numErrors == 0:
            responseData['success'] = self.successMessage
            return responseData

        responseData['error'] = ""
        for error in self.errors:
            responseData['error'] = responseData['error'] + error + '\n'

        return responseData