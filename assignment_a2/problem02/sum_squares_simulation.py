import threading
import multiprocessing
import time

def calculate_sum(n):
    total = 0

    for number in range(1, n + 1):
        total += number * number

    return total
   

def run_sequential(n):

    print(f"Starting calculate_sum via Sequential Execution...")

    start_time = time.perf_counter()

    for i in range (10):
        calculate_sum(n)
        
    end_time = time.perf_counter()
    
    print(f"Sequential Execution time: {end_time - start_time:.2f} seconds\n")

def run_multithreading(n):

    print("Starting calculate_sum via Multithreading...")

    """
        I wanted to use a loop here, however I'm still learning python so I wasn't quite sure
        how to set it up for this. So I'll get that figured out later and go the long way for now.
    """    
    thread1 = threading.Thread(target=calculate_sum, args=(n,))
    thread2 = threading.Thread(target=calculate_sum, args=(n,))
    thread3 = threading.Thread(target=calculate_sum, args=(n,))
    thread4 = threading.Thread(target=calculate_sum, args=(n,))
    thread5 = threading.Thread(target=calculate_sum, args=(n,))
    thread6 = threading.Thread(target=calculate_sum, args=(n,))
    thread7 = threading.Thread(target=calculate_sum, args=(n,))
    thread8 = threading.Thread(target=calculate_sum, args=(n,))
    thread9 = threading.Thread(target=calculate_sum, args=(n,))
    thread10 = threading.Thread(target=calculate_sum, args=(n,))

    start_time = time.perf_counter()

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()

    end_time = time.perf_counter()
    
    print(f"Multithreading execution time: {end_time - start_time:.2f} seconds\n")


def run_multiprocessing(n):

    print("Starting calculate_sum via Multiprocessing...")
    
    process1 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process2 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process3 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process4 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process5 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process6 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process7 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process8 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process9 = multiprocessing.Process(target=calculate_sum, args=(n,))
    process10 = multiprocessing.Process(target=calculate_sum, args=(n,))
    
    start_time = time.perf_counter()

    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    process6.start()
    process7.start()
    process8.start()
    process9.start()
    process10.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    process6.join()
    process7.join()
    process8.join()
    process9.join()
    process10.join()
    
    end_time = time.perf_counter()
    
    print(f"Multiprocessing execution time: {end_time - start_time:.2f} seconds\n")


if __name__ == "__main__":
    N = 10000000
    print(f"N = {N}\n")
    
    run_sequential(N)
    run_multithreading(N)
    run_multiprocessing(N)
    

    