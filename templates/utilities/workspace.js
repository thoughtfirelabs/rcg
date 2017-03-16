// Functions to get and retrieve the workspace settings/data
function getWorkspace(callback){
    
    $.ajax({
          type: "GET",
          url: '/workspace',
          data: {'handle':'getWorkspace'},
          error: function(data){
            alert("There was a problem");
          },
          success: function(data){
              port_id = JSON.parse(data)['portfolio_id']
              port_name = JSON.parse(data)['portfolio_name']
              fund_id = JSON.parse(data)['fund_id']
              fund_name = JSON.parse(data)['fund_name']
              snapshot_date = JSON.parse(data)['snapshot_date']
              validity = JSON.parse(data)['valid']
              
              callback(port_id,port_name,fund_id,fund_name,snapshot_date,validity)
              return 
            }
        })
}


// Communicate to back end to change the portfolio stored for the session.
function setWorkspacePortfolio(port_id,callback){

    $.ajax({
        type: "GET",
        url: '/workspace',
        data: {'handle':'setPortfolio','port_id':port_id},
        error: function(data){
          alert("There was a problem");
        },
        success: function(data){

          // Return Workspace Data 
          port_id = JSON.parse(data)['portfolio_id']
          port_name = JSON.parse(data)['portfolio_name']
          snapshot_date = JSON.parse(data)['snapshot_date']
          validity = JSON.parse(data)['valid']

          callback(port_id,port_name,snapshot_date,validity)
          return
        }
      })
}

// Communicate to back end to change the fund stored for the session.
function setWorkspaceFundDate(fund_id,snapshot_date,callback){

    $.ajax({
        type: "GET",
        url: '/workspace',
        data: {'handle':'setFundandDate','snapshot_date':snapshot_date,'fund_id':fund_id},
        error: function(data){
          alert("There was a problem");
        },
        success: function(data){

          // Return Workspace Data 
          fund_id = JSON.parse(data)['fund_id']
          fund_name = JSON.parse(data)['fund_name']
          snapshot_date = JSON.parse(data)['snapshot_date']
          validity = JSON.parse(data)['valid']

          callback(fund_id,fund_name,snapshot_date,validity)
          return
        }
      })
}


// Communicate to back end to change the fund stored for the session.
function setWorkspaceFund(fund_id,callback){

    $.ajax({
        type: "GET",
        url: '/workspace',
        data: {'handle':'setFund','fund_id':fund_id},
        error: function(data){
          alert("There was a problem");
        },
        success: function(data){

          // Return Workspace Data 
          fund_id = JSON.parse(data)['fund_id']
          fund_name = JSON.parse(data)['fund_name']
          snapshot_date = JSON.parse(data)['snapshot_date']
          validity = JSON.parse(data)['valid']

          callback(fund_id,fund_name,snapshot_date,validity)
          return
        }
      })
}


/// Sets workspace date to request's session on back end, if there are no holdings on the date
/// the date will not be stored to the session and an error will be returned.
function setWorkspaceDate(snapshot_date,callback){
  $.ajax({
      type: "GET",
      url: '/workspace',
      data: {'snapshot_date':snapshot_date,'handle':'setDate'},
      error: function(data){
        alert("There was a problem");
      },
      success: function(data){

        // Return Workspace Data 
        port_id = JSON.parse(data)['portfolio_id']
        port_name = JSON.parse(data)['portfolio_name']
        fund_id = JSON.parse(data)['fund_id']
        fund_name = JSON.parse(data)['fund_name']
        snapshot_date = JSON.parse(data)['snapshot_date']
        validity = JSON.parse(data)['valid']

        callback(port_id,port_name,fund_id,fund_name,snapshot_date,validity)
  
      }
    })
}


// Functions to Show the Success or Invalidity of the Workspaces
function animateWorkspaceSuccess(){

    $('#workspace_success').show()
    $('#workspace_success').html("Valid Workspace")
    $('#workspace_success').fadeOut(2000)
}

function animateWorkspaceError(){

    $('#workspace_warning').show()
    $('#workspace_warning').html("Workspace Error : No holdings on specified date.")
    $('#workspace_warning').fadeOut(2000)
}


/////////////////////////////////////
function loadFunds(){
    $.ajax({
      type: "GET",
      url: '/workspace',
      data: {'handle':'loadFunds'},
      error: function(data){
        alert("There was a problem");
      },
      success: function(data){
        funds = JSON.parse(data)['funds']
        populate_fund_dropdown(funds)
        dataTable = create_fund_table('#fund_table',funds)
        dataTable.draw()
      }
    })
    
}
/////////////////////////////////////////
function loadPortfolios(){
    $.ajax({
      type: "GET",
      url: '/workspace',
      data: {'handle':'loadPortfolios'},
      error: function(data){
        alert("There was a problem");
      },
      success: function(data){
        
        portfolios = JSON.parse(data)['portfolios']
        populate_portfolio_dropdown(portfolios)
        dataTable = create_portfolio_table('#port_table',portfolios)
        dataTable.draw()
      }
    })
}

// Functions to populate common dropdowns if applicable

// Load Portfolios for Selected Fund and Populate Table
function populate_portfolio_dropdown(portfolios){

    select = document.getElementById('port_select')
    if(select){

      for(var i = 0; i<portfolios.length; i++){
      port = portfolios[i]
      port_id = port['id']
      port_name = port['portfolio_name']
      dropdown_title = String(port_id)+'-'+port_name

      var option = document.createElement('option');
      option.text = dropdown_title;
      option.value = port_id;

      select.add(option, 0);
    }
  }

}

////////////////////////////////////////////////////////
function populate_fund_dropdown(funds){
  
  select = document.getElementById('fund_select')
  if(select){

      for(var i = 0; i<funds.length; i++){
      fund = funds[i]
      fund_id = fund['id']
      fund_name = fund['fund_name']
      dropdown_title = String(fund_id)+'-'+fund_name

      var option = document.createElement('option');
      option.text = dropdown_title;
      option.value = fund_id;
      select = document.getElementById('fund_select')
      select.add(option, 0);
    }
  }
  
}