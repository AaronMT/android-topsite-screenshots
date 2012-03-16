# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is android-topsite-screenshots.
#
# The Initial Developer of the Original Code is Aaron Train.
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#  Aaron Train <atrain@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys, csv

browsers = ['com.android.chrome/.Main',
            'org.mozilla.fennec/.App']

def main():
    # Connects to the current device, returning a MonkeyDevice object
    device = MonkeyRunner.waitForConnection()

    #Start each browser activity with the provided URI
    for run, browser in enumerate(browsers):
        
        # Visit each site
        for visit, site in enumerate(csv.reader(open(sys.argv[1]).readlines())):
            
            # Start the activity with the provided site
            device.startActivity(component=browser, uri=site[0])
            
            # Wait for page load timeout
            MonkeyRunner.sleep(20) # Sleep 20 seconds between page loads

            # Snap a screenshot of the running activity
            device.takeSnapshot().writeToFile("%s%s-%s.png" % (sys.argv[2], visit, run), 'png')

if __name__ == "__main__":
	main()