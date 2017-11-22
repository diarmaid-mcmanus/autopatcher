import subprocess
import xml.etree.ElementTree as etree
from subprocess import PIPE as SPIPE

def is_exported(element):
    try:
        if element.get('{http://schemas.android.com/apk/res/android}exported') == 'true':
            return True
    except TypeError:
        return False

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


subprocess.run(apktool_decode, stdout=SPIPE, stderr=SPIPE)

manifest_file = etree.parse('example/AndroidManifest.xml')

for child in manifest_file.getroot():
    if child.tag == "application":
        child.attrib[debuggable_attribute] = 'true'
        for application_child in child.iter():
            if application_child.tag in attack_surface:
                if(is_exported(application_child)):
                    # yup
                    print(etree.tostring(application_child, encoding='unicode'))

# This is where I should do initial static (Manifest) analysis

manifest_file.write('example/AndroidManifest.xml', encoding="unicode")

subprocess.run(apktool_build, stdout=SPIPE, stderr=SPIPE)
# this doesn't align the zip because we're not releasing it.
subprocess.run(jarsigner_sign, stdout=SPIPE, stderr=SPIPE)
