# ConnectToWiFirst

Python script to connect to Wifirst Wifi network.

Originally developed to be installed on a OSMC device, which do not have a Web Browser to perform the web authentication

> Based upon the post https://www.jgachelin.fr/connexion-automatique-au-portail-captif-wifirst/

## How to use

 1. Install python, OSMC already has it installed.

 1. Manually calling the script to connect:
 
'''
python ConnectToWiFirst.py <username> <password>
'''

 1. Replace your WiFirst credentials in 'WiFirst.sh' and then call simply:
 
'''
chmod a+x WiFirst.sh
./WiFirst.sh
'''
 
 2. Copy 'wifirst.service' into the SystemD folder ('/etc/systemd/system/') and install it at boot time:
 
'''
sudo cp wifirst.service /etc/systemd/system/
sudo chmod a+rx /etc/systemd/system/wifirst.service
sudo systemctl daemon-reload
sudo systemctl enable wifirst
sudo service wifirst start
'''

# License notice

Copyright (c) 2018 Jose Ignacio Tamayo Segarra

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
