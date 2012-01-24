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
# The Initial Developer of the Original Code is
# Aaron Train.
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

import optparse
import json
import time
import subprocess
import os

_browser_intents = {'android' : 'com.google.android.browser/com.android.browser.BrowserActivity',
					'fennec-native' : 'org.mozilla.fennec/.App',
              		'opera' : 'com.opera.browser/com.opera.Opera'}

waitForPageLoad = 0 #TODO: Need to figure out a better wait for page load

class StartupOptions(optparse.OptionParser):
	def __init__(self, configFile=None, **kwargs):
		optparse.OptionParser.__init__(self, **kwargs)

		self.add_option("--sites", action="store", dest="sites", type="string",
						help="Provide a JSON list of top sites to visit")
		
		self.add_option("--dir", action="store", dest="dir", type="string",
						help="Provide an existing directory to store PNG screenshots")

	def verify_options(self, options):
		if(not os.path.exists(options.dir)):
			print "Provided directory %s does not exist" % options.dir
			return False
		
		if(not os.path.isfile(options.sites)):
			print "Provided JSON list %s does not exist" % options.sites
			return False

		return options

class topsite_screenshots:
	def __init__(self, options):
		self.sites = options.sites
		self.dir = options.dir

	def Run(self):
		self.sites = self._read_json(self.sites)
		self._startBrowserAndScreenshot()

	def _read_json(self, _jsonfile):
		self.json_file = open(_jsonfile).read()
		self.json_data = json.loads(self.json_file)
		return self.json_data

	def _startBrowserAndScreenshot(self):
		for index, intent in enumerate(_browser_intents.itervalues()):
			for site in self.sites:
				self._startBrowserIntent(intent, site)
				self._createScreenshot("%s-%s" % (self.sites.index(site), index))
			self._killBrowser(intent)

	def _startBrowserIntent(self, intent, site):
		subprocess.call(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-n", intent, site])
		time.sleep(waitForPageLoad)

	def _createScreenshot(self, index):
		subprocess.call(["adb", "pull", "/dev/graphics/fb0", "%s%s" % (self.dir, "fb0")])
		subprocess.call(["dd", "bs=1920", "count=800", "if=%s%s" % (self.dir, "fb0"), "of=%s%s" % (self.dir, "fb0b")])
		subprocess.call(["ffmpeg", "-vframes", "1", "-vcodec", "rawvideo", "-f", "rawvideo", "-pix_fmt", 
						 "rgb32", "-s", "480x800", "-i", "%s%s" % (self.dir, "fb0b"), "-f", "image2", "-vcodec", "png",
						 "%s%s.png" % (self.dir, index)])
	
	def _killBrowser(self, intent):
		pid = subprocess.Popen(["-c", "adb shell ps | grep %s | awk ' {print $2} '" % (intent.split("/")[0])], 
		                        stdin=subprocess.PIPE, shell=True)
		pid.communicate("")
		pid.wait()

		subprocess.call(["adb", "shell", "run-as", intent.split("/")[0], "kill", pid])

def main():
	parser = StartupOptions()
	(options, args) = parser.parse_args()

	options = parser.verify_options(options)

	if not options:
		raise Exception('Options', 'Invalid options passed to topsite-screenshots')

	n = topsite_screenshots(options)
	n.Run()

if __name__ == "__main__":
	main()