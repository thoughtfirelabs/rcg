////////////////////////////
function create_holdings_table(div_name, holdings_content, desired_fields,numPerPage){

    var dataTable = $(div_name).DataTable({"pageLength": numPerPage, "searching":true, "retrieve": true});
    dataTable.clear();
    sec_ids = Object.keys(holdings_content['security_name'])

    function isNumeric(num){
        return !isNaN(num)
    }

    // Loop Over Securities
    for (var i = 0; i<sec_ids.length; i++){
        
        var new_row = []
        var sec_id = sec_ids[i]
        new_row.push(sec_id)
        // Loop Over Fields
        for (var j = 0; j<desired_fields.length; j++){
            var fieldVal = holdings_content[desired_fields[j]][sec_id]
            var data = ""
            if (typeof(fieldVal) != "undefined" && fieldVal != null){
                data = fieldVal
                // Handle Number Data for Dollar Amts
                if(isNumeric(fieldVal)){
                    data = fieldVal.formatMoney(2)
                }
                new_row.push(data)
            }
            else{
                new_row.push("")
            }
        }

        dataTable.row.add(new_row)
    }
    return dataTable
}    

