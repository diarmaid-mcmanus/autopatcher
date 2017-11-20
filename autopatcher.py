import subprocess
import sys
import xml.etree.ElementTree as etree
from subprocess import PIPE as SPIPE

apk_file = "example.apk"

subprocess.run(["apktool", "d", apk_file], stdout=SPIPE, stderr=SPIPE)

# open example/AndroidManifest.xml
manifest_file = etree.parse('example/AndroidManifest.xml')
# Find Application key
for child in manifest_file.getroot():
    if child.tag == "application":
        child.attrib['{http://schemas.android.com/apk/res/android}debuggable'] = 'true'

# Write application manifest back out
manifest_file.write('example/AndroidManifest.xml', encoding="unicode")

subprocess.run(["apktool", "b", "example", "-oexample-debug.apk"], stdout=SPIPE, stderr=SPIPE)


