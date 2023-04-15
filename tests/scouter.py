import json
from datetime import datetime
import os
from collections import Counter

osv = int(input(
    "Which computer are you running? (1=Shravan's Mac, 2=PIT Computer): "))
JSON_LOCATION = "2023testdata"
EVENT_CODE = input(
    "Event Code (https://frc-events.firstinspires.org/team/75): ")
YEAR = str(datetime.now())[0:4]
GLOBAL_MATCH_NUMBER = int(input("Starting Match Number: "))
GLOBAL_ROBOT_NUMBER = 1
try:
    with open(f"data/{JSON_LOCATION}.json", "x") as j:
        j.write("[]")
        j.close()
except:
    pass


def toJSON(gameString):
    headers = []

    d = str(datetime.now())
    year = d[0:4]
    month = d[5:7]
    day = d[8:10]

    DATE = f"{month}/{day}/{year}"

    gameDict = {"event_code": EVENT_CODE, "datetime": DATE, "year": YEAR}

    with open(f"data/2023headers.txt", "r+") as headerFile:
        for line in range(int(headerFile.readline())):
            headers.append(str(((headerFile.readline()))).strip())

    for index, value in enumerate(gameString.split(";")):
        try:
            if str(headers[index]) == "auto_grid":
                value = value.replace(",", ".")
                entries = (value.split("?. "))
                eList = []
                for i in entries:
                    entry = i.split(".")
                    e = {"x.position": entry[0], 'y.position': entry[1],
                         'Game Piece': entry[2], 'Success/Fail': entry[3].replace("?", "")}
                    eList.append(e)
                d = {headers[index]: eList}
                gameDict.update(d)
            elif str(headers[index]) == "teleop_grid":
                value = value.replace(",", ".")
                entries = (value.split("?. "))
                eList = []
                for i in entries:
                    entry = i.split(".")
                    e = {"x.position": entry[0], 'y.position': entry[1],
                         'Game Piece': entry[2], 'Success/Fail': entry[3].replace("?", "")}
                    eList.append(e)
                d = {headers[index]: eList}
                gameDict.update(d)
            else:
                value = value.replace("?", "")
                if str(headers[index]) != "additional":
                    value = value.replace(" ", "")
                elif value == "":
                    value = "0"
                value = value.replace(",", "-")
                d = {headers[index]: str(value)}
                gameDict.update(d)
        except:
            with open("data/errorlog.txt", "a") as errorlog:
                errorlog.write(f"\n{gameString}")
            return

    team = gameDict["Team_Number"]
    match = gameDict["Match_Number"]
    key = f"{team}-{match}|{EVENT_CODE}"
    gameDict.update({"key": key})

    return (gameDict)


def saveJSON(MATCH_NUMBER, TEAM_DATA):
    with open(f"data/{JSON_LOCATION}.json", "r+") as file:
        try:
            listObj = list(json.load(file))

        except:
            listObj = []

    added = False

    for game in listObj:
        if game[0]["Match_Number"] == MATCH_NUMBER:
            game.append(TEAM_DATA)
            added = True

    if added == False:
        listObj.append([TEAM_DATA])

    with open(f"data/{JSON_LOCATION}.json", "w+") as file:
        json.dump(listObj, file, indent=4, separators=(',', ': '))


def updateDrive(drivePath, driveNumber):
    try:
        with open(f"{drivePath}{JSON_LOCATION}.json", "x") as j:
            j.close()
    except:
        pass

    with open(f"data/{JSON_LOCATION}.json", "r") as file:
        NEW_DATA = list(json.load(file))

    with open(f"{drivePath}{JSON_LOCATION}.json", "w") as driveFile:
        json.dump(NEW_DATA, driveFile)


def updateDrives():
    if osv == 1:
        volumes = ([x[0] for x in os.walk("/Volumes")])[1:]
        if "/Volumes/TEAM75-1" in volumes:
            updateDrive("/Volumes/TEAM75-1/", 1)
    elif osv == 2:
        D_DRIVE = ([x[0] for x in os.walk("D:")])[1:]
        E_DRIVE = ([x[0] for x in os.walk("E:")])[1:]

        if len(D_DRIVE) != 0:
            updateDrive("D:", 0)

        if len(E_DRIVE) != 0:
            updateDrive("E:", 0)


BUFFER = []

def votingSystem(match_dicts):
    global BUFFER
    global GLOBAL_MATCH_NUMBER

    matches = []

    for match in match_dicts:
        try:
            matches.append(int(match["Match_Number"]))
        except:
            pass

    matches.append(int(GLOBAL_MATCH_NUMBER))

    matches = Counter((matches))
    keys = list(matches.keys())
    values = list(matches.values())

    if ((dict(Counter(values)))[max(values)]) > 1:
        winner = int(input("Manual Needed, Match Number?: "))
    else:
        winner = (keys[values.index(max(values))])

    for bufferMatch in BUFFER:
        try:
            bufferMatch["Match_Number"] = f"{winner}"
        except:
            continue

    try:
        GLOBAL_MATCH_NUMBER = int(BUFFER[0]["Match_Number"])
    except:
        GLOBAL_MATCH_NUMBER = int(f"{winner}")


def bufferMatches(TEAM_DATA):
    global BUFFER
    global GLOBAL_MATCH_NUMBER
    global GLOBAL_ROBOT_NUMBER
    BUFFER.append(TEAM_DATA)

    if len(BUFFER) == 6:
        votingSystem(BUFFER)

        print(
            f"\nFINAL MATCH NUMBER: {GLOBAL_MATCH_NUMBER} #####################")
        saveQ = input(
            "Save the Data? Last confirmation: (enter something to CANCEL) ")

        if saveQ == "":

            for robot in BUFFER:
                try:
                    saveJSON(robot["Match_Number"], robot)
                except:
                    continue
            updateDrives()
            BUFFER = []
            GLOBAL_MATCH_NUMBER += 1
            print("\nDATA SAVED ****************************\n")
        else:
            BUFFER = []
            print(f"Match Number {GLOBAL_MATCH_NUMBER} RESET. Input Again")
        GLOBAL_ROBOT_NUMBER = 1
    else:
        GLOBAL_ROBOT_NUMBER += 1

while True:
    qrString = input(f"{GLOBAL_ROBOT_NUMBER}: QR String ---- ")
    while len(qrString.split(";")) != 31:
        qrString += input("")

    try:
        with open("data/runninglog.txt", "x") as runninglog:
            runninglog.write(f"\n{qrString}")
    except:
        with open("data/runninglog.txt", "a") as runninglog:
            runninglog.write(f"\n{qrString}")

    bufferMatches(toJSON(qrString))
    qrString = ""
    print()