import requests
import json
import os
osv = int(input(
    "Which computer are you running? (1=Shravan's Mac, 2=PIT Computer, 3=Strategy Laptop): "))


def ovverrideDrive(drivePath, driveNumber):
    try:
        with open(f"{drivePath}NJFLA_Schedule.json", "x") as j:
            j.close()
    except:
        pass

    with open(f"NJFLA_Schedule.json", "r") as file:
        NEW_DATA = list(json.load(file))

    with open(f"{drivePath}NJFLA_Schedule.json", "w") as driveFile:
        json.dump(NEW_DATA, driveFile)


def updateDrives():

    if osv == 1:
        volumes = ([x[0] for x in os.walk("/Volumes")])[1:]
        if "/Volumes/TEAM75-1" in volumes:
            ovverrideDrive("/Volumes/TEAM75-1/", 1)

        if "/Volumes/TEAM75-2" in volumes:
            ovverrideDrive("/Volumes/TEAM75-2/", 2)
    elif osv == 2:
        D_DRIVE = ([x[0] for x in os.walk("D:")])[1:]
        E_DRIVE = ([x[0] for x in os.walk("E:")])[1:]

        if len(D_DRIVE) != 0:
            ovverrideDrive("D:", 0)

        if len(E_DRIVE) != 0:
            ovverrideDrive("E:", 0)

    elif osv == 3:
        E_DRIVE = ([x[0] for x in os.walk("E:")])[1:]
        F_DRIVE = ([x[0] for x in os.walk("F:")])[1:]

        if len(E_DRIVE) != 0:
            ovverrideDrive("E:", 0)

        if len(F_DRIVE) != 0:
            ovverrideDrive("F:", 0)


LOC = input("Event Code: ")
url = f"https://frc-api.firstinspires.org/v3.0/2023/schedule/{LOC}?tournamentLevel=qual"

payload = {}
headers = {
    'Authorization':
    'Basic c2hyYXZhbnA0Nzo4N2Q2YmQ1Yi02MmIzLTQwZDEtYjAwMS05ZTk2YmMzYjczODQ=',
    'If-Modified-Since': ''
}

response = requests.request("GET", url, headers=headers, data=payload)

j = (json.loads(response.text))

event = []

for match in j["Schedule"]:
    for team in match["teams"]:
        alliance_color = team["station"][:-1]
        driverstaton = team["station"][-1]

        added = False
        for i in event:
            if i["Team_Number"] == team["teamNumber"]:
                d = {"Match_Number": match["matchNumber"],
                     "Alliance_Color": alliance_color, "Driver Station": driverstaton}
                i["Matches"].append(d)
                added = True

        if added == False:
            event.append(
                {"Team_Number": team["teamNumber"], "Matches": [{"Match_Number": match["matchNumber"], "Alliance_Color": alliance_color, "Driver Station": driverstaton}]})


with open(f"NJFLA_Schedule.json", "w") as file:
    json.dump(event, file)

updateDrives()
