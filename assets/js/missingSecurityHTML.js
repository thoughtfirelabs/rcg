function getDropDownList(name, id, optionList) {
    var combo = $("<select></select>").attr("id", id).attr("name", name);

    $.each(optionList, function (i, el) {
        option = document.createElement('option')
        $(option).text(el)
        $(option).val(el)
        combo.append(option)
    });

    return combo;
}
//////////////////////////////////////////////////////
/// Parses the data shown in the missing security HTML grid and returns a dictionary
/// referencing the different data
function retrieveDataFromMissingSecurityHTML(){
   // Loop Over Divs

   var data = new Object()
   headers = ['rcg_id','isin','securityName','search_name','instrumentType','proxy_rcg_id','underlying_rcg_id']

   $("#missingSecurities").children().slice(1).each(function () {

      // Each Div Contains Row : Loop Over Row
      var count = 0
      var rcgID = $(this).children().children().first().val()
      data[rcgID]= new Object()
      

      $(this).children().each(function(){

         var child = $(this).children().first()
         element = document.getElementById(child.attr('id'))

         // Ignore Data in Buttons
         if(element.tagName != 'BUTTON'){
            data[rcgID][headers[count]]=child.val()
            count = count + 1
         }
      })
      

   });

   return data
}
//////////////////////////////////////////////////////
function generateMissingSecurityHTML(missingSecurityData,instrumentTypes){

   // Create Header Row
   headers = ['RCG ID','ISIN','Security Name','Lookup Name','Instrument Type','Proxy ID','Underlying ID']
   var colWidths = [120,120,240,140,160,140,140]
   var leftOffsets = [25,25,25,25,10,0,50]

   colSizeDesignations = []
   row = document.createElement('div');
   $(row).addClass('row')
   $(row).width(1400)

   for(var i = 0; i<headers.length; i++){
      header = document.createElement('div');
      $(header).addClass('col-sm-1')
      $(header).width(colWidths[i])
      $(header).html(headers[i])
      $(header).css({'text-align':'center',"position":"relative", "left":leftOffsets[i]});

      $(row).append(header)
   }

   $('#missingSecurities').append(row)

   // Store Other Data
   var rcg_ids = Object.keys(missingSecurityData)
   for(var i = 0; i<rcg_ids.length; i++){
       var row = missingSecurityData[rcg_ids[i]]
       // Reference Row Number so IDS Can Be Retrieved Later
       createHTMLRow(rcg_ids[i],row,i,instrumentTypes,colWidths)
   }
}
//////////////////////////////////////////////////////
// Makes selection from dropdown menu element
function selectFromDropDown($element, value) {
   $element.find("option").filter(function(){
      return ( ($(this).val() == value) || ($(this).text() == value) )
    }).prop('selected', true);
}

//////////////////////////////////////////////////////
function createHTMLRow(rcg_id,row,rowID,instrumentTypes,colWidths){

      var instrumentType = row['instrument_type']
      var search_name = row['search_name']
      var proxy_rcg_id = row['proxy_rcg_id']
      var underlying_rcg_id = row['underlying_rcg_id']
      var securityName = row['securityName']
      var isin = row['isin']

      var row = document.createElement('div');
      $(row).width(1400)
      $(row).addClass('row')
      $(row).css({position: 'relative','top':10});
      $('#missingSecurities').width(1400)

      // Before instrument type drop down
      addData = [rcg_id,isin,securityName,search_name]
      addDataIdDesignations = ['rcg_id','isin','securityName','search_name']

      for(var i = 0; i<addData.length; i++){

         col = document.createElement('div');
         
         $(col).addClass('col-sm-1')
         $(col).width(colWidths[i])
         

         var input = document.createElement("input");
         input.type = "text";

         if(i == 0 ){
            $(input).attr("disabled", true);
         }
         
         $(input).width(colWidths[i]-15)
         $(input).val(addData[i])
         $(input).css({position: 'relative','left':25});
         $(input).attr('id',addDataIdDesignations[i]+'_'+rowID)
         $(col).append(input)
         $(row).append(col)

      }

      // Create Drop Down Input Field 5
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(160)
      $(col).css({"position":"relative", "left":"25px"});
      
      var dropDown = getDropDownList("InstrumentDropDown", "InstrumentDropDown"+String(rcg_id), instrumentTypes)
      $(dropDown).width(115)
      selectFromDropDown(dropDown,instrumentType)
      $(dropDown).attr('id','instrumentType'+'_'+rowID)

      $(col).append(dropDown)
      $(row).append(col)

      // After Instrument Drop Down - Add Portions for Proxy and Underlying

      // Proxy /////////////////
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(colWidths[5])
      
      var input = document.createElement("input");
      input.type = "text";
      $(input).width(colWidths[5]-15)
      $(input).val(proxy_rcg_id)
      $(input).attr('id','proxy_rcg_id'+'_'+rowID)

      $(col).append(input)
      $(row).append(col)

      // Proxy Button
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(30)

      // Create Button to Add Proxy or Underlying
      button = $('<button/>', {
               text: 'Add', //set text 1 to 10
               id: 'btn_'+proxy_rcg_id,
               click: function () { addProxy(rowID) }
      });

      $(col).append(button)
      $(row).append(col)

      // Underlying /////////////////
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(colWidths[5])
      $(col).css({"position":"relative", "left":"25px"});

      var input = document.createElement("input");
      input.type = "text";
      $(input).width(colWidths[5]-15)
      $(input).val(underlying_rcg_id)
      $(input).attr('id','underlying_rcg_id'+'_'+rowID)

      $(col).append(input)
      $(row).append(col)

      // Underlying Button
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(30)

      // Create Button to Add Proxy or Underlying
      button = $('<button/>', {
               text: 'Add', //set text 1 to 10
               id: 'btn_'+underlying_rcg_id,
               click: function () { addUnderlying(rowID) }
      });
      $(button).css({"position":"relative", "left":"25px"});

      $(col).append(button)
      $(row).append(col)

      // Add the Final Save Button
      // Underlying Button
      col = document.createElement('div');
      $(col).addClass('col-sm-1')
      $(col).width(30)

      button = $('<button/>', {
               text: 'Save', //set text 1 to 10
               id: 'save_'+rcg_id,
               click: function () { saveMissingSecurity() }
      });
      $(button).css({"position":"relative", "left":"75px"});

      $(col).append(button)
      $(row).append(col)

      $('#missingSecurities').append("<br>")
      $('#missingSecurities').append(row)

      return
}