import json
with open("/Users/shravanp/Strategy2023/data/2023testdata.json", "r+") as file:
    j = json.load(file)


totalPoints = 0
pos1 = 0
pos2 = 0
pos3 = 0
c = 0
for match in j:
    for robot in match:
        i = 1
        for autoGrid in robot["auto_grid"]:
            if i == 1:
                i += 1
                continue
            autoGrid["x.position"] = autoGrid["y.position"]
            autoGrid["y.position"] = autoGrid["Game Piece"]

            autoGrid["Game Piece"] = autoGrid["Success/Fail"]
            autoGrid["Success/Fail"] = "1"

        i = 1
        for autoGrid in robot["teleop_grid"]:
            if i == 1:
                i += 1
                continue
            autoGrid["x.position"] = autoGrid["y.position"]
            autoGrid["y.position"] = autoGrid["Game Piece"]

            autoGrid["Game Piece"] = autoGrid["Success/Fail"]
            autoGrid["Success/Fail"] = "1"

# print(j)
with open("/Users/shravanp/Strategy2023/data/2023testdata.json", "w+") as file:
    j = json.dump(j, file)
