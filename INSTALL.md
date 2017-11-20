Insall apktool & put it on your path github.com/iBotPeaches/Apktool
Install jarsigner and configure it per developer.android.com
keytool -genkey -v -keystore autopatcher.jks -keyalg RSA -keysize 2048 -storepass password -validity 10000 -alias autopatcher-keystore
Set up a virtualenv
Install androguard
python autopatcher.py example # this will patch example.apk 
