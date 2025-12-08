import argparse
import sys
from collections import deque


def parse_input(input_data: str) -> list[list[str]]:
    return [list(line) for line in input_data.splitlines()]


def get_start_pos(rows: list[list[str]]) -> tuple[int, int] | None:
    for row_idx in range(0, len(rows)):
        for col_idx in range(0, len(rows[0])):
            if rows[row_idx][col_idx] == "S":
                return (row_idx + 1, col_idx)

    return None


def get_n_splits(rows: list[list[str]]) -> int:
    result = 0

    checked: set[tuple[int, int]] = set()
    queued: deque[tuple[int, int]] = deque()

    start = get_start_pos(rows)
    if start is None:
        raise ValueError("Start position not found, input invalid")
    queued.append(start)

    while len(queued) > 0:
        check = queued.popleft()

        if check in checked:
            continue

        checked.add(check)

        y, x = check[0], check[1]

        grid_value = rows[y][x]

        new_positions: list[tuple[int, int]] = []

        if grid_value == ".":
            new_positions = [(y + 1, x)]
        elif grid_value == "^":
            new_positions = [(y + 1, x - 1), (y + 1, x + 1)]
            result += 1

        for pos in new_positions:
            if (
                pos[0] < 0
                or pos[0] >= len(rows)
                or pos[1] < 0
                or pos[1] >= len(rows[0])
            ):
                continue

            if pos not in checked:
                queued.append(pos)

    return result


# memoize the amount of paths that "emerge" from a given start position to speed up brute-force
def count_paths_from_position(
    rows: list[list[str]],
    start_row_idx: int,
    start_col_idx: int,
    paths_from_pos: dict[tuple[int, int], int],
) -> int:
    # if steps path from position to end are known, skip re-compute
    if (start_row_idx, start_col_idx) in paths_from_pos:
        return paths_from_pos[(start_row_idx, start_col_idx)]

    current_row = start_row_idx
    current_col = start_col_idx

    # for each row,
    while current_row < len(rows):
        grid_value = rows[current_row][current_col]

        # split into 2 paths, recursive call for each
        # then sum up and memoize paths from here
        if grid_value == "^":
            paths_left = count_paths_from_position(
                rows, current_row + 1, current_col - 1, paths_from_pos
            )
            paths_right = count_paths_from_position(
                rows, current_row + 1, current_col + 1, paths_from_pos
            )

            result = paths_left + paths_right
            paths_from_pos[(start_row_idx, start_col_idx)] = result
            return result

        current_row += 1

    # end of grid -> 1 path
    paths_from_pos[(start_row_idx, start_col_idx)] = 1
    return 1


def part1(input_data: str) -> None:
    grid = parse_input(input_data)
    result = get_n_splits(grid)
    print(result)


def part2(input_data: str) -> None:
    grid = parse_input(input_data)

    start = get_start_pos(grid)
    if start is None:
        raise ValueError("Start position not found, input invalid")

    result = count_paths_from_position(grid, start[0], start[1], {})

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
