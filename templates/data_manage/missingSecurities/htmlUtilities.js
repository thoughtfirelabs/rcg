// Creates Preselected HTML Dropdown List Based on Instrument Type nad All Possible Instrument Types
function createDropDownList(optionList) {

    var dropDown = $("<select></select>")
    dropDown.attr('name','instrumentType')
    defaultOption = document.createElement('option')
    $(defaultOption).val("None")
    $(defaultOption).text("None")

    for(var i = 0; i<optionList.length; i++){

      option = document.createElement('option')
      $(option).val(optionList[i])
      $(option).text(optionList[i])

      dropDown.append(option)
    }
    dropDown.val("None") // Default Selection
    return dropDown;
}
//////////////////////////////////////////////////////
// Removes row from the HTML table for missing securities by locating the corresponding ID
function removeRowFromMissingSecurities(rcg_id){

   tableData = readDataFromMissingSecurities()
   keys = Object.keys(tableData)

   var rightIndex; 

   // Find corresponding table row index for rcg id
   for(var i = 0; i<keys.length; i++){
      var index = tableData[keys[i]]['index']
      if(keys[i]==rcg_id){
         rightIndex = index
      }
   }
   $('#missingSecuritiesTable tr').eq(rightIndex).remove();
   return 
}

//////////////////////////////////////////////////////
/// Parses the data shown in the missing security HTML grid and returns a dictionary
/// referencing the different data
function readDataFromMissingSecurities(){

    var data = new Object()
    headers = ['rcg_id','id_isin','security_name','search_name','instrument_type','proxy_rcg_id','underlying_rcg_id']

    var rowCount = 0
    var table = $("#missingSecuritiesTable")

    table.find('tr').each(function (i, el) {
        var $tds = $(this).find('td')

        var container = $tds.eq(0)
        var child = container.children().first()
        var rcgID = child.val()

        data[rcgID]= new Object()

        for(var i = 1; i<headers.length; i++){

          var container = $tds.eq(i)
          var child = container.children().first()
          valueFound = child.val()
          data[rcgID][headers[i]] = valueFound
        }
         // Indexed Used to Refer to Table from Other Jquery/Javascript Functions
         // Keeps track of order of elements so they can be referenced.
         data[rcgID]['index']=rowCount
         rowCount = rowCount + 1

    });
    return data
}

//////////////////////////////////////////////////////
function generateMissingSecurityHTML(missingSecurityData,instrumentTypes){

   // Create Header Row
   headers = ['RCG ID','ISIN','Security Name','Ticker','Instrument Type','Proxy ID','Add Proxy','Underlying ID','Add Undl','Save']
   var colWidths = [120,120,320,140,160,140,60,140,60,100]

   colSizeDesignations = []
   row = document.createElement('div');
   $(row).addClass('row')
   $(row).width(1400)

   var table = $('<table></table>')
   table.attr('id','missingSecuritiesTable')
   var headerRow = $('<tr></tr>')

   // Create Header and Add to  Table
   for(var i = 0; i<headers.length; i++){

      var header = $('<th></th>')
      
      header.width(colWidths[i])
      header.html(headers[i])
      header.css({'text-align':'center'})
      headerRow.append(header)
   }

   table.append(headerRow)
   
   // Store Other Data
   var rcg_ids = Object.keys(missingSecurityData)
   for(var i = 0; i<rcg_ids.length; i++){

       var completeDropDown = createDropDownList(instrumentTypes)
       var rowData = missingSecurityData[rcg_ids[i]]
       var row = createHTMLRow(rcg_ids[i],rowData,completeDropDown,colWidths)
       table.append(row)
   }

   return table 
}

//////////////////////////////////////////////////////
function createHTMLRow(rcg_id,rowData,completeDropDown,colWidths){

      var instrumentType = rowData['instrument_type']
      var search_name = rowData['search_name']
      var proxy_rcg_id = rowData['proxy_rcg_id']
      var underlying_rcg_id = rowData['underlying_rcg_id']
      var securityName = rowData['securityName']
      var isin = rowData['isin']

      var row = $('<tr></tr>')
      var colHeight = 30

      // Input Fields At Beginning ////////////////////////
      addData = [rcg_id,isin,securityName,search_name]
      for(var i = 0; i<addData.length; i++){

         var col = $('<td align="center"></td>')
         col.height(colHeight)

         var input = document.createElement("input");
         input.type = "text";
         $(input).width(colWidths[i]-20)
         $(input).val(addData[i])

         // Disable RCG ID Input
         if(i == 0 ){
            $(input).attr("disabled", true);
         }
         
         col.append(input)
         col.css({'text-align':'center'})
         row.append(col)
      }

      // Instrument Drop Down ////////////////////////
      var col = $('<td></td>')
      col.height(colHeight)
      completeDropDown.width(115)
      
      if(typeof(instrumentType) != "undefined"){
        completeDropDown.val(instrumentType)
      }
    
      col.append(completeDropDown)
      col.css({'text-align':'center'})
      row.append(col)

      // Proxy ////////////////////////
      var col = $('<td></td>')
      col.height(colHeight)
     
      var input = $('<input type="text" readonly></input>')
      input.width(colWidths[5]-20)
      input.val(proxy_rcg_id)

      col.append(input)
      col.css({'text-align':'center'})
      row.append(col)

      ////////////////////////////////////////////////////////////////////////////////////////////////
      // Proxy Button ////////////////////////
      var col = $('<td></td>')
      col.height(colHeight)

      proxyButton = $('<button/>')
      proxyButton.html('Add')
      proxyButton.on('click',function(){
          openProxyModal(rcg_id)
      })

      col.append(proxyButton)
      col.css({'text-align':'center'})
      row.append(col)

      ////////////////////////////////////////////////////////////////////////////////////////////////

      // Underlying ////////////////////////
      var col = $('<td></td>')
      col.height(colHeight)

      var input = $('<input type="text" readonly></input>')
      input.width(colWidths[5]-20)
      input.val(underlying_rcg_id)

      col.append(input)
      col.css({'text-align':'center'})
      row.append(col)

      ////////////////////////////////////////////////////////////////////////////////////////////////
      // Underlying Button ////////////////////////
      var col = $('<td></td>')
      col.height(colHeight)

      underlyingButton = $('<button/>', {
               text: 'Add', 
               name: 'addUnderlying',
               click: function(){openUnderlyingModal(rcg_id)}
      });

      col.append(underlyingButton)
      col.css({'text-align':'center'})
      row.append(col)
      ////////////////////////////////////////////////////////////////////////////////////////////////

      // Add the Final Save Button
      var col = $('<td></td>')
      col.height(colHeight)

      saveButton = $('<button/>', {
               text: 'Save', //set text 1 to 10
               name: 'save',
               click: function(){saveMissingSecurity(rcg_id)}
      });

      col.append(saveButton)
      col.css({'text-align':'center'})
      row.append(col)
      return row
}