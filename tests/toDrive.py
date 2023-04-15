import os
import time
import sys
import json
import PySimpleGUI as sg


osv = int(input(
    "Which computer are you running? (1=Shravan's Mac, 2=PIT Computer, 3=Strategy Laptop): "))
JSON_LOCATION = "2023testdata"

if osv == 1 or osv == 2 or osv == 3:
    pass
else:
    sys.exit("Error getting running computer path")

try:
    with open(f"data/{JSON_LOCATION}.json", "x") as j:
        j.write("[]")
        j.close()
except:
    pass


DRIVE_1_UPDATED = False
DRIVE_2_UPDATED = False


def createWindow(driveNumber):

    pass


def ovverrideDrive(drivePath, driveNumber):
    try:
        with open(f"{drivePath}{JSON_LOCATION}.json", "x") as j:
            j.close()
    except:
        pass

    with open(f"data/{JSON_LOCATION}.json", "r") as file:
        NEW_DATA = list(json.load(file))

    with open(f"{drivePath}{JSON_LOCATION}.json", "w") as driveFile:
        json.dump(NEW_DATA, driveFile)

    createWindow(driveNumber)


while True:
    if osv == 1:
        volumes = ([x[0] for x in os.walk("/Volumes")])[1:]
        if "/Volumes/TEAM75-1" in volumes and DRIVE_1_UPDATED == False:
            DRIVE_1_UPDATED = True
            ovverrideDrive("/Volumes/TEAM75-1/", 1)

        if "/Volumes/TEAM75-2" in volumes and DRIVE_2_UPDATED == False:
            DRIVE_2_UPDATED = True
            ovverrideDrive("/Volumes/TEAM75-2/", 2)

        if "/Volumes/TEAM75-1" not in volumes:
            DRIVE_1_UPDATED = False

        if "/Volumes/TEAM75-2" not in volumes:
            DRIVE_2_UPDATED = False
    elif osv == 2:
        # PIT
        # D: == BLUE, E: YELLOW

        D_DRIVE = ([x[0] for x in os.walk("D:")])[1:]
        E_DRIVE = ([x[0] for x in os.walk("E:")])[1:]

        if len(D_DRIVE) != 0 and DRIVE_2_UPDATED == False:
            DRIVE_2_UPDATED = True
            ovverrideDrive("D:", 2)

        if len(E_DRIVE) != 0 and DRIVE_1_UPDATED == False:
            DRIVE_1_UPDATED = True
            ovverrideDrive("E:", 1)

        if len(D_DRIVE) == 0:
            DRIVE_2_UPDATED = False

        if len(E_DRIVE) == 0:
            DRIVE_1_UPDATED = False

    elif osv == 3:
        # STRAT
        # E: BLUE 2, F: YELLOW 1
        E_DRIVE = ([x[0] for x in os.walk("E:")])[1:]
        F_DRIVE = ([x[0] for x in os.walk("F:")])[1:]

        if len(E_DRIVE) != 0 and DRIVE_2_UPDATED == False:
            DRIVE_2_UPDATED = True
            ovverrideDrive("E:", 2)

        if len(D_DRIVE) != 0 and DRIVE_1_UPDATED == False:
            DRIVE_1_UPDATED = True
            ovverrideDrive("D:", 1)

        if len(E_DRIVE) == 0:
            DRIVE_2_UPDATED = False

        if len(F_DRIVE) == 0:
            DRIVE_1_UPDATED = False

    time.sleep(5)
