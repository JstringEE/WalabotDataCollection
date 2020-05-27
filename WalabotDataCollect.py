from __future__ import print_function
from sys import platform
from os import system
import csv
import WalabotAPI as wlbt

xArenaMin, xArenaMax, xArenaRes = -3, 4, 0.5
yArenaMin, yArenaMax, yArenaRes = -6, 4, 0.5
zArenaMin, zArenaMax, zArenaRes = 1, 8, 0.1
thresh = 0
q = 0
sc = "N"
fileit = 1

wlbt.Init()  # load the WalabotSDK to the Python wrapper
wlbt.Initialize()  # set the path to the essetial database files
wlbt.ConnectAny()  # establishes communication with the Walabot

wlbt.SetProfile(wlbt.PROF_SHORT_RANGE_IMAGING)  # set scan profile out of the possibilities
wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)  # specify filter to use
wlbt.SetThreshold(thresh)
wlbt.SetAdvancedParameter(wlbt.PARAM_DIELECTRIC_CONSTANT,4)

wlbt.SetArenaX(xArenaMin, xArenaMax, xArenaRes) #Set Arena Size
wlbt.SetArenaY(yArenaMin, yArenaMax, yArenaRes)
wlbt.SetArenaZ(zArenaMin, zArenaMax, zArenaRes)

cali = 'N'
print("Please enter C to calibrate")
cali = input()


wlbt.Start()  # starts Walabot in preparation for scanning
wlbt.StartCalibration() #Walabot Calibration
while wlbt.GetStatus()[0] == wlbt.STATUS_CALIBRATING:
 	wlbt.Trigger()
while sc == "N":
 	print("Please enter S to start a scan")
 	sc = input()
 	if sc == "S":
 		#print(wlbt.GetAdvancedParameter(wlbt.PARAM_DIELECTRIC_CONSTANT))
 		q = 1
while (q == 1):
	appStatus, calibrationProcess = wlbt.GetStatus()
	wlbt.Trigger()  # initiates a scan and records signals
	listpairs = wlbt.GetAntennaPairs()
	q = len(listpairs)

	f1 = open("AntennaPairs.txt","w+")
	for i in listpairs:
		f1.write(str(i) + "\n")
	f1.close()

	# f2 = open("AntennaLocations.txt", "w+")
	# for i in range(1,19):
	# 	location = wlbt.GetAntennaLocation(i)
	# 	f2.write(str(location))
	# f2.close()
	SigAmpFileName = 'SignalAmplitudeList{0}.txt'	
	f3 = open(SigAmpFileName.format(fileit),"w+")
	f4 = open("TimeAxisList.txt","w+")
	for i in listpairs:
		ampList,timeaxis = wlbt.GetSignal(i)
		for i in ampList:
			f3.write(str(i) + "\n")
		# with open("amps.csv",'w') as resultFile:
		# 	wr = csv.writer(resultFile)
		# 	wr.writerow(ampList)
		f3.write('Next' + "\n")
	f3.close()	
	for i in timeaxis:
		f4.write(str(i) + "\n")
	f4.close()
	#ampList, timeList = wlbt.GetSignal(listpairs[i])
	q = 0
	sc = "N"
	print("Scan Complete")
	while sc == "N":
 		print("Please enter S to start a new scan, or enter any other letter to stop scanning")
 		fileit += 1
 		sc = input()
 		if sc == "S":
 			q = 1
wlbt.Stop()  # stops Walabot when finished scanning
wlbt.Disconnect()  # stops communication with Walabot