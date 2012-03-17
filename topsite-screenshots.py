# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

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