'''
laboratory_threading.py
Assignment 3.2: Hospital Laboratory Test Processing System

Author: Jessi Lewis
Course: CPSI 48703-9S1 - Distributed Computing
Date: 22-OCT-2026

Description:
    Simulates a hospital laboratory using the Producer-Consumer
    strategy. Python threads emulate MPI ranks that communicate
    only by passing tagged messages through per-rank mailboxes.

    Rank 0          Coordinator: Owns the bounded sample buffer
                    (capacity 5), tracks submitted and completed
                    samples, and sends termination messages.
    Producer ranks  Hospital departments that submit samples.
    Consumer ranks  Lab technicians that request, test, and
                    complete samples.

How to run:
    python laboratory_threading.py

Configuration:
    Change NUM_PRODUCERS and NUM_CONSUMERS below to test
    different thread counts.
'''

import queue              # Provides the Queue class
import threading          # Used for multithreading
import time               # Used for delay
import random             # Used for generating random numbers


# ----------------------------------------------------------------
# Set up
# ----------------------------------------------------------------

NUM_PRODUCERS = 4
NUM_CONSUMERS = 4
BUFFER_CAPACITY = 5
TOTAL_RANKS = 1 + NUM_PRODUCERS + NUM_CONSUMERS 

# Tag Numbers
SUBMIT = 0
ACK = 1
FULL = 2
REQUEST = 3
WORK = 4
EMPTY = 5
COMPLETE = 6
TERMINATE = 7

DEPARTMENTS = ["Emergency", "General Ward", "ICU", "Outpatient"]

SAMPLE = [
    {  
        "sample_id": 101,
        "patient_name": "Bob Thebuilder",
        "department": "",
        "test_type": "Blood Test",
        "priority": "High", 
    },

    {
        "sample_id": 102,
        "patient_name": "Alice Johnson",
        "department": "",
        "test_type": "Urine Test",
        "priority": "Medium", 
    },

    {
        "sample_id": 103,
        "patient_name": "Charlie Brown",
        "department": "",
        "test_type": "Urinalysis",
        "priority": "High", 
    },    
    
    {
        "sample_id": 104,
        "patient_name": "David Davis",
        "department": "",
        "test_type": "Blood Test",
        "priority": "Medium", 
    },    
    
    {
        "sample_id": 105,
        "patient_name": "Diana Prince",
        "department": "",
        "test_type": "CBC",
        "priority": "Low", 
    },    
    
    {
        "sample_id": 106,
        "patient_name": "Eve Wilson",
        "department": "",
        "test_type": "Metabolic Panel",
        "priority": "High", 
    },    
    
    {
        "sample_id": 107,
        "patient_name": "Frank Miller",
        "department": "",
        "test_type": "Urine Test",
        "priority": "Medium", 
    },    
    
    {
        "sample_id": 108,
        "patient_name": "Grace Lee",
        "department": "",
        "test_type": "Urinalysis",
        "priority": "High", 
    },

    {
        "sample_id": 109,
        "patient_name": "Henry Davis",
        "department": "",
        "test_type": "CBC",
        "priority": "Low", 
    },  
    
    {
        "sample_id": 110,
        "patient_name": "Ivy Chen",
        "department": "",
        "test_type": "Metabolic Panel",
        "priority": "High", 
    },

    {
        "sample_id": 111,
        "patient_name": "Jack Wilson",
        "department": "",
        "test_type": "Blood Test",
        "priority": "Medium", 
    },

    {
        "sample_id": 112,
        "patient_name": "Kate Brown",
        "department": "",
        "test_type": "Urinalysis",
        "priority": "High", 
    },

    {
        "sample_id": 113,
        "patient_name": "Liam Davis",
        "department": "",
        "test_type": "CBC",
        "priority": "Low", 
    },

    {
        "sample_id": 114,
        "patient_name": "Mia Johnson",
        "department": "",
        "test_type": "Blood Test",
        "priority": "Medium", 
    },
     
    {
        "sample_id": 115,
        "patient_name": "Noah Wilson",
        "department": "",
        "test_type": "Urinalysis",
        "priority": "High", 
    }
]

mailboxes = []

for rank in range(TOTAL_RANKS):
    mailboxes.append(queue.Queue()) 

