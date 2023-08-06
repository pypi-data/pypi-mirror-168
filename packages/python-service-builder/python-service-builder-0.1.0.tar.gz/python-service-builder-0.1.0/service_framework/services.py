# Copyright 2022 David Harcombe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import dataclasses
import enum
from typing import Any, Optional

import dataclasses_json
import immutabledict

from . import field, lazy_property


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ServiceDefinition(object):
  service_name: Optional[str] = field()
  version: Optional[str] = field()
  discovery_service_url: Optional[str] = field()


class S(enum.Enum):
  @lazy_property
  def definition(self) -> ServiceDefinition:
    """Fetch the ServiceDefinition.

    Lazily returns the dataclass containing the service definition
    details. It has to be lazy, as it can't be defined at
    initialization time.

    Returns:
        ServiceDefinition: the service definition
    """
    (service_name, version) = SERVICE_DEFINITIONS.get(self.name)
    return ServiceDefinition(
        service_name=service_name,
        version=version,
        discovery_service_url=(
            f'https://{service_name}.googleapis.com/$discovery/rest'
            f'?version={version}'))

  @classmethod
  def from_value(cls, value) -> S:
    for k, v in cls.__members__.items():
      if k == value.upper():
        return v
    else:
      raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")


SERVICE_DEFINITIONS = \
    immutabledict.immutabledict({
        'ABUSIVEEXPERIENCEREPORT': ('abusiveexperiencereport', 'v1'),
        'ACCELERATEDMOBILEPAGEURL': ('acceleratedmobilepageurl', 'v1'),
        'ACCESSAPPROVAL': ('accessapproval', 'v1'),
        'ACCESSCONTEXTMANAGER': ('accesscontextmanager', 'v1'),
        'ADEXCHANGEBUYER2': ('adexchangebuyer2', 'v2beta1'),
        'ADEXPERIENCEREPORT': ('adexperiencereport', 'v1'),
        'ADSDATAHUB': ('adsdatahub', 'v1'),
        'ADMIN': ('admin', 'reports_v1'),
        'ADMOB': ('admob', 'v1'),
        'ADSENSE': ('adsense', 'v2'),
        'ADSENSEHOST': ('adsensehost', 'v4.1'),
        'ALERTCENTER': ('alertcenter', 'v1beta1'),
        'ANALYTICS': ('analytics', 'v3'),
        'ANALYTICSADMIN': ('analyticsadmin', 'v1alpha'),
        'ANALYTICSDATA': ('analyticsdata', 'v1beta'),
        'ANALYTICSHUB': ('analyticshub', 'v1'),
        'ANALYTICSREPORTING': ('analyticsreporting', 'v4'),
        'ANDROIDDEVICEPROVISIONING': ('androiddeviceprovisioning', 'v1'),
        'ANDROIDENTERPRISE': ('androidenterprise', 'v1'),
        'ANDROIDMANAGEMENT': ('androidmanagement', 'v1'),
        'ANDROIDPUBLISHER': ('androidpublisher', 'v3'),
        'APIGATEWAY': ('apigateway', 'v1'),
        'APIGEE': ('apigee', 'v1'),
        'APIGEEREGISTRY': ('apigeeregistry', 'v1'),
        'APIKEYS': ('apikeys', 'v2'),
        'APPENGINE': ('appengine', 'v1'),
        'AREA120TABLES': ('area120tables', 'v1alpha1'),
        'ARTIFACTREGISTRY': ('artifactregistry', 'v1'),
        'ASSUREDWORKLOADS': ('assuredworkloads', 'v1'),
        'AUTHORIZEDBUYERSMARKETPLACE': ('authorizedbuyersmarketplace', 'v1'),
        'BAREMETALSOLUTION': ('baremetalsolution', 'v2'),
        'BEYONDCORP': ('beyondcorp', 'v1'),
        'BIGQUERY': ('bigquery', 'v2'),
        'BIGQUERYCONNECTION': ('bigqueryconnection', 'v1beta1'),
        'BIGQUERYDATATRANSFER': ('bigquerydatatransfer', 'v1'),
        'BIGQUERYRESERVATION': ('bigqueryreservation', 'v1'),
        'BIGTABLEADMIN': ('bigtableadmin', 'v2'),
        'BILLINGBUDGETS': ('billingbudgets', 'v1'),
        'BINARYAUTHORIZATION': ('binaryauthorization', 'v1'),
        'BLOGGER': ('blogger', 'v3'),
        'BOOKS': ('books', 'v1'),
        'BUSINESSPROFILEPERFORMANCE': ('businessprofileperformance', 'v1'),
        'CALENDAR': ('calendar', 'v3'),
        'CERTIFICATEMANAGER': ('certificatemanager', 'v1'),
        'CHAT': ('chat', 'v1'),
        'CHROMEMANAGEMENT': ('chromemanagement', 'v1'),
        'CHROMEPOLICY': ('chromepolicy', 'v1'),
        'CHROMEUXREPORT': ('chromeuxreport', 'v1'),
        'CIVICINFO': ('civicinfo', 'v2'),
        'CLASSROOM': ('classroom', 'v1'),
        'CLOUDASSET': ('cloudasset', 'v1'),
        'CLOUDBILLING': ('cloudbilling', 'v1'),
        'CLOUDBUILD': ('cloudbuild', 'v1'),
        'CLOUDCHANNEL': ('cloudchannel', 'v1'),
        'CLOUDDEBUGGER': ('clouddebugger', 'v2'),
        'CLOUDDEPLOY': ('clouddeploy', 'v1'),
        'CLOUDERRORREPORTING': ('clouderrorreporting', 'v1beta1'),
        'CLOUDFUNCTIONS': ('cloudfunctions', 'v2'),
        'CLOUDIDENTITY': ('cloudidentity', 'v1'),
        'CLOUDIOT': ('cloudiot', 'v1'),
        'CLOUDKMS': ('cloudkms', 'v1'),
        'CLOUDPROFILER': ('cloudprofiler', 'v2'),
        'CLOUDRESOURCEMANAGER': ('cloudresourcemanager', 'v3'),
        'CLOUDSCHEDULER': ('cloudscheduler', 'v1'),
        'CLOUDSEARCH': ('cloudsearch', 'v1'),
        'CLOUDSHELL': ('cloudshell', 'v1'),
        'CLOUDSUPPORT': ('cloudsupport', 'v2beta'),
        'CLOUDTASKS': ('cloudtasks', 'v2'),
        'CLOUDTRACE': ('cloudtrace', 'v2'),
        'COMPOSER': ('composer', 'v1'),
        'COMPUTE': ('compute', 'v1'),
        'CONNECTORS': ('connectors', 'v2'),
        'CONTACTCENTERINSIGHTS': ('contactcenterinsights', 'v1'),
        'CONTAINER': ('container', 'v1'),
        'CONTAINERANALYSIS': ('containeranalysis', 'v1'),
        'CONTENT': ('content', 'v2.1'),
        'CUSTOMSEARCH': ('customsearch', 'v1'),
        'DATACATALOG': ('datacatalog', 'v1'),
        'DATAFLOW': ('dataflow', 'v1b3'),
        'DATAFUSION': ('datafusion', 'v1'),
        'DATALABELING': ('datalabeling', 'v1beta1'),
        'DATAMIGRATION': ('datamigration', 'v1'),
        'DATAPIPELINES': ('datapipelines', 'v1'),
        'DATAPLEX': ('dataplex', 'v1'),
        'DATAPROC': ('dataproc', 'v1'),
        'DATASTORE': ('datastore', 'v1'),
        'DATASTREAM': ('datastream', 'v1'),
        'DEPLOYMENTMANAGER': ('deploymentmanager', 'v2'),
        'DFAREPORTING': ('dfareporting', 'v4'),
        'DIALOGFLOW': ('dialogflow', 'v3'),
        'DIGITALASSETLINKS': ('digitalassetlinks', 'v1'),
        'DISCOVERY': ('discovery', 'v1'),
        'DISPLAYVIDEO': ('displayvideo', 'v2'),
        'DLP': ('dlp', 'v2'),
        'DNS': ('dns', 'v1'),
        'DOCS': ('docs', 'v1'),
        'DOCUMENTAI': ('documentai', 'v1'),
        'DOMAINS': ('domains', 'v1'),
        'DOMAINSRDAP': ('domainsrdap', 'v1'),
        'DOUBLECLICKBIDMANAGER': ('doubleclickbidmanager', 'v2'),
        'DOUBLECLICKSEARCH': ('doubleclicksearch', 'v2'),
        'DRIVE': ('drive', 'v3'),
        'DRIVEACTIVITY': ('driveactivity', 'v2'),
        'DRIVELABELS': ('drivelabels', 'v2'),
        'ESSENTIALCONTACTS': ('essentialcontacts', 'v1'),
        'EVENTARC': ('eventarc', 'v1'),
        'FACTCHECKTOOLS': ('factchecktools', 'v1alpha1'),
        'FCM': ('fcm', 'v1'),
        'FCMDATA': ('fcmdata', 'v1beta1'),
        'FILE': ('file', 'v1'),
        'FIREBASE': ('firebase', 'v1beta1'),
        'FIREBASEAPPCHECK': ('firebaseappcheck', 'v1'),
        'FIREBASEDATABASE': ('firebasedatabase', 'v1beta'),
        'FIREBASEDYNAMICLINKS': ('firebasedynamiclinks', 'v1'),
        'FIREBASEHOSTING': ('firebasehosting', 'v1'),
        'FIREBASEML': ('firebaseml', 'v1'),
        'FIREBASERULES': ('firebaserules', 'v1'),
        'FIREBASESTORAGE': ('firebasestorage', 'v1beta'),
        'FIRESTORE': ('firestore', 'v1'),
        'FITNESS': ('fitness', 'v1'),
        'FORMS': ('forms', 'v1'),
        'GAMES': ('games', 'v1'),
        'GAMESCONFIGURATION': ('gamesConfiguration', 'v1configuration'),
        'GAMESERVICES': ('gameservices', 'v1'),
        'GAMESMANAGEMENT': ('gamesManagement', 'v1management'),
        'GENOMICS': ('genomics', 'v2alpha1'),
        'GKEBACKUP': ('gkebackup', 'v1'),
        'GKEHUB': ('gkehub', 'v1'),
        'GMAIL': ('gmail', 'v1'),
        'GMAILPOSTMASTERTOOLS': ('gmailpostmastertools', 'v1'),
        'GROUPSMIGRATION': ('groupsmigration', 'v1'),
        'GROUPSSETTINGS': ('groupssettings', 'v1'),
        'HEALTHCARE': ('healthcare', 'v1'),
        'HOMEGRAPH': ('homegraph', 'v1'),
        'IAM': ('iam', 'v1'),
        'IAMCREDENTIALS': ('iamcredentials', 'v1'),
        'IAP': ('iap', 'v1'),
        'IDEAHUB': ('ideahub', 'v1beta'),
        'IDENTITYTOOLKIT': ('identitytoolkit', 'v3'),
        'IDS': ('ids', 'v1'),
        'INDEXING': ('indexing', 'v3'),
        'INTEGRATIONS': ('integrations', 'v1alpha'),
        'JOBS': ('jobs', 'v4'),
        'KEEP': ('keep', 'v1'),
        'KGSEARCH': ('kgsearch', 'v1'),
        'LANGUAGE': ('language', 'v1'),
        'LIBRARYAGENT': ('libraryagent', 'v1'),
        'LICENSING': ('licensing', 'v1'),
        'LIFESCIENCES': ('lifesciences', 'v2beta'),
        'LOCALSERVICES': ('localservices', 'v1'),
        'LOGGING': ('logging', 'v2'),
        'MANAGEDIDENTITIES': ('managedidentities', 'v1'),
        'MANUFACTURERS': ('manufacturers', 'v1'),
        'MEMCACHE': ('memcache', 'v1'),
        'METASTORE': ('metastore', 'v1beta'),
        'ML': ('ml', 'v1'),
        'MONITORING': ('monitoring', 'v3'),
        'MYBUSINESSACCOUNTMANAGEMENT': ('mybusinessaccountmanagement', 'v1'),
        'MYBUSINESSBUSINESSCALLS': ('mybusinessbusinesscalls', 'v1'),
        'MYBUSINESSBUSINESSINFORMATION': ('mybusinessbusinessinformation', 'v1'),
        'MYBUSINESSLODGING': ('mybusinesslodging', 'v1'),
        'MYBUSINESSNOTIFICATIONS': ('mybusinessnotifications', 'v1'),
        'MYBUSINESSPLACEACTIONS': ('mybusinessplaceactions', 'v1'),
        'MYBUSINESSQANDA': ('mybusinessqanda', 'v1'),
        'MYBUSINESSVERIFICATIONS': ('mybusinessverifications', 'v1'),
        'NETWORKCONNECTIVITY': ('networkconnectivity', 'v1'),
        'NETWORKMANAGEMENT': ('networkmanagement', 'v1'),
        'NETWORKSECURITY': ('networksecurity', 'v1'),
        'NETWORKSERVICES': ('networkservices', 'v1'),
        'NOTEBOOKS': ('notebooks', 'v1'),
        'OAUTH2': ('oauth2', 'v2'),
        'ONDEMANDSCANNING': ('ondemandscanning', 'v1'),
        'ORGPOLICY': ('orgpolicy', 'v2'),
        'OSCONFIG': ('osconfig', 'v1'),
        'OSLOGIN': ('oslogin', 'v1'),
        'PAGESPEEDONLINE': ('pagespeedonline', 'v5'),
        'PAYMENTSRESELLERSUBSCRIPTION': ('paymentsresellersubscription', 'v1'),
        'PEOPLE': ('people', 'v1'),
        'PLAYCUSTOMAPP': ('playcustomapp', 'v1'),
        'PLAYDEVELOPERREPORTING': ('playdeveloperreporting', 'v1beta1'),
        'PLAYINTEGRITY': ('playintegrity', 'v1'),
        'POLICYANALYZER': ('policyanalyzer', 'v1'),
        'POLICYSIMULATOR': ('policysimulator', 'v1'),
        'POLICYTROUBLESHOOTER': ('policytroubleshooter', 'v1'),
        'POLY': ('poly', 'v1'),
        'PRIVATECA': ('privateca', 'v1'),
        'PROD_TT_SASPORTAL': ('prod_tt_sasportal', 'v1alpha1'),
        'PUBSUB': ('pubsub', 'v1'),
        'PUBSUBLITE': ('pubsublite', 'v1'),
        'REALTIMEBIDDING': ('realtimebidding', 'v1'),
        'RECAPTCHAENTERPRISE': ('recaptchaenterprise', 'v1'),
        'RECOMMENDATIONENGINE': ('recommendationengine', 'v1beta1'),
        'RECOMMENDER': ('recommender', 'v1'),
        'REDIS': ('redis', 'v1'),
        'RESELLER': ('reseller', 'v1'),
        'RESOURCESETTINGS': ('resourcesettings', 'v1'),
        'RETAIL': ('retail', 'v2'),
        'RUN': ('run', 'v2'),
        'RUNTIMECONFIG': ('runtimeconfig', 'v1'),
        'SAFEBROWSING': ('safebrowsing', 'v4'),
        'SASPORTAL': ('sasportal', 'v1alpha1'),
        'SCRIPT': ('script', 'v1'),
        'SEARCHCONSOLE': ('searchconsole', 'v1'),
        'SECRETMANAGER': ('secretmanager', 'v1'),
        'SECURITYCENTER': ('securitycenter', 'v1'),
        'SERVICECONSUMERMANAGEMENT': ('serviceconsumermanagement', 'v1'),
        'SERVICECONTROL': ('servicecontrol', 'v2'),
        'SERVICEDIRECTORY': ('servicedirectory', 'v1'),
        'SERVICEMANAGEMENT': ('servicemanagement', 'v1'),
        'SERVICENETWORKING': ('servicenetworking', 'v1'),
        'SERVICEUSAGE': ('serviceusage', 'v1'),
        'SHEETS': ('sheets', 'v4'),
        'SITEVERIFICATION': ('siteVerification', 'v1'),
        'SLIDES': ('slides', 'v1'),
        'SMARTDEVICEMANAGEMENT': ('smartdevicemanagement', 'v1'),
        'SOURCEREPO': ('sourcerepo', 'v1'),
        'SPANNER': ('spanner', 'v1'),
        'SPEECH': ('speech', 'v1'),
        'SQLADMIN': ('sqladmin', 'v1'),
        'STORAGE': ('storage', 'v1'),
        'STORAGETRANSFER': ('storagetransfer', 'v1'),
        'STREETVIEWPUBLISH': ('streetviewpublish', 'v1'),
        'STS': ('sts', 'v1'),
        'TAGMANAGER': ('tagmanager', 'v2'),
        'TASKS': ('tasks', 'v1'),
        'TESTING': ('testing', 'v1'),
        'TEXTTOSPEECH': ('texttospeech', 'v1'),
        'TOOLRESULTS': ('toolresults', 'v1beta3'),
        'TPU': ('tpu', 'v1'),
        'TRAFFICDIRECTOR': ('trafficdirector', 'v2'),
        'TRANSCODER': ('transcoder', 'v1'),
        'TRANSLATE': ('translate', 'v3'),
        'VAULT': ('vault', 'v1'),
        'VERIFIEDACCESS': ('verifiedaccess', 'v2'),
        'VERSIONHISTORY': ('versionhistory', 'v1'),
        'VIDEOINTELLIGENCE': ('videointelligence', 'v1'),
        'VISION': ('vision', 'v1'),
        'VMMIGRATION': ('vmmigration', 'v1'),
        'WEBFONTS': ('webfonts', 'v1'),
        'WEBRISK': ('webrisk', 'v1'),
        'WEBSECURITYSCANNER': ('websecurityscanner', 'v1'),
        'WORKFLOWEXECUTIONS': ('workflowexecutions', 'v1'),
        'WORKFLOWS': ('workflows', 'v1'),
        'YOUTUBE': ('youtube', 'v3'),
        'YOUTUBEANALYTICS': ('youtubeAnalytics', 'v2'),
        'YOUTUBEREPORTING': ('youtubereporting', 'v1')})


Service = S('Service', list(SERVICE_DEFINITIONS.keys()))
