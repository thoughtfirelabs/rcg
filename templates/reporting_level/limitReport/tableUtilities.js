function drawLimitReports(limit_report_data){

    $('#applicableTables').empty()
    $('#allTables').empty()

    var tables = limit_report_data['tables']
    var portIDs = limit_report_data['portIDs']
    var groupingNames = limit_report_data['groupingNames']
    var formalConstraintNameConv = limit_report_data['formalConstraintNameConv']
    var managerNameConv = limit_report_data['managerNameConv']

    var categoryFormalNames = limit_report_data['table_settings']['categoryFormalNames']
    var categoryOrder = limit_report_data['table_settings']['categoryOrder']

    // Create Column Headers
    var tableHeaders = "<th> Constraint </th>"
    for(var i = 0; i<portIDs.length; i++){
        portID = portIDs[i]
        managerName = managerNameConv[portID]
        tableHeaders += "<th>" + managerName + "</th>";
    }

    tableTypes = Object.keys(tables)
    // Loop Over Different Tables
    for(var t = 0; t<categoryOrder.length; t++){

        // Breaches for Table
        breaches = new Array()

        groupName = categoryOrder[t]
        tableData = tables[groupName]

        constraintIDS = Object.keys(tableData)

        applicableTableData = new Array()
        nonApplicableTableData = new Array()

        // Loop Over Constraints
        for(var i = 0; i<constraintIDS.length; i++){
            var applicableRowData = new Array()
            var nonApplicableRowData = new Array()

            // Add Constraint Formal Name
            refID = constraintIDS[i]
            rowJson = tableData[refID]

            formalConstraintName = formalConstraintNameConv[refID]

            // Add Constraint Name for Both Applicable and Non Applicable Tables
            applicableRowData.push(formalConstraintName)
            nonApplicableRowData.push(formalConstraintName)

            // Loop Over Individual Managers
            for(var j = 0; j<portIDs.length; j++){
                port_id = portIDs[j]
                constraintData = rowJson[port_id]
                // Always Add Data to All Data Table
                val = constraintData['value']
                val = String((100*val).toFixed(2))+' %'

                nonApplicableRowData.push(val)

                applicable = constraintData['applicable']
                // Applicable - Store value to applicable table and note if there 
                // is a breach
                if(applicable){
                    applicableRowData.push(val)
                    breached = constraintData['breached']
                    if(breached){
                        // Track Breached Indices
                        console.log('Found Breach For : '+managerNameConv[portID]+' - '+formalConstraintName+'...')
                        var newBreach = new Object()
                        newBreach.row = i 
                        newBreach.col = j
                        breaches.push(newBreach)
                    }
                }
                // Not Applicable - NA
                else {
                    applicableRowData.push('')
                }

            } // End Loop Over Managers
            applicableTableData.push(applicableRowData)
            nonApplicableTableData.push(nonApplicableRowData)
        } // End Loop Over Constraints

        var headerName = categoryFormalNames[groupName]
        var $header = $('<h2 class="modalTitle" style="float:left; font-weight: 600; color:#696969; font-size:13px;">'+headerName+'<span style="color:#b92429">.</span></h2>')

        // Create New Table Tables for Specific Group
        var $appdiv = $("<div>", {id: groupName+"_applicable_outerdiv", "class": "row","style":"position:relative; width:1150px; top:0px;"});
        var $apptableDiv = $('<table class = "dataTable cell-border display compact"><thead><tr>' + tableHeaders + "</tr></thead></table>", {id: groupName+"_applicable"});

        $appdiv.append('<br>')
        $appdiv.append($header)
        $appdiv.append('<br>')
        $appdiv.append($apptableDiv)


        var $header2 = $('<h2 class="modalTitle" style="float:left; font-weight: 600; color:#696969; font-size:13px;">'+headerName+'<span style="color:#b92429">.</span></h2>')

        var $nonappdiv = $("<div>", {id: groupName+"_nonapplicable_outerdiv", "class": "row", "style":"position:relative; width:1150px; top:0px;"});
        var $nonapptableDiv = $('<table class = "dataTable cell-border display compact"><thead><tr>' + tableHeaders + "</tr></thead></table>", {id: groupName+"_nonapplicable"});

        $nonappdiv.append('<br>')
        $nonappdiv.append($header2)
        $nonappdiv.append('<br>')
        $nonappdiv.append($nonapptableDiv)

        var appDataTable = $apptableDiv.DataTable({"searching":false,"bPaginate": false, "info":false,
            data: applicableTableData,
            bAutoWidth:false,
            aoColumns : [
            { sWidth: '30%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' }
          ],
            "columnDefs": [
                {"className": "dt-center", "targets": [1,2,3,4,5,6,7]},
            ],
        });
        highlightTableForBreaches(appDataTable,breaches)
        appDataTable.draw()

        var nonappDataTable = $nonapptableDiv.DataTable({"searching":false,"bPaginate": false, "info":false,
            data: nonApplicableTableData,
            bAutoWidth:false,
            aoColumns : [
            { sWidth: '30%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' },
            { sWidth: '10%' }
          ],
            "columnDefs": [
                {"className": "dt-center", "targets": [1,2,3,4,5,6,7]},
            ],
        });
        highlightTableForBreaches(nonappDataTable,breaches)
        nonappDataTable.draw()

        $('#applicableTables').append($appdiv)
        $('#allTables').append($nonappdiv)

    } // End Loop Over Tables

}
// Given breaches as a list of ordered pairs, the function will highlight the cells
// that are indicated by the given breach indices
function highlightTableForBreaches(dataTable,breaches){
    for(var i = 0; i<breaches.length; i++){
        rowInd = breaches[i].row 
        colInd = breaches[i].col + 1
        var cell = dataTable.cell({row: rowInd, column: colInd}).node();
        $(cell).addClass('report_flag');
    }
 }