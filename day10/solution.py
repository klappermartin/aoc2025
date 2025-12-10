import argparse
import sys
from collections import deque


def parse_input(input_data: str) -> list[tuple[list[int], list[list[int]]]]:
    result: list[tuple[list[int], list[list[int]]]] = []
    for line in input_data.splitlines():
        split = line.split()

        desired_raw, buttons_raw, _ = split[0], split[1:-1], split[-1]

        desired = [0 if val == "." else 1 for val in list(desired_raw)[1:-1]]
        buttons = []

        for buttons_str in buttons_raw:
            button_result = [0] * len(desired)
            for press in buttons_str[1:-1].split(","):
                button_result[int(press)] = 1

            buttons.append(button_result)

        result.append((desired, buttons))

    return result


def transform_input_to_bin(
    parsed_input: list[tuple[list[int], list[list[int]]]],
) -> list[tuple[int, list[int]]]:
    result: list[tuple[int, list[int]]] = []

    for line in parsed_input:
        target = int("".join([str(x) for x in line[0]]), 2)
        bins: list[int] = []

        for arr in line[1]:
            bin = int("".join([str(x) for x in arr]), 2)
            bins.append(bin)

        result.append((target, bins))

    return result


def find_minimum_presses_to_reach_target(target: int, buttons: list[int]) -> int:
    # start with all turned off and no buttons pressed
    queue = deque([(0, 0)])

    # memo seen light switch positions, so we can skip them
    visited = set()
    visited.add(0)

    while queue:
        state, presses = queue.popleft()

        # press each button (XOR) and queue the result
        for button in buttons:
            new_state = state ^ button

            # done if reached target
            if new_state == target:
                return presses + 1

            # skip seen positions, otherewise queue next light switches states
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))

    return 0


def part1(input_data: str) -> None:
    parsed = parse_input(input_data)
    transformed = transform_input_to_bin(parsed)

    total_presses = 0
    for target, buttons in transformed:
        presses = find_minimum_presses_to_reach_target(target, buttons)
        total_presses += presses

    print(total_presses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        pass
