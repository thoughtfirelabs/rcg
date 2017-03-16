// Gets detailed static data for a given security.
function get_security_details(securityID,callback){

    console.log('Getting Security Details for : '+String(securityID))
	$.ajax({
        url: '/get_security_details/',
        type: "get",
        data: {'security_id':securityID},
        success: function(response) {
            var security_details = JSON.parse(response)['security_details']
            callback(security_details)
        }
    })
}

////////////////////////////////////////////////////////
// Functions to remove or update proxies or underlyings for a specific security.
function removeSecurity(securityID,callback){

	$.ajax({
        url: '/removeSecurity/',
        type: "get",
        data: {'security_id':securityID},
        success: function(response) {
        	var updateResponse = JSON.parse(response)['updateResponse']
            callback(updateResponse)
        }
    })
}
///////////
function checkIfProxyExists(proxyTickerOrID,callback){

    $.ajax({
        url: '/checkIfProxyExists/',
        type: "get",
        data: {'proxyTickerOrID':proxyTickerOrID},
        success: function(response) {
            var response = JSON.parse(response)['data']
            callback(response)
        }
    })
}

///////////
function checkIfUnderlyingExists(underlyingTickerOrID,callback){

    $.ajax({
        url: '/checkIfUnderlyingExists/',
        type: "get",
        data: {'underlyingTickerOrID':underlyingTickerOrID},
        success: function(response) {
            var response = JSON.parse(response)['data']
            callback(response)
        }
    })
}


///////////
function updateProxy(securityID,proxyData,callback){

    if(typeof(securityID) == "undefined" || securityID == ""){
        alert("Error : Invalid Security ID")
        return
    }

	// This should never be nil.
	proxyTicker = proxyData.proxyTicker
    proxyID = proxyData.proxyID
    proxyInstrumentType = proxyData.proxyInstrumentType
    proxyName = proxyData.proxyName

	$.ajax({
        url: '/updateProxy/',
        type: "get",
        data: {'proxyTicker':proxyTicker,'proxyID':proxyID,'proxyName':proxyName,'proxyInstrumentType':proxyInstrumentType,'securityID':securityID},
        success: function(response) {
        	var data = JSON.parse(response)['data']
            callback(data)
        }
    })
}
///////////
function updateUnderlying(securityID,underlyingData,callback){

    if(typeof(securityID) == "undefined" || securityID == ""){
        alert("Error : Invalid Security ID")
        return
    }

    // This should never be nil.
    underlyingTicker = underlyingData.underlyingTicker
    underlyingID = underlyingData.underlyingID
    underlyingInstrumentType = underlyingData.underlyingInstrumentType
    underlyingName = underlyingData.underlyingName

    $.ajax({
        url: '/updateUnderlying/',
        type: "get",
        data: {'underlyingTicker':underlyingTicker,'underlyingID':underlyingID,'underlyingName':underlyingName,'underlyingInstrumentType':underlyingInstrumentType,'securityID':securityID},
        success: function(response) {
            var data = JSON.parse(response)['data']
            callback(data)
        }
    })
}


////////////////////////////////////////////////////////
function retrieveAllSecurities(callback){
    $.ajax({
        url: '/getAllSecurities/',
        type: "get",
        success: function(response) {
            var securityData = JSON.parse(response)['securityData']
            callback(securityData)
        }
    })

}


////////////////////////////////////////////////////////
// Suppresses field and includes the suppressed security details in the response for updating
function suppressField(securityID,fieldName,callback){
    $.ajax({
        url: '/suppressField/',
        type: "get",
        data: {'securityID':securityID,'fieldName':fieldName},
        success: function(response) {
            var security_details = JSON.parse(response)['security_details']
            callback(security_details)
        }
    })

}

////////////////////////////////////////////////////////
// Unsuppresses field and includes the unsuppressed security details in the response for updating
function unsuppressField(securityID,fieldName,callback){
    $.ajax({
        url: '/unsuppressField/',
        type: "get",
        data: {'securityID':securityID,'fieldName':fieldName},
        success: function(response) {
            var security_details = JSON.parse(response)['security_details']
            callback(security_details)
        }
    })

}





