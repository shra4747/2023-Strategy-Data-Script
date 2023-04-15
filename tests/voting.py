from collections import Counter



GLOBAL_MATCH_NUMBER = 0

# 10;1923;Blue;Left;5;4.2.cone.1?5.2.cube.1?;1;0;0;0;1;1;1;1;1;1;6.2.cone.1?1.3.cube.1?2.3.cube.1?3.3.cube.1?4.3.cube.1?5.3.cube.1?;20;0;0;0;0;0;0;1;0010;4;Feeder;;0?

buffer = [{"Match_Number": 2}, {"Match_Number": 2}, {
    "Match_Number": 2}, {"Match_Number": 1}, {"Match_Number": 1}, {"Match_Number": 1}]

def votingSystem(match_dicts):
    global buffer

    matches = []

    for match in match_dicts:
        matches.append(match["Match_Number"])

    matches.append(GLOBAL_MATCH_NUMBER)

    matches = Counter((matches))
    keys = list(matches.keys())
    values = list(matches.values())

    if ((dict(Counter(values)))[max(values)]) > 1:
        winner = int(input("Manual Needed, Match Number?: "))
    else:
        winner = (keys[values.index(max(values))])

    for bufferMatch in buffer:
        bufferMatch["Match_Number"] = int(winner)

    GLOBAL_MATCH_NUMBER == buffer[0]["Match_Number"]


votingSystem(buffer)
print(buffer)
