Insall apktool & put it on your path github.com/iBotPeaches/Apktool
Install jarsigner and configure it per developer.android.com
keytool -genkey -v -keystore autopatcher.jks -keyalg RSA -keysize 2048 -storepass password -validity 10000 -alias autopatcher-keystore
Set up a virtualenv
Into the virtualenv, install androguard from github.com/androguard/androguard
python autopatcher.py example # this will patch example.apk and output example-debug.apk with a folder example/
