from app.constant import RANGES_MIN_MAX_AGE


def get_ranges_by_min_max_age(min_age: int, max_age: int) -> str:
    ranges_to_include = []
    for range_name, ranges in RANGES_MIN_MAX_AGE.items():
        if (min_age < ranges[0] and max_age < ranges[0]) or (min_age > ranges[1] and max_age > ranges[1]):
            continue
        ranges_to_include.append(range_name)

    return " + ".join(ranges_to_include)


def validate_input(month: int, year: int, min_age: int, max_age: int, min_population: int) -> tuple:
    if not (1 <= month <= 12):
        return False, "Month should be between 1 and 12"
    if year > 2024:
        return False, "You can't give a future year"
    if min_age < 0 or max_age < 0:
        return False, "Ages must be positive numbers"
    if min_age > max_age:
        return False, "Min age must be smaller then max age"
    if min_population < 0:
        return False, "Min population myst be a positive number"

    return True, ""
