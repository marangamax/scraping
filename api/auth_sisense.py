import json 
import time 
import jwt
import urllib
import requests
import yaml
import sys

# This script follow the sisense API documentation(http://www.sisense.com/documentation/sisense-rest-api/)
# to run sql queries from scripts
class Sisense_api():
    # given config_file prepare API call
    def __init__(self, config_file):
        # initialize all variables to be authorize to talk to the API
        self.__api_config = self.take_config(config_file)
        try:
            self.url = self.__api_config.get("URL")
            self.__key = self.__api_config.get("key")
            self.__email = self.__api_config.get("email")
            self.__password = self.__api_config.get("password")
        except:
            print 'config_file not found'
            sys.exit(1) 
        self.headers = {'x-api-key': self.__create_jwt_token()}
     
     # look for the configuration file and if not found on the given path return error   
    def take_config(self, config_path):
        try:
            with open(config_path, 'r') as api_connection:
                try:
                    return yaml.load(api_connection)
                except yaml.YAMLError as e:
                    sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))
        except IOError as e:
            print config_path
            sys.exit("Error {0}) : {1}".format(e.errno, e.strerror))
    
    # create auth_token
    def __create_jwt_token(self):
        payload = { "iat": int(time.time()), 
                    'email': self.__email,
                    'password': self.__password
        }
    
        jwt_string = jwt.encode(payload, self.__key)
        encoded_jwt = urllib.quote_plus(jwt_string) # url-encode the jwt string
        return encoded_jwt
    
    # make get request to API given a sql_query 
    # if request return query response return query response, else we will make the
    # tree timers before raising an error
    def make_request(self, query):
        self.counter = 0 # error counter
        self.params = {'query': query}
        while self.counter < 10: 
            self.request = requests.get(self.url, headers=self.headers, params=self.params)
            # check if the api request has correct authorification, if not add one error and
            # try again up to 3 times
            if self.request.status_code == 200:
                try:
                    self.api_response = self.request.json()
                    if not self.api_response.get('type', None):
                        return self.api_response
                    else:
                        print """Api-call trial: %s - requeststatus: %s
                            Api response was not the one expected: JSON response not expected
                            response_status: %s
                            
                                %s
                                """ % (self.counter, self.request.status_code, self.api_response['type'], self.api_response)
                        self.counter += 1
                except Exception, e:
                    print str(e)
                    print """Api-call trial: %s - status: %s
                            Api response was not the one expected: Failed to convert to JSON.
                            
                                %s
                                """ % (self.counter, self.request.status_code, self.request.text)
                    self.counter += 1

            elif self.request.status_code == 503:
                print """ Api-call trial: %s - status: %s
            
                    %s 
                
                    1 - Verify your credentials(make sure that the credentials correspond to an administrator)
                    2 - Restart the server were Sisense is running
                    If any of the following worked please contatct Sisense staff """ % (self.counter, self.request.status_code, self.request.text)
                self.counter += 1
            
            else:
                print """Api-call trial: %s - status: %s
            
                    %s 
                    """ %(self.counter, self.request.status_code, self.request.text)
                self.counter += 1
        
        else:
            sys.exit(""" Api-call failed: number of tries was exceeded. """)
    
    # Sisense API can not handle very heavy queries. i.e: Select * from Table where x in (big_list)
    # chuncker breaks big_lists of arg into many smaller list of args
    def chuncker(self, seq, size):
        self.seq = seq
        pieces = [self.seq[pos:pos + size] for pos in range(0, len(self.seq), size)]
        self.chuncks = [str("("+','.join("'" + i + "'" for i in x)+")") for x in pieces] 
        return self.chuncks
