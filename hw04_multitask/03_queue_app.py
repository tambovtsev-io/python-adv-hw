import codecs
import logging
import multiprocessing as mp
import threading
import time
from queue import Empty

STOP_SIGNAL = "quit"

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_a(input_queue, output_queue):
    while True:
        try:
            message = input_queue.get()
            if message == STOP_SIGNAL:
                output_queue.put(STOP_SIGNAL)
                break

            # Convert message to lowercase
            processed_message = message.lower()

            # Wait 5 seconds before sending
            time.sleep(5)
            logger.info(f"Process A sending: {processed_message}")
            output_queue.put(processed_message)

        except Empty:
            continue


def process_b(input_queue, output_queue):
    while True:
        try:
            message = input_queue.get()
            if message == STOP_SIGNAL:
                output_queue.put(STOP_SIGNAL)
                break

            # Apply ROT13 encoding
            encoded_message = codecs.encode(message, "rot_13")
            logger.info(f"Process B encoded (ROT13): {encoded_message}")

            output_queue.put(encoded_message)

        except Empty:
            continue


def input_handler(queue):
    while True:
        try:
            message = input("Enter message (or 'quit' to quit):\n")
            if message.lower() == STOP_SIGNAL:
                queue.put(STOP_SIGNAL)
                break
            logger.info(f"Main process sending: {message}")
            queue.put(message)
        except Empty:
            break


def main():
    # Create queues
    queue_a_in = mp.Queue()
    queue_b_in = mp.Queue()
    queue_main = mp.Queue()

    # Create and start processes
    process_a_instance = mp.Process(target=process_a, args=(queue_a_in, queue_b_in))
    process_b_instance = mp.Process(target=process_b, args=(queue_b_in, queue_main))

    process_a_instance.start()
    process_b_instance.start()

    # Create and start input thread
    input_thread = threading.Thread(target=input_handler, args=(queue_a_in,))
    input_thread.start()

    # Main process receives messages from Process B
    while True:
        try:
            result = queue_main.get()
            if result == STOP_SIGNAL:
                break
            logger.info(f"Main process received: {result}")
        except Empty:
            continue

    # Wait for processes to finish
    input_thread.join()
    process_a_instance.join()
    process_b_instance.join()


if __name__ == "__main__":
    main()
