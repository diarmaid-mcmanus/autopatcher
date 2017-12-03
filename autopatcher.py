import androguard
from androguard.core.bytecodes import apk
from androguard.core.bytecodes.dvm import DalvikVMFormat
import subprocess
import time
import xml.etree.ElementTree as etree
from subprocess import PIPE as SPIPE

apk_file = "example.apk"
debuggable_attribute = "{http://schemas.android.com/apk/res/android}debuggable"
apktool_decode = ["apktool", "d", apk_file ]
apktool_build = ["apktool", "b", "example", "-oexample-debug.apk"]
jarsigner_sign = ["jarsigner", "-verbose", "-sigalg", "SHA1withRSA", 
    "-digestalg", "SHA1", "-keystore", "autopatcher.jks", "-storepass", "password",
    "example-debug.apk", "autopatcher-keystore" ]
attack_surface = [ 'activity', 'service', 'receiver', 'provider' ]

# TODO verify properly signed apk
# Shouldn't I be able to do this with Androguard?

# Step one : make APK debuggable, sign it
subprocess.run(apktool_decode, stdout=SPIPE, stderr=SPIPE)

manifest_file = etree.parse('example/AndroidManifest.xml')

for child in manifest_file.getroot():
    if child.tag == "application":
        child.attrib[debuggable_attribute] = 'true'

manifest_file.write('example/AndroidManifest.xml', encoding="unicode")

subprocess.run(apktool_build, stdout=SPIPE, stderr=SPIPE)
# this doesn't align the zip because we're not releasing it.
subprocess.run(jarsigner_sign, stdout=SPIPE, stderr=SPIPE)

# Step two: do static analysis using androguard
apkf = apk.APK(apk_file)

activities = apkf.get_activities()
receivers = apkf.get_receivers()
services = apkf.get_services()
providers = apkf.get_providers()

exported_activities = []
exported_receivers = []
dynamic_exported_receivers = []
exported_services = []
exported_providers = []

for activity in activities:
    if apkf.get_element('activity', 'exported', name=activity) == 'true':
        exported_activities.append(activity)
    else:
        filters = apkf.get_intent_filters("activity", activity)
        if len(filters) > 0:
            exported_activities.append(activity)

for receiver in receivers:
    if apkf.get_element('receiver', 'exported', name=receiver) == 'true':
        exported_receivers.append(receiver)
    else:
        filters = apkf.get_intent_filters("receiver", receiver)
        if len(filters) > 0:
            exported_receivers.append(receiver)

dexf = DalvikVMFormat(apkf.get_dex())

for item in dexf.get_classes_def_item().get_obj():
    if "BroadcastReceiver" in str(item):
        dynamic_exported_receivers.append(item)

for service in services:
    if apkf.get_element('service', 'exported', name=service) == 'true':
        exported_services.append(service)
    else:
        filters = apkf.get_intent_filters("service", service)
        if len(filters) > 0:
            exported_services.append(service)

if int(apkf.get_target_sdk_version()) < 17:
    exported_providers = providers
else:
    for provider in providers:
        if apkf.get_element('provider', 'exported', name=provider) == 'true':
            exported_providers.append(provider)
        else:
            filters = apkf.get_intent_filters('provider', provider)
            if len(filters) > 0:
                exported_providers.append(provider)

print(apkf.get_app_name())

print("\nActivities:")
for activity in exported_activities:
    print(activity)

print("\nReceivers (static):")
for receiver in exported_receivers:
    print(receiver)

print("\nReceivers (dynamic):")
for receiver in dynamic_exported_receivers:
    print(receiver)

print("\nServices:")
for service in exported_services:
    print(service)

print("\nProviders:")
for provider in exported_providers:
    print(provider)
