"""
# Script to connect to WiFirst portal

Based on https://www.jgachelin.fr/connexion-automatique-au-portail-captif-wifirst/

> Python => 3.5
> Date: January 2018
> Verion: 0.1

# Execution #
    
    python ConnectToWifirst.py <username> <password> [--debug]
    
"""

# utf8 field in Wifirst login form
utf8 = "&#x2713"

# URL to test if there is access to Internet.
# Do not use HTTPS, because of certificates the connection will fail. 
# Use HTTP only, and a site that replies HTTP 200 directly.
testURL = "http://www.example.org"

import requests  
import sys
import argparse
import re

#Global flag for Debug output
DEBUG = False

def connectWiFirst(username, password):
    """
        Checks if there is already access to Internet, then follows the Wifirst login process through forms and redirections
        
        The function will output messages to STDOUT, and return a boolean result if Internet is working fine before|after the authentication
        
        :param username/password: are strings, corresponding to the Wifirst account
        
        :return boolean: true if Internet access is working OK, either before or after the authentication.
        
    """   

    global DEBUG
    
    if username=="" or password == "":
        print("ERR: Missing username or password")
        return False

    # Try to access internet
    try:
        examplePage = requests.get(testURL, allow_redirects=False)
    except:
        print("ERR: Unable to reach Internet, check network connectivity and test with "+testURL)
        return False
        
    if examplePage.status_code == 200:
        print("OK: Internet working fine")
        return True
    
    elif examplePage.status_code == 302:
        
        # Redirected to the Wifirst login site
        try:
            wifirstPage = requests.get("https://selfcare.wifirst.net/sessions/new")
        except:
            print("ERR: Unable to reach Wifirst selfcare site") 
            return False
            
        if wifirstPage.status_code == 200:
            
            #Get the form token value            
            #The token is the only value with 46 characters
            
            try:
                longTokenValueRegex = re.compile('value="([^"]{30,})"')
                token = longTokenValueRegex.search(str(wifirstPage.content)).group(1)
            except:
            
                print("ERR: Unable to get token!")
                if DEBUG:
                    print("-"*20 + wifirstPage.url)
                    print(wifirstPage.content)
                    print("-"*40)
                return False    
            
            print("INFO: Token is " + token)
            
            # A session is used to keep the cookies through the process
            aSession = requests.Session()
            postData = {"login":username , "password":password, "authenticity_token":token,"utf8":utf8}
            
            #Send the authentication form, with the credentials
            try:
                wifirstPage = aSession.post("https://selfcare.wifirst.net/sessions", data=postData, allow_redirects=False)
            except:
                print("ERR: Unable to reach Wifirst selfcare site with a POST request") 
                return False
            
            # If the authenticatino is ok, a redirection will take place
            
            if wifirstPage.status_code == 302:
                
                try:
                    wifirstPage = aSession.get("https://connect.wifirst.net/?perform=true")
                except:
                    print("ERR: Unable to reach Wifirst redirected site") 
                    return False
    
                # The returned page content has an automatically filled form, that will submit on loading
                # On a Browser, as the content has an 'onLoad' function, it will automatically send the form with the credentials
            
                #Wifirst login form
                try:
                    wifirstLoginFormRegex = re.compile('action="(https://[a-zA-Z0-9:\./]+)"')
                    wifirstUsernameRegex = re.compile('name="username"\s+type="hidden"\s+value="(w/[0-9]+@wifirst.net)"')
                    wifirstPasswordRegex = re.compile('name="password"\s+type="hidden"\s+value="([a-zA-Z0-9]+)"')
                
                    wifirstLoginForm = wifirstLoginFormRegex.search(str(wifirstPage.content)).group(1)
                    wifirstUsername = wifirstUsernameRegex.search(str(wifirstPage.content)).group(1)
                    wifirstPassword = wifirstPasswordRegex.search(str(wifirstPage.content)).group(1)
                    
                except: 
                    print("ERR: Unable to get the Wifirst Credentials!")
                    if DEBUG:
                        print("-"*20 + wifirstPage.url)
                        print(wifirstPage.content)
                        print("-"*40)
                    return False
                
                
                
                print("INFO: Wifirst Usename = '" + wifirstUsername + "' LoginPage = '" + wifirstLoginForm +"'")
                
                #Now send the second authentication form and credentials
                
                postData = {"username":wifirstUsername , "password":wifirstPassword, "qos_class":"","success_url":testURL, "error_url":"https://connect.wifirst.net/login_error"}
                try:
                    wifirstPage = aSession.post(wifirstLoginForm, data=postData, allow_redirects=True)
                except:
                    print("ERR: Unable to reach Wifirst login form") 
                    return False
                
                if wifirstPage.status_code == 200:
                    if wifirstPage.url == testURL:
                        print("OK: Authentication sucessfull")
                        return True
                    else:
                        print("ERR: Authentication failed, redirected to " + wifirstPage.url)
                else:
                    print("ERR: Final authentication failed with error " + str(wifirstPage.status_code)) 
                    return False
            
            # If the self care POST returns 200, it means that the Wifirst authentiation failed
            
            elif wifirstPage.status_code == 200:
                print("ERR: Wrong credentials!")
                return False
            else :
                print("ERR: Wifirst loging form returned " + str(wifirstPage.status_code))
                return False
        
            
        else:
            print("ERR: Unable to reach Wifirst redirected site") 
            return False
    else :
        print("ERR: Unexpected HTTP Result for "+TestURL)
        return False
#end def


#####################################################################        
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Wifirst username")
    parser.add_argument("password", help="Wifirst password")
    parser.add_argument("--debug","-d", help="Prints the HTTP replies content during the process",  action='store_true')
    try:
        args = parser.parse_args()
    except:
        #print("ERR: Unable to parse arguments, run '--help' option")
        sys.exit(9)

    DEBUG = args.debug
    
    sys.exit(0 if connectWiFirst(args.username, args.password) else 6)
    
    
# Copyright (c) 2018 Jose Ignacio Tamayo Segarra
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.    
