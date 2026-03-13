import random
import time


def slow_random_sum(n):
    data = []
    for _ in range(n):
        data.append(random.randint(1, 100))

    total = 0
    for x in data:
        total += x * x

    return total


def main():
    print("Starting workload...")

    # Run several times so py-spy has time to sample
    for i in range(100):
        result = slow_random_sum(2_000_000)
        print(f"Iteration {i + 1}, result={result}")
        time.sleep(1)

    print("Finished.")


if __name__ == "__main__":
    main()