from multiprocessing import Pool

def compute(x):
    return x * x

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(compute, range(10))
    print(results)

###############################


import multiprocessing
import time

def worker_function(number):
    """Function to square a number."""
    time.sleep(1)  # Simulate some work
    return number ** 2

def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Use multiprocessing.Pool for parallel processing
    with multiprocessing.Pool(processes=4) as pool:  # Adjust the number of processes as needed
        # Map the worker function to the list of numbers
        results = pool.map(worker_function, numbers)

    print("Input Numbers:", numbers)
    print("Squared Results:", results)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Execution time: {time.time() - start_time:.2f} seconds")
