import sys
sys.dont_write_bytecode = True

#########################################################################
import django.views.static
from django.contrib import admin
from django.conf.urls import include, url
import django.views.defaults
########################################################################
### Views

### Management View
from app.managementView import custom_login, custom_logout, getAuthenticatedUser

import app.views.views_Exposure as viewsExposure

from app.views.views_SingleSecurity import *
from app.views.reporting.viewsLimitReport import *
from app.views.reporting.viewsExposureReport import *
from app.views.views_Cleanup import *
from app.views.viewsHoldings import *

from app.views.views_GeneralAPIData import *

### Data management views
from app.views.views_HoldingsManagement import HoldingsUpdateView
from app.views.views_DataReport import DataReportView
from app.views.views_MissingSecurities import *
from app.views.views_AllSecurities import *
from app.views.views_StaticManagement import StaticUpdateView
from app.views.views_DynamicManagement import DynamicUpdateView

from app.views.viewsRedirect import *
from app.views.workspace.views_Workspace import WorkspaceView

import app.lib.modal_views
import settings

#########################################################################
urlpatterns = (

    url(r'^admin/', admin.site.urls),

    #url(r'^static/(?P<path>.*)$', django.views.static.serve,
    #    {'document_root': 'assets'}),
    url(r'^modules/(?P<path>.*)$', django.views.static.serve,
        {'document_root': 'node_modules'}),
    url(r'^templates/(?P<path>.*)$', django.views.static.serve,
        {'document_root': 'templates'}),

    # static files w/ no-cache headers
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),

    url(r'^$', portfolio_level),

    ### Login and Management Views
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', custom_login),
    url(r'^logout/$', django.contrib.auth.views.logout,{'next_page': '/'}),
    url(r'getAuthenticatedUser/$', getAuthenticatedUser),

    #### Single Security API Views #######
    url(r'^get_security_details/$', get_security_details),
    url(r'^save_security_details/$', save_security_details),

    url(r'^removeProxy/$', removeProxy),
    url(r'^checkIfProxyExists/$', checkIfProxyExists),
    url(r'^updateProxy/$', updateProxy),

    url(r'^removeUnderlying/$', removeUnderlying),
    url(r'^checkIfUnderlyingExists/$', checkIfUnderlyingExists),
    url(r'^updateUnderlying/$', updateUnderlying),

    url(r'^removeSecurity/$', removeSecurity),

    url(r'^suppressField/$', suppressField),
    url(r'^unsuppressField/$', unsuppressField),

    ### Missing Security Views
    url(r'^findAllMissingSecurities/$', findAllMissingSecurities),
    url(r'^findHeldMissingSecurities/$', findHeldMissingSecurities),

    ### Data Cleanup Views
    url(r'^cleanupProxiesUnderlyings/$', cleanupProxiesUnderlyings),
    url(r'^cleanupStatic/$', cleanupStatic),
    url(r'^cleanupDynamic/$', cleanupDynamic),

    ################# Port Level Tabs #####################
    url(r'^get_portfolio_overview/$', viewsExposure.get_portfolio_overview),
    url(r'^get_category_exposure_analysis/$', viewsExposure.get_category_exposure_analysis),
    
    ############## Field Relevant Views ###################
    url(r'^get_all_instrument_types/$', get_all_instrument_types),
    url(r'^get_all_sectors/$', get_all_sectors),
    url(r'^get_all_country_names/$', get_all_country_names),
    url(r'^get_all_country_codes/$', get_all_country_codes),
    
    url(r'^smartInstrumentClassifier/$', smartInstrumentClassifier),

    ######################## ######################## ######################## ######################## ######################## ########################
    ################# ################## ###################### Data Manage Page Section ##################### ################# ############################

    ### Base Redirection Views (These need to be directly communicated through back end for permission reasons)
    url(r'^data_manageAdmin', data_manageAdmin),
    url(r'^data_manage', data_manage),

    url(r'^updateHoldings', HoldingsUpdateView.as_view()),
    url(r'^updateStatic', StaticUpdateView.as_view()),
    url(r'^updateDynamic', DynamicUpdateView.as_view()),

    url(r'^generateMissingData', DataReportView.as_view()),
    url(r'^workspace', WorkspaceView.as_view()),
    url(r'^getAllSecurities', getAllSecurities),

    ######################## ######################## ######################## ######################## ######################## ########################
    ################# ################## ###################### Port Level ##################### ########################### ############################

    url(r'^portfolio_level/open_geo_modal/$', app.lib.modal_views.geo_modal_base),
    url(r'^portfolio_level/geo_modal_data/$', app.lib.modal_views.geo_modal_data),
    url(r'^portfolio_level/open_explore_modal/$', app.lib.modal_views.explore_modal_base),
    url(r'^portfolio_level/explore_region/$', app.lib.modal_views.explore_region),


    ######################## ######################## ######################## ######################## ######################## ########################
    ################# ################## ###################### Fund Level ##################### ########################### ############################

    url(r'^fund_level/get_fund_overview/$', viewsExposure.get_fund_overview),
    url(r'^fund_level/get_fund_category_exposure_analysis/$', viewsExposure.get_fund_category_exposure_analysis),

    ######################## ######################## ######################## ######################## ######################## ########################
    ################# ################## ###################### Holdings Level ##################### ########################### ############################
    url(r'^holding_level/get_portfolio_holdings/$', get_portfolio_holdings),

    ######################## ######################## ######################## ######################## ######################## ########################
    ################# ################## ###################### Reporting Section ##################### ################# ############################

    ####### Monthly Exposure Report Base
    url(r'^reporting_level/download_exposure_report/$', download_exposure_report),
    url(r'^reporting_level/download_security_details/$', download_security_details),

    ####### Limit Report General Tab
    url(r'^reporting_level/generateLimitReport/$', generateLimitReport),
    url(r'^reporting_level/retrieveLimitReportData/$', retrieveLimitReportData),
    url(r'^reporting_level/generateLimitReportPDF/$', generateLimitReportPDF),

    ####### Limit Report Manager Details Tab
    url(r'^reporting_level/generate_single_manager_limit_report/$', generate_single_manager_limit_report),

    url(r'portfolio_level/', portfolio_level),
    url(r'^data_manage/$', data_manage),

    url(r'^fund_level/$', fund_level),
    url(r'^holding_level/$', holding_level),
    url(r'^reporting_level/$', reporting_level),

)