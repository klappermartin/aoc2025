import argparse
import sys


def parse_input(input_data: str) -> list[tuple[int, int]]:
    tile_positions: list[tuple[int, int]] = []

    for line in input_data.splitlines():
        x, y = [int(x) for x in line.split(",")]

        tile_positions.append((x, y))

    return tile_positions


def find_largest_area_rectangle(positions: list[tuple[int, int]]) -> int:
    result = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            result = max(result, area)

    return result


def part1(input_data: str) -> None:
    red_tile_positions = parse_input(input_data)
    result = find_largest_area_rectangle(red_tile_positions)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        pass
