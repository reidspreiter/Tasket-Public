def sort_to_walk(unit_numbers):
    units_by_building = sort_by_building(unit_numbers)
    unit_numbers.clear()

    if (bool(units_by_building[2]["front"]) 
        ^ bool(units_by_building[2]["back"])):
        units_by_building[3]["front"].reverse()

    direction = -1
    for building_number in units_by_building:
        for side, units in units_by_building[building_number].items():

            if not units:
                continue

            if (building_number <= 4 
                    and side == "front" 
                    and units.reverse() != []):
                units_by_building[building_number]["back"].reverse()

            elif building_number > 4:
                if ((building_number % 2 and direction == -1) 
                        or (not building_number % 2 and direction == 1)):
                    units.reverse()
                direction *= -1

            unit_numbers.extend(units)
    return unit_numbers


def sort_by_building(unit_numbers):
    units_by_building = {}
    sides = ["front", "back"]
    ranges = {
        "front" : [
            (), (60, 73), (40, 49), (24, 33), (8, 17), (100, 105), 
            (206, 213), (108, 113), (218, 225), (134, 141), 
            (242, 252), (122, 129), (224, 234)
            ],
        "back" : [
            (), (48, 61), (32, 41), (16, 25), (0, 9), (200, 207), 
            (104, 109), (212, 219), (112, 117), (251, 261), 
            (128, 135), (233, 243), (116, 123)
            ],
    }
    
    for i in range(1, 13):
        units_by_building[i] = {}
        for side in sides:
            units_by_building[i][side] = list(filter(
                lambda x: ranges[side][i][0] < x < ranges[side][i][1],
                unit_numbers
                ))
    return units_by_building