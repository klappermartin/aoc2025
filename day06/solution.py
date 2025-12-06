import argparse
import math
import sys


def parse_input(input_data: str) -> tuple[list[tuple[int, ...]], list[str]]:
    lines = input_data.splitlines()

    num_lines = lines[:-1]
    nums = [[int(x.strip()) for x in line.split(" ") if x] for line in num_lines]
    operations = [x.strip() for x in lines[-1].split(" ") if x]

    numbers: list[tuple[int, ...]] = list(zip(*nums))

    return (numbers, operations)


def parse_input_p2(input_data: str) -> tuple[list[tuple[int, ...]], list[str]]:
    lines = input_data.splitlines()
    operations = [x.strip() for x in lines[-1].split(" ") if x]
    num_lines = lines[:-1]

    helper_nums = [[int(x.strip()) for x in line.split(" ") if x] for line in num_lines]

    parsed_matrix = []

    start_idx = 0
    start_idx_ops = 0
    while start_idx_ops < len(operations):
        max_len = 0

        # for each line, get the number at the idx
        for line in helper_nums:
            num = line[start_idx_ops]
            max_len = max(len(str(num)), max_len)

        processed_nums = []

        for line in num_lines:
            candidate = line[start_idx : start_idx + max_len]

            processed = []

            for el in candidate:
                if el == " ":
                    processed.append("")
                else:
                    processed.append(el)

            processed_nums.append(processed)

        start_idx += max_len + 1
        start_idx_ops += 1

        parsed_matrix.append(processed_nums)

    finished = [
        tuple(int("".join(x)) for x in zip(*matrix)) for matrix in parsed_matrix
    ]
    print(finished)

    return (finished, operations)


def get_results(nums: list[tuple[int, ...]], operations: list[str]) -> int:
    result = 0

    for i in range(0, len(operations)):
        numbers = nums[i]
        operation = operations[i]

        if operation == "+":
            result += sum(numbers)
        elif operation == "*":
            result += math.prod(numbers)

    return result


def prepare_p2(nums: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    combinations: list[tuple[int, ...]] = []

    for maths in nums:
        transformed: list[str] = []
        max_length = 0

        for num in maths:
            max_length = max(len(str(num)), max_length)

        for num in maths:
            transformed_num = str(num) + "0" * (max_length - len(str(num)))
            transformed.append(transformed_num)

        mega_mind = tuple(int("".join(position)) for position in zip(*transformed))

        combinations.append(tuple(mega_mind))

    return combinations


def part1(input_data: str) -> None:
    nums, operations = parse_input(input_data)
    result = get_results(nums, operations)
    print(result)


def part2(input_data: str) -> None:
    nums, operations = parse_input_p2(input_data)
    result = get_results(nums, operations)
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
