import argparse
import sys
from functools import cache


def parse_input(input_data: str) -> dict[str, list[str]]:
    graph = {}
    for line in input_data.strip().splitlines():
        parts = line.split()
        name, children = parts[0][:-1], parts[1:]
        graph[name] = children
    return graph


# FIXME: A bit pointless to have the find with and without required vists be the same function
# just makes it harder to read
def count_paths_from_start_to_target(
    graph: dict[str, list[str]],
    start: str,
    target: str,
    required: set[str] | None = None,
) -> int:
    required = required or set()
    required_frozen: frozenset[str] = frozenset(required)

    @cache
    # recursively find valid path to target node (that traverse the required nodes if passed)
    def count_from_start_to_target(current: str, seen_required: frozenset[str]) -> int:
        if current == target:
            # valid path if required not passed and thereby sets empty
            # or all required nodes have been seen
            if not required_frozen or seen_required == required_frozen:
                return 1
            else:
                return 0

        # if this is a required node, mark it as seen
        new_seen = seen_required
        if current in required:
            new_seen = seen_required | {current}

        # for all children, get paths to target
        total = 0
        for child in graph[current]:
            total += count_from_start_to_target(child, new_seen)

        return total

    return count_from_start_to_target(start, frozenset())


def part1(input_data: str) -> None:
    graph = parse_input(input_data)
    n_paths_to_target = count_paths_from_start_to_target(graph, "you", "out")
    print(n_paths_to_target)


def part2(input_data: str) -> None:
    graph = parse_input(input_data)
    n_paths_to_target = count_paths_from_start_to_target(
        graph, start="svr", target="out", required={"dac", "fft"}
    )
    print(n_paths_to_target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        part2(input_data)
