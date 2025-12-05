import argparse
import sys


def parse_input(input_data: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges: list[tuple[int, int]] = []
    ids: list[int] = []

    parse_ranges = True
    for line in input_data.splitlines():
        if line == "":
            parse_ranges = False
            continue

        if parse_ranges:
            start, end = [int(x) for x in line.split("-")]
            ranges.append((start, end))
        else:
            ids.append(int(line))

    return (ranges, ids)


def find_fresh_ingredients_in_ranges(
    ranges: list[tuple[int, int]], ids: list[int]
) -> int:
    fresh_count = 0

    for id in ids:
        for low, high in ranges:
            if id >= low and id <= high:
                fresh_count += 1
                break

    return fresh_count


def solve_part2(ranges: list[tuple[int, int]]) -> int:
    sorted_ranges = sorted(ranges, key=lambda r: r[0])

    if len(sorted_ranges) == 0:
        return 0

    result = 0
    res_ranges = []

    prev_low, prev_high = sorted_ranges[0][0], sorted_ranges[0][1]
    for i in range(1, len(sorted_ranges)):
        low, high = sorted_ranges[i][0], sorted_ranges[i][1]

        # completely ignore sub-intervals
        if low >= prev_low and high <= prev_high:
            continue

        if low <= prev_high:
            # if overlapping, adjust prev range
            prev_high = max(prev_high, high)
        else:
            # otherwise, append and move to next
            res_ranges.append((prev_low, prev_high))

            prev_low = low
            prev_high = high

    res_ranges.append((prev_low, prev_high))

    for low, high in res_ranges:
        result += high - low + 1

    return result


def part1(input_data: str) -> None:
    ranges, ids = parse_input(input_data)
    result = find_fresh_ingredients_in_ranges(ranges, ids)
    print(result)


def part2(input_data: str) -> None:
    ranges, _ = parse_input(input_data)
    result = solve_part2(ranges)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        part2(input_data)
