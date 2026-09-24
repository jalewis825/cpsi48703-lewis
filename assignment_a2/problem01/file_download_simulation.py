import threading
import multiprocessing
import time

def worker_function(file_num):
    """
        Simulates downloading a single file.
        Uses time.sleep(2) to mimic the time it takes for the file to download.
        Used provided example code.
    """
    print(f"Started download of {file_num}")
    time.sleep(2)

    print(f"Finished downloading of {file_num}")

def run_sequential():
    """
        Downloads the files sequentially in a single thread.
        Each file download must be fully complete before moving on to the next.
    """
    print("Starting download of files via Sequential Execution...")

    start_time = time.perf_counter()

    for i in range (1, 6):
        file_label = f"File {i}"
        worker_function(f"{file_label}")
    
    print("All files downloaded.")
    
    end_time = time.perf_counter()
    
    print(f"Sequential Execution file download execution time: {end_time - start_time:.2f} seconds\n")


def run_multithreading():
    """
        Downloads the files concurrently using multiple threads within the same process.
        Threads can overlap during sleep time.
        Used example code provided.
    """
    print("Starting download of files via Multithreading...")
    
    thread1 = threading.Thread(target=worker_function, args=("File 1",))
    thread2 = threading.Thread(target=worker_function, args=("File 2",))
    thread3 = threading.Thread(target=worker_function, args=("File 3",))
    thread4 = threading.Thread(target=worker_function, args=("File 4",))
    thread5 = threading.Thread(target=worker_function, args=("File 5",))
    
    start_time = time.perf_counter()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    
    print("All files downloaded.")
    
    end_time = time.perf_counter()
    
    print(f"Multithreading file download execution time: {end_time - start_time:.2f} seconds\n")


def run_multiprocessing():
    """
        Downloads the files concurrently across 5 separate processes.
        Each process has its own isolated memory space.
        Used example code provided.
    """

    print("Starting download of files via Multiprocessing...")
    
    process1 = multiprocessing.Process(target=worker_function, args=("File 1",))
    process2 = multiprocessing.Process(target=worker_function, args=("File 2",))
    process3 = multiprocessing.Process(target=worker_function, args=("File 3",))
    process4 = multiprocessing.Process(target=worker_function, args=("File 4",))
    process5 = multiprocessing.Process(target=worker_function, args=("File 5",))
    
    start_time = time.perf_counter()
    process1.start()
    process2.start()
    process3.start()
    process4.start()
    process5.start()
    
    process1.join()
    process2.join()
    process3.join()
    process4.join()
    process5.join()
    
    print("All files downloaded.")
    
    end_time = time.perf_counter()
    
    print(f"Multiprocessing file download execution time: {end_time - start_time:.2f} seconds\n")
    
if __name__ == "__main__":
    run_sequential()
    run_multithreading()
    run_multiprocessing()
    

    