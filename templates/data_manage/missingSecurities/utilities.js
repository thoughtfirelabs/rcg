//////////
function clearMissingSecurities(){
  $('#missingSecurities').empty()
}

///////////////// Missing Security Functions /////////////////////

//////////////////////////////////////////////////////
// Look for missing securities between the designated dates that might be
// requiring information or models that are not present.
function getHoldingMissingSecurities(startDate,endDate,singleDate,refreshType,include_proxy_underlying,callback){
    
    console.log('Parameters for Missing Security Search - Over Held Securities : ')
    console.log('Start Date : '+String(startDate))
    console.log('End Date : '+String(endDate))
    console.log('Single Date : '+String(singleDate))
    console.log('Refresh Type : '+String(refreshType))
    console.log('Include Proxies/Underlyings : '+String(include_proxy_underlying))

    $.ajax({
        type: "GET",
        url: '/findHeldMissingSecurities/',
        data: {'startDate':startDate,'endDate':endDate,'singleDate':singleDate,'refreshType':refreshType,'include_proxy_underlying':include_proxy_underlying},
        error: function(data){
          alert("Error:  Unknown Error");
        },
        success: function(response){
          callback(response)
        }
    })
}
//////////////////////////////////////////////////////
// Finds missing securities regardless of whether or not they are being held.
function getAllMissingSecurities(include_proxy_underlying,callback){

  console.log('Parameters for Missing Security Search - Over All Securities in Database : ')
  console.log('Include Proxies/Underlyings : '+String(include_proxy_underlying))

  $.ajax({
      type: "GET",
      url: '/findAllMissingSecurities/',
      data: {'include_proxy_underlying':include_proxy_underlying},
      error: function(data){
        alert("Error:  Unknown Error");
      },
      success: function(response){
        callback(response)
      }
  })
}

//////////////////////////////////////////////////////
// Saves Backend Data for the Missing Securitty from the Missing Security Table/Widget View
// Called from both Update Data Tab (after update holdings if user clicks the save button) and find missing data button.
function saveMissingSecurity(sec_id){

  var data = readDataFromMissingSecurities()
  var sec_data = data[sec_id]

  var save_data = new Object()

  keys = Object.keys(sec_data)
  length = keys.length
  for(var i = 0; i<length; i++) {
      if(  typeof(sec_data[keys[i]]) != "undefined"){
        save_data[keys[i]]=sec_data[keys[i]]
      }
  }
  saveSecurityData(sec_id,save_data,function(){
    // Remove Security From Table
    removeRowFromMissingSecurities(sec_id)
  })
  
}

// Saves Backend Data for the All Data in Missing Security Table/Widget View
function saveAllMissingSecurity(){

    data = readDataFromMissingSecurities()
    
    confirmation = confirm("Are you sure you would like to save the data for all the securities in the table?")
    if(!confirmation){
      return
    }
    secKeys = Object.keys(data)
    // Loop over securities
    for(var i = 0; i<secKeys.length; i++) {

        sec_id = secKeys[i]
        if (typeof(sec_id) != "undefined"){

            var sec_data = data[sec_id]
            var save_data = new Object()

            // Loop over data attributes
            keys = Object.keys(sec_data)
            length = keys.length
            for(var k = 0; k<length; k++) {
                if(  typeof(sec_data[keys[k]]) != "undefined" &&  sec_data[keys[k]] != ""){
                  save_data[keys[k]]=sec_data[keys[k]]
                }
            }

            // Call Made for Each Security
            $.ajax({
                  type: "GET",
                  url: '/missingSecurities/',
                  data:{'data':data,'command':'save'},
                  error: function(data){
                    alert("Error:  Unknown Error");
                    return
                  },
                  success: function(data){
                      
                  }
              })

        }
      }
  
}
  
