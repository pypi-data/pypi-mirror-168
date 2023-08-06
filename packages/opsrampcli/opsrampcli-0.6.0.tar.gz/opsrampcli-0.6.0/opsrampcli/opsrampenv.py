from genericpath import exists
import yaml
import sys
import requests
import json
import time
from datetime import datetime
#import opsramp.binding as po_binding
#import opsramp.tenant as po_tenant
#import opsramp.service_maps as po_service_maps

class OpsRampEnv:

    OPS_ALERT_SEARCH_ATTRIBUTES = [
        'states',
        'startDate',
        'endDate',
        'priority',
        'uniqueId',
        'deviceStatus',
        'resourceType',
        'resourceIds',
        'actions',
        'alertTypes',
        'metrics',
        'duration',
        'alertTimeBase',
        'clientIds',
        'ticketId',
        'apps'
    ]
    def __init__(self, env, isSecure=True):
        self.env = env
        self.isSecure = True
        if isinstance(isSecure, str) and (isSecure.lower() == 'false' or isSecure.lower() == 'no' or isSecure == '0'):
            self.isSecure = False

    def get_templates(self, queryString=None):
        return self.get_objects("templates", queryString=queryString)

    def clone_template(self, templateobj, newname, newdesc):
        token = self.get_token()
        url = f'{self.env["url"]}/api/v2/tenants/{self.env["tenant"]}/monitoring/templates/clone'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        #removeattrs = ['id', 'uniqueId', 'name', 'createdDate', 'updatedDate', ]
        body = {}
        body['clonedTemplateId'] = templateobj['uniqueId']
        body['name'] = newname

        response = requests.request("POST", url, headers=headers, data=json.dumps(body), verify=self.isSecure)
        return response.json() 

    def get_service_maps(self, queryString=None):
        return self.get_objects("serviceMaps", queryString=queryString)

    def get_child_service_groups(self, sgId):
        return self.get_objects("childServiceGroups", itemId=sgId)

    def get_service_group(self, sgId):
        return self.get_objects("serviceGroup", itemId=sgId)

    def make_healing_alert(self, alert):
        newalert={}
        newalert['currentState'] = "Ok"
        newalert['device'] = alert['device']
        newalert['metric'] = alert['metric']
        newalert['component'] = alert['component']
        newalert['subject'] = "Heal via script for alert " + alert['uniqueId']
        newalert['description'] = "Healed via script"
        newalert['serviceName'] = alert['serviceName']
        newalert['problemArea'] = alert['problemArea']
        newalert['alertType'] = alert['alertType']
        newalert['app'] = alert['app']
        return newalert

    def post_alert_bearer(self, alert):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/alert"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        print("Sending: %s" % (json.dumps(alert)))
        response = requests.request("POST", url, headers=headers, data=json.dumps(alert), verify=self.isSecure)
        return response.json() 

    def post_alert_vtoken(self, alert):
        url = self.env['url'] + "/integrations/alertsWebhook/" + self.env['tenant'] + "/alerts?vtoken=" + self.env['vtoken']
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        print("Sending: %s" % (json.dumps(alert)))
        response = requests.request("POST", url, headers=headers, data=json.dumps(alert), verify=self.isSecure)
        return response.json()

    def is_in_range(self, range, i):
        ranges = range.split(",")
        for range in ranges:
            # all
            if range == 'all':
                return True
            
            # simple integer value    
            try:
                if i==(int(range)-1):
                    return True
            except:
                pass

            # from-to range
            fromto = range.split("-")
            if len(fromto) == 2:
                lower = fromto[0]
                upper = fromto[1]
                if ((lower == '') or int(lower) <= (i+1)) and  ((upper == '') or int(upper) >= (i+1)):
                    return True

        return False

    def get_alert(self,  alertid):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/alerts/" + str(alertid)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        params = {
        }

        response = requests.request("GET", url, headers=headers, params=params, verify=self.isSecure)
        responseobj = response.json()
        return responseobj


    def do_alert_action(self,  action, alertid):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/alerts/" + str(alertid) + "/actions/" + action
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        data = {
            "description": action + " via script."
        }

        response = requests.request("POST", url, headers=headers, verify=self.isSecure, data = json.dumps(data))
        responseobj = { "status_code": 200}
        if response.status_code != 200:
            responseobj = response.json()
        return responseobj

    def validate_alert_query(self, query):
        invalid_search_attrs = set([a.split(":")[0] for a in query.split("+")]).difference(set(self.OPS_ALERT_SEARCH_ATTRIBUTES))
        if len(invalid_search_attrs) > 0:
            raise ValueError('Alert search query contains invalid search attributes: %s\nValid search attributes are: %s' % (invalid_search_attrs, self.OPS_ALERT_SEARCH_ATTRIBUTES))
        return True

    def get_alerts_count(self, query):
        self.validate_alert_query(query)
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/alerts/search"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            'queryString': query,
            'pageSize': 1
        }

        count = 0
        responseobj = {}
        try:
            response = requests.request("GET", url, headers=headers, params=params, verify=self.isSecure)
            responseobj = response.json()
            count = responseobj['totalResults']
        except Exception as e:
            print(repr(responseobj))
            print(repr(e))
            print("Exception encountered.")
        return count



    def get_alerts(self, query, page=1, brief=False, details=False, filter=""):
        self.validate_alert_query(query)
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/alerts/search"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            'queryString': query,
            'pageNo': page,
            'pageSize': 500
        }

        got_result = False
        while not got_result:
            try:
                response = requests.request("GET", url, headers=headers, params=params, verify=self.isSecure)
                responseobj = response.json()
                results = responseobj['results']
                got_result = True
            except Exception as e:
                print(repr(responseobj))
                print(repr(e))
                print("Exception on page %d.  Processing partial results." % (page))
                return []

        alerts = []
        if brief:
            for result in results:
                alerts.append({
                    'uniqueId': result['uniqueId'],
                    'createdDate': result['createdDate'],
                    'updatedTime': result['updatedTime'],
                    'device': { 
                        'name': result['device']['name'],
                        'id': result['device']['id']
                    },
                    'component': result['component'],
                    'metric': result['metric'],
                    'problemArea': result['problemArea'],
                    'subject': result['subject'],
                    'status': result['status'],
                    'eventType': result['eventType'],
                    'alertType': result['alertType'],
                    'currentState': result['currentState'],
                    'repeatCount': result['repeatCount']
                })
        else:
            alerts = results
        if details:
            for alert in alerts:
                details = self.get_alert(alert['uniqueId'])
                alert['description'] = details['description']

        if filter:
            for idx, alert in enumerate(alerts):
                if not eval(filter):
                   del alerts[idx] 

        if responseobj['nextPage']:
            #print("Got %i alerts, proceeding to page %i" % (len(alerts),responseobj['nextPageNo']))
            return alerts + self.get_alerts(query, responseobj['nextPageNo'], brief, details, filter)
        else:
            return alerts

    def post_incident_update(self, id, update):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/incidents/" + id
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        print("Updating %s: %s" % (id, json.dumps(update)))
        response = requests.request("POST", url, headers=headers, data=json.dumps(update), verify=self.isSecure)
        return response.json() 
 
    def get_incidents_count(self, query):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/incidents/search"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            'queryString': query,
            'pageSize': 1
        }

        response = requests.request("GET", url, headers=headers, params=params, verify=self.isSecure)
        responseobj = response.json()
        return responseobj['totalResults']

    def get_incidents(self, query, page=1, brief=False, details=False, filter=""):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/incidents/search"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            'queryString': query,
            'pageNo': page
        }

        response = requests.request("GET", url, headers=headers, params=params, verify=self.isSecure)
        responseobj = response.json()
        results = responseobj['results']
        incidents = []
        if brief:
            for result in results:
                incidents.append({
                    'uniqueId': result['uniqueId'],
                    'createdDate': result['createdDate'],
                    'updatedTime': result['updatedTime'],
                    'device': { 
                        'name': result['device']['name'],
                        'id': result['device']['id']
                    },
                    'component': result['component'],
                    'metric': result['metric'],
                    'problemArea': result['problemArea'],
                    'subject': result['subject'],
                    'status': result['status'],
                    'eventType': result['eventType'],
                    'incidentType': result['incidentType'],
                    'currentState': result['currentState'],
                    'repeatCount': result['repeatCount']
                })
        else:
            incidents = results
        if details:
            for incident in incidents:
                details = self.get_incident(incident['uniqueId'])
                incident['description'] = details['description']

        if filter:
            for idx, incident in enumerate(incidents):
                if not eval(filter):
                   del incidents[idx] 

        if responseobj['nextPage']:
            #print("Got %i incidents, proceeding to page %i" % (len(incidents),responseobj['nextPageNo']))
            return incidents + self.get_incidents(query, responseobj['nextPageNo'], brief, details, filter)
        else:
            return incidents

    def get_token(self):
        url = self.env['url'] + "/auth/oauth/token"

        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.env['client_id'],
            'client_secret': self.env['client_secret']
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=self.isSecure)

            #print(response.text)
            return response.json()['access_token']
        except requests.exceptions.ConnectionError as err:
            print(f'\nUnable to connect to {self.env["url"]}')
            print(f'Please check that this is the correct url and is resolvable/reachable!\n')
            sys.exit(1)
        except Exception as err:
            print(str(err))
            sys.exit(1)


    def get_discoprofile(self, id, tenant):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + tenant + "/policies/discovery/" + id
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("GET", url, headers=headers, verify=self.isSecure)
        responseobj = response.json()
        return responseobj

    def get_alertescalations(self, query='', page=1):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/escalations/search"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            "queryString": query,
            "pageSize": 500,
            "pageNo": page
        }

        response = requests.request("GET", url, headers=headers, verify=self.isSecure, params=params)
        try:
            responseobj = response.json()
        except Exception as e:
            print(repr(response))
            sys.exit(1)

        if "results" in responseobj:
            results = responseobj['results']
        else:
            results = responseobj

        if "nextPage" in responseobj and responseobj['nextPage']:
            #print("Got %i policies from %s, proceeding to page %i" % (len(results), self.env['name'], responseobj['nextPageNo']))
            return results + self.get_alertescalations(query, responseobj['nextPageNo'])
        else:
            return results

    def get_alertescalation(self, allClients, id, params={}):
        for key, val in params.items():
            if val == True:
                params[key] = "true"
        token = self.get_token()
        tenant = self.env['tenant']
        if allClients:
            tenant = self.env['partner']
        url = self.env['url'] + "/api/v2/tenants/" + tenant + "/escalations/" + id
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("GET", url, headers=headers, verify=self.isSecure, params=params)
        try:
            responseobj = response.json()
        except Exception as e:
            print(repr(response))
            sys.exit(1)

        return responseobj

    
    def create_alertescalation(self, policy):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/escalations"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(policy), verify=self.isSecure)
        return response.json()

    def update_alertescalation(self, policy, id):
        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/escalations/" + id
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(policy), verify=self.isSecure)
        return response.json()

    def set_custom_attr_on_devices(self, attr_id, value_id, device_ids):
        devices = []
        if isinstance(device_ids, list):
            devices = device_ids
        elif isinstance(device_ids, str):
            devices.append(device_ids)
        else:
            raise TypeError("device_ids must be an array or a string") 

        payload = []
        for device in devices:
            payload.append({"id": device})

        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/customAttributes/" + str(attr_id) + "/values/" + str(value_id) + "/devices"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=self.isSecure)
        return response.json()     

    def remove_custom_attr_from_devices(self, attr_id, value_id, device_ids):
        devices = []
        if isinstance(device_ids, list):
            devices = device_ids
        elif isinstance(device_ids, str):
            devices.append(device_ids)
        else:
            raise TypeError("device_ids must be an array or a string") 

        payload = []
        for device in devices:
            payload.append({"id": device})

        token = self.get_token()
        url = self.env['url'] + "/api/v2/tenants/" + self.env['tenant'] + "/customAttributes/" + str(attr_id) + "/values/" + str(value_id) + "/devices"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("DELETE", url, headers=headers, data=json.dumps(payload), verify=self.isSecure)
        return response.json() 

    def get_objects(self, obtype, page=1, queryString=None, searchQuery=None,countonly=False, itemId=None):

        endpoints = {
            "clients": self.env['partner'] + "/clients/" + self.env['tenant'],
            "incidentCustomFields": self.env['tenant'] + "/customFields/INCIDENT",
            "deviceGroups": self.env['tenant'] + "/deviceGroups/minimal",
            "userGroups": self.env['tenant'] + "/userGroups",
            "urgencies": self.env['tenant'] + "/incidents/urgencies",
            "customAttributes": self.env['tenant'] + "/customAttributes/search",
            "resources": self.env['tenant'] + "/resources/search",
            "resourcesNewSearch": self.env['tenant'] + "/query/execute",
            "assignedAttributeEntities": self.env['tenant'] + "/customAttributes/" + str(itemId) + "/assignedEntities/search",
            "serviceMaps": self.env['tenant'] + "/serviceGroups/search",
            "childServiceGroups": self.env['tenant'] + "/serviceGroups/" + str(itemId) + "/childs/search",
            "serviceGroup": self.env['tenant'] + "/serviceGroups/" + str(itemId),
            "templates": self.env['tenant'] + "/monitoring/templates/search"
        }

        url = self.env['url'] + "/api/v2/tenants/" + endpoints[obtype]
        token = self.get_token()
 
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = {
            'pageSize': 500,
            'pageNo': page
        }

        if countonly:
            params['pageSize'] = 1

        if queryString:
            params['queryString'] = queryString

        if searchQuery:
            params['searchQuery'] = searchQuery
            params['type'] = "resources"

        if obtype == 'userGroups' or obtype == 'serviceMaps':
            params['pageSize'] = 100

        response = requests.request("GET", url, headers=headers, verify=self.isSecure, params=params)
        try:
            responseobj = response.json()
        except Exception as e:
            print(repr(response))
            sys.exit(1)

        if countonly:
            return int(responseobj['totalResults'])

        if "results" in responseobj:
            results = responseobj['results']
        else:
            results = responseobj
 
        if "nextPage" in responseobj and responseobj['nextPage']:
            #print("Got %i %s from %s, proceeding to page %i" % (len(results), obtype, self.env['name'], responseobj['nextPageNo']))
            return results + self.get_objects(obtype=obtype, page=responseobj['nextPageNo'],queryString=queryString, searchQuery=searchQuery, itemId=itemId)
        else:
            return results
        
    def do_resource_action(self, action, resourceId):
        # Action is manage or unmanage
        token = self.get_token()
        url = f'{self.env["url"]}/api/v2/tenants/{self.env["tenant"]}/devices/{resourceId}/{action}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("POST", url, headers=headers, verify=self.isSecure)
        responseobj = { "status_code": 200}
        if response.status_code != 200:
            responseobj = response.json()


        if int(response.headers['x-ratelimit-remaining']) < 2 :
            sleeptime = int(response.headers['x-ratelimit-reset']) - int(datetime.now().timestamp()) + 3
            print(f'Sleeping for {str(sleeptime)} sec..')
            time.sleep(sleeptime)
        return responseobj

    def delete_resource(self, resourceId):
        token = self.get_token()
        url = f'{self.env["url"]}/api/v2/tenants/{self.env["tenant"]}/resources/{resourceId}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("DELETE", url, headers=headers, verify=self.isSecure)
        responseobj = { "status_code": 200}
        if response.status_code != 200:
            responseobj = response.json()


        if int(response.headers['x-ratelimit-remaining']) < 2 :
            sleeptime = int(response.headers['x-ratelimit-reset']) - int(datetime.now().timestamp()) + 3
            print(f'Sleeping for {str(sleeptime)} sec..')
            time.sleep(sleeptime)
        return responseobj
    
    def create_or_update_service_group(self, svcgroup):
        if type(svcgroup) == list:
            for grp in svcgroup:
                self.create_or_update_service_group(grp)
        token = self.get_token()
        url = f'{self.env["url"]}/api/v2/tenants/{self.env["tenant"]}/serviceGroups/'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        svcgrouparr = [svcgroup]
        response = requests.request("POST", url, headers=headers, verify=self.isSecure, data=json.dumps(svcgrouparr))
        responseobj = response.json()
        if type(responseobj) == list and len(responseobj) > 0:
            return responseobj[0]
        else:
            print(f'Failed to import service group {svcgroup["name"]}:\n{response.json()}')
            return False

    def link_service_group(self, parent, child):
        token = self.get_token()
        url = f'{self.env["url"]}/api/v2/tenants/{self.env["tenant"]}/serviceGroups/link'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        link = [
            {
                "id": child,
                "parent": {
                    "id": parent
                }
            }
        ]
        response = requests.request("POST", url, headers=headers, verify=self.isSecure, data=json.dumps(link))
        if response.status_code == 200:
            return True
        return False
