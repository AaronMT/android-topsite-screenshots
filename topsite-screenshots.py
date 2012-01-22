#!/usr/bin/python

__author__ = 'aaron.train@gmail.com'

import sys, getopt, json, os, time

class topsite_screenshots:
	def __init__(self, sites, browsers):
		self._list_of_sites = self._read_json(sites)
		self._list_of_browsers = self._read_json(browsers)

	def Run(self):
		self._topsite_screenshots()

	def _read_json(self, _jsonfile):
		self.json_file = open(_jsonfile).read()
		self.json_data = json.loads(self.json_file)
		return self.json_data

	def _topsite_screenshots(self):
		for self.n, self.x in enumerate(self._list_of_browsers):
			for self.o, self.y in enumerate(self._list_of_sites):
				self._startBrowserIntent(self.x, self.y)
				time.sleep(12) #Hack: Need to figure out how to wait for page load
				self._createScreenshot("%s-%s" % (self.o, self.n))

	def _startBrowserIntent(self, _browser_intent, _site):
		os.system("adb shell am start -a android.intent.action.VIEW -n %s %s%s" % (_browser_intent, "http://", _site))

	def _createScreenshot(index):
		self._createDir()
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
	try:
		opts, args = getopt.getopt(sys.argv[1:], "", ["sites=", "browsers="])
	except getopt.error, msg:
		print 'python topsite-screenshots.py --sites [sites (JSON)] --browsers [browser intents (JSON)]'
		sys.exit(2)
	
	sites = ""
	browsers = ""

	for o, a in opts:
		if o == "--sites":
			sites = a
		if o == "--browsers":
			browsers = a

	if sites == "" or browsers == "":
		print 'python topsite-screenshots.py --sites [sites (JSON)] --browsers [browser intents (JSON)]'
		sys.exit(2)

	n = topsite_screenshots(sites, browsers)
	n.Run()

if __name__ == "__main__":
	main()