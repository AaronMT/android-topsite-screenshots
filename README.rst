README
========

android-topsite-screenshots

android-topsite-screenshots is a [MonkeyRunner](http://developer.android.com/tools/help/monkeyrunner_concepts.html) script that runs through various available Android internet browsers (e.g, com.android.browser, Chrome, Opera, Dolphin and Firefox) visiting any provided (CSV listing) of sites and takes screenshots. It is a simple script.

How to Run
__________

* Install the [Android SDK](http://developer.android.com/sdk/index.html)
* Edit the script and the `browser` array to provide the appropriate browser package/activity  names that you want your run to use (e.g, `com.android.chrome/.Main` and `com.android.browser`)
* From within the Android SDK is the utility `monkeyrunner`. Run `monkeyrunner topsite-screenshots.py <sites.csv> <directory-of-screenshots-to-save-to>`
* Example: `monkeyrunner topsite-screenshots.py topsites.csv ~/Desktop/screenshots/`

Project details
_______________

Code:
    https://github.com/AaronMT/android-topsite-screenshots

Issue tracker:
    https://github.com/AaronMT/android-topsite-screenshots/issues

IRC:
    ``#mobile`` on irc.mozilla.org

License:
    Mozilla Public License [MPL](http://www.mozilla.org/MPL/)