import argparse
import sys
from typing import Callable


def is_invalid_id(num: int) -> bool:
    num_str = str(num)
    middle = len(num_str) // 2
    return len(num_str) % 2 == 0 and num_str[:middle] == num_str[middle:]


def is_invalid_id_p2(num: int) -> bool:
    num_str = str(num)
    length = len(num_str)

    # check all sample_sizes for repeating
    for sample_size in range(1, length // 2 + 1):
        # skip ranges that don't fit repeating
        if length % sample_size != 0:
            continue

        # repeat sample as often as it fits, then compare with initial id
        repeated_sample = num_str[:sample_size] * (length // sample_size)

        if repeated_sample == num_str:
            return True

    return False


def parse_input(input_data: str) -> list[tuple[int, int]]:
    ranges = []
    for range_str in input_data.split(","):
        start, end = [int(x) for x in range_str.split("-")]
        ranges.append((start, end))
    return ranges


def calculate_solution(
    ranges: list[tuple[int, int]], check_valid_id: Callable[[int], bool]
) -> int:
    solution = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            if check_valid_id(num):
                solution += num
    return solution


def part1(input_data: str) -> None:
    ranges = parse_input(input_data)
    result = calculate_solution(ranges, is_invalid_id)
    print(result)


def part2(input_data: str) -> None:
    ranges = parse_input(input_data)
    result = calculate_solution(ranges, is_invalid_id_p2)
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
