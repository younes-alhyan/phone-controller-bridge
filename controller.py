import subprocess
import logging
from event_handler import handle_event
from concurrent.futures import ThreadPoolExecutor
from config import controller_device_path, accepted_event_types

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def listen_for_controller_input():
    """Main loop to listen and forward controller input to vJoy."""
    try:
        logging.info("Listening for controller input...")

        process = subprocess.Popen(
            ['adb', 'shell', 'getevent', controller_device_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        with ThreadPoolExecutor(max_workers=4) as pool:
            while True:
                line = process.stdout.readline().strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) != 3:
                    continue

                event_type = int(parts[0], 16)
                event_code = int(parts[1], 16)
                event_value = int(parts[2], 16)

                if event_type not in accepted_event_types:
                    continue

                pool.submit(handle_event, event_code, event_value)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error with subprocess: {e}")
    except OSError as e:
        logging.error(f"OS error: {e}")
    except Exception as e:
        logging.error(f"Listener error: {e}")
        process.terminate()  # Ensure the subprocess is terminated if there's an error
