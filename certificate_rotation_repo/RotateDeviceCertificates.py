#!/usr/bin/env python3

'''
@author: Tabish Naved
Date: 08-Aug-2022

'''
import json

from CreateNewCertificate import CreateNewCertificate
from RevokeOldCertificate import RevokeOldCertificate

thingName = "CameraDevice_D01299"
rootCA = 'certificates_D01299/AmazonRootCA1.pem'
thingCertificate = 'certificates_D01299/D01299-certificate.pem.crt'
privateKey = 'certificates_D01299/D01299-private.pem.key'



# New Certifcate Oject
newCertificate = CreateNewCertificate(thingName, rootCA, thingCertificate, privateKey)
newCertificate.run()

with open('newCert/certificateInfo.json') as f:
	certificateInfo = json.loads(f.read())
	certtificateArn = certificateInfo['certificateArn']

# Revoke Certificate Object
revokeCertificate = RevokeOldCertificate(thingName, rootCA, thingCertificate, privateKey, certtificateArn)
revokeCertificate.run()