# ----------------------------------------------------------------
# Message Helper Functions
# ----------------------------------------------------------------

def send_message(source_rank, dest_rank, tag, data):
    message = {
        "source": source_rank,  
        "tag": tag,
        "data": data
    }
    mailboxes[dest_rank].put(message)

def receive_message(rank):
    message = mailboxes[rank].get()
    return message

# ----------------------------------------------------------------
# Producer Function (one department)
# ----------------------------------------------------------------

def producer(rank, department, my_samples):
    for sample in my_samples:
        while True:
            send_message(rank, 0, SUBMIT, sample)
            message = receive_message(rank)

            if message["tag"] == ACK:
                print(f"{department} submitted Sample {sample['sample_id']}\nTest: {sample['test_type']}\nQueue size: {message['data']}")
                break
            elif message["tag"] == FULL:
                print(f"{department}: queue full, waiting to resubmit {sample['sample_id']}")
                time.sleep(random.uniform(0.1, 0.5))        # Randomized waiting time before trying to submit same sample again

        time.sleep(random.uniform(0.1, 0.5))                # Randomized waiting time before submissions

    print(f"{department} finished submitting")



# ----------------------------------------------------------------
# Consumer Function (one lab technician)
# ----------------------------------------------------------------
def consumer(rank):
    while True:
        send_message(rank, 0, REQUEST, None)
        message = receive_message(rank)

        if message["tag"] == WORK:
            sample = message['data']
            print(f"Tech {rank - NUM_PRODUCERS} testing Sample {sample['sample_id']}")
            time.sleep(random.uniform(0.5, 1.0))        # Randomized waiting time for test to complete
            print(f"Tech {rank - NUM_PRODUCERS} finished Sample {sample['sample_id']}")
            send_message(rank, 0, COMPLETE, sample['sample_id'])
        elif message["tag"] == EMPTY:
            time.sleep(random.uniform(0.1, 0.5))
        elif message["tag"] == TERMINATE:
            print(f"Tech {rank - NUM_PRODUCERS} going home")
            break

# ----------------------------------------------------------------
# Coordinator Function (rank 0, the front desk)
# ----------------------------------------------------------------
def coordinator(total_samples):
    shelf = []
    submitted = 0
    completed = 0
    terminated = 0
    full_waits = 0
    empty_waits = 0

    while terminated < NUM_CONSUMERS:
        message = receive_message(0)
        source = message['source']

        if message["tag"] == SUBMIT:
            if len(shelf) < BUFFER_CAPACITY:
                shelf.append(message['data'])
                submitted += 1
                send_message(0, source, ACK, len(shelf))
            else:
                send_message(0, source, FULL, None)
                full_waits += 1
        elif message["tag"] == REQUEST:
            if completed == total_samples:
                send_message(0, source, TERMINATE, None)
                terminated += 1
            elif len(shelf) > 0:
                sample = shelf.pop(0)
                send_message(0, source, WORK, sample)
            else:
                send_message(0, source, EMPTY, None)
                empty_waits += 1
        elif message["tag"] == COMPLETE:
            completed += 1

    print(f"Submitted: {submitted}, Completed: {completed}")
    print(f"Department waits: {full_waits}, Technician waits: {empty_waits}")

# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
def main():
    
    threads = []

    # ----- Split up the samples ----- 
    producer_samples = []
    for _ in range(NUM_PRODUCERS):
        producer_samples.append([])

    for i in range(len(SAMPLE)):
        p = i % NUM_PRODUCERS           # p is the producer index (0-based)
        SAMPLE[i]['department'] = DEPARTMENTS[p]
        producer_samples[p].append(SAMPLE[i])

    # ----- Create Threads -----
    threads.append(threading.Thread(target=coordinator, args=(len(SAMPLE),)))

    for p in range(NUM_PRODUCERS):
        threads.append(threading.Thread(target=producer, args=(p + 1, DEPARTMENTS[p], producer_samples[p])))

    for c in range(NUM_PRODUCERS + 1, TOTAL_RANKS):
        threads.append(threading.Thread(target=consumer, args=(c,)))

    start_time = time.perf_counter()

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter()

    print(f"Producers: {NUM_PRODUCERS}")
    print(f"Consumers: {NUM_CONSUMERS}")
    print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")

if __name__ == "__main__":
    main()