#!/usr/bin/python

__author__ = 'aaron.train@gmail.com'

import sys
import optparse
import json
import os
import time

_browser_intents = {'android' : 'com.google.android.browser/com.android.browser.BrowserActivity',
					'fennec-native' : 'org.mozilla.fennec/.App',
              		'opera' : 'com.opera.browser/com.opera.Opera'}

class StartupOptions(optparse.OptionParser):
	def __init__(self, configFile=None, **kwargs):
		optparse.OptionParser.__init__(self, **kwargs)
		defaults = {}

		self.add_option("--sites", action="store", dest="sites", type="string",
						help="Provide a JSON list of top sites")
		defaults["sites"] = None

class topsite_screenshots:
	def __init__(self, options):
		self.sites = options.sites

	def Run(self):
		self.sites = self._read_json(self.sites)
		self._topsite_screenshots()

	def _read_json(self, _jsonfile):
		self.json_file = open(_jsonfile).read()
		self.json_data = json.loads(self.json_file)
		return self.json_data

	def _topsite_screenshots(self):
		self._createDir()
		for index, intent in enumerate(_browser_intents.itervalues()):
			for site in self.sites:
				self._startBrowserIntent(intent, site)
				time.sleep(12) #Hack: Need to figure out wait for page load
				self._createScreenshot("%s-%s" % (self.sites.index(site), index))

	def _startBrowserIntent(self, intent, site):
		os.system("adb shell am start -a android.intent.action.VIEW -n %s %s" % (intent, site))

	def _createScreenshot(self, index):
		os.system("adb pull /dev/graphics/fb0 fb0")
		os.system("dd bs=1920 count=800 if=fb0 of=fb0b")
		os.system("ffmpeg -vframes 1 -vcodec rawvideo -f rawvideo -pix_fmt rgb32 -s 480x800 -i fb0b -f image2 -vcodec png %s.png" % (index))

	def _createDir(self):
		t = time.localtime()
		timestamp = time.strftime('%b-%d-%Y', t)
		
		if not os.path.exists(timestamp):
			os.mkdir(timestamp)
			os.chdir(timestamp)
		elif os.path.exists(timestamp):
			os.chdir(timestamp)

def main():
	parser = StartupOptions()
	options, args = parser.parse_args()

	if not options:
		raise Exception('Options', 'Invalid options passed to topsite-screenshots')

	n = topsite_screenshots(options)
	n.Run()

if __name__ == "__main__":
	main()