//////////////////////////////////////////////////////
function validateDates(startDate,endDate,singleDate){

  var startInValid = false
  if(startDate == "" || typeof(startDate)=="undefined"){
    startInValid = true
  }
  var endInValid = false
  if(endDate == "" || typeof(endDate)=="undefined"){
    endInValid = true
  }
  var singleInValid = false
  if(singleDate == "" || typeof(singleDate)=="undefined"){
    singleInValid = true
  }

  if (startInValid && endInValid && singleInValid) {
    return true
  }
  if (endInValid == false){
    if(startInValid){
      return true
    }
  }
  if (startInValid == false){
    if(endInValid){
      return true
    }
  }
  if(singleInValid){
      if (startInValid && endInValid) {
        return true
      }
  }
  if (startInValid && endInValid) {
    if(singleInValid){
      return true
    }
  }
  return false
}

////////////////////////////
function create_all_securities_table(div_name, securityData, desired_fields,numPerPage){

    sec_ids = Object.keys(securityData)
    dataList = new Array()
    // Loop Over Securities
    for (var i = 0; i<sec_ids.length; i++){
        
        // Get Data for Specific Security in Loop
        var sec_id = sec_ids[i]
        singleSecurityData = securityData[sec_id]
        var new_row = []
        new_row.push(sec_id)
        // Loop Over Fields
        for (var j = 0; j<desired_fields.length; j++){
            var fieldVal = singleSecurityData[desired_fields[j]]
            var data = ""
            if (typeof(fieldVal) != "undefined"){
                data = fieldVal
            }
            new_row.push(data)
        }
        dataList.push(new_row)
    }


    var dataTable = $(div_name).DataTable({"pageLength": numPerPage, "searching":true, "retrieve": true,

      data: dataList,
      scrollY:        620,
      scrollCollapse: true,
      scroller:       true,

      "aoColumns": [
          {"sTitle": "ID", "bSortable":false, "sWidth":"8%"},
          {"sTitle": "ISIN", "bSortable":false, "sWidth":"8%"},
          {"sTitle": "Name", "bSortable":true, "sWidth":"15%"},
          {"sTitle": "Ticker", "bSortable":false, "sWidth":"5%"},
          {"sTitle": "Instrument", "bSortable":true, "sWidth":"12.5%"},
          {"sTitle": "Country", "bSortable":true, "sWidth":"12.5%"},
          {"sTitle": "Cntry of Risk", "bSortable":true, "sWidth":"5%"},
          {"sTitle": "Sector", "bSortable":true, "sWidth":"10%"},
          {"sTitle": "Industry", "bSortable":true, "sWidth":"10%"},
          {"sTitle": "Proxy Ticker", "bSortable":false, "sWidth":"5%"},
          {"sTitle": "Undl Ticker", "bSortable":false, "sWidth":"5%"},
          ],
    });
    return dataTable
}    
