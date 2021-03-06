+++++++++
Stuhlgang
+++++++++

Run it in browser
=================

1.  You gotta install cordova::

        $ sudo npm -g install cordova

2.  You gotta add "browser" as a platform::

        $ cordova platform add browser

3.  Now you can fire up the app in your browser, like so::

        $ cordova run browser

And now you should hopefully see your browser open
http://localhost:8000/ or something like that, and you'll see a goofy
robot and a green blinking button "device is ready".

Here is a fun fact... if you alter some of the HTML code in www/, and
then reload the browser, too bad!  You won't see your changes.  You
gotta do this::

    $ cordova prepare browser

Or, just kill the process running in the "cordova run browser" tab and
rerun it.

You'll remember to do this most of the time, but not always, and you'll
start going crazy when you're wondering why stuff isn't changing.

Build stuff with build.phonegap
===============================

This is how you can build the executables suitable for installing on the
phone.

Log into build.phonegap.com with these credentials:

    ask Matt for these -- since this is an open-source repo, I shouldn't
    put them in here.

And then on the "Apps" tab, look for StuhlGang.  Click on the StuhlGang
text.

Then you gotta make sure you have already pushed all the code up to the
github repo, because that's where build.phonegap pulls from.

Then after you pushed it up, click "Update Code" and then after that,
"Rebuild All".

HURRAY!!!

Right now, the android app will build A-OK.

If you download the apk file on your phone and then open it, you'll get
prompted to install the app.

The iOS version needs me to do some tedious crap involving uploading a
dev key, which I can do, but I don't really want to do right now, but I
will do it.

.. vim: set syntax=rst:
