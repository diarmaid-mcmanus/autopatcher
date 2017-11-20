import subprocess
import sys
import xml.etree.ElementTree as etree
from subprocess import PIPE as SPIPE

apk_file = "example.apk"
debuggable_attribute = "{http://schemas.android.com/apk/res/android}debuggable"
apktool_decode = ["apktool", "d", apk_file ]
apktool_build = ["apktool", "b", "example", "-oexample-debug.apk"]

subprocess.run(apktool_decode, stdout=SPIPE, stderr=SPIPE)

# open example/AndroidManifest.xml
manifest_file = etree.parse('example/AndroidManifest.xml')
# Find Application key
for child in manifest_file.getroot():
    if child.tag == "application":
        child.attrib[debuggable_attribute] = 'true'

# Write application manifest back out
manifest_file.write('example/AndroidManifest.xml', encoding="unicode")

subprocess.run(apktool_build, stdout=SPIPE, stderr=SPIPE)


