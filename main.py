import sys
import signal
import logging
from controller import listen_for_controller_input

def shutdown_gracefully(signal_num=None, frame=None):
    """Handle shutdown gracefully."""
    logging.info("Shutdown initiated...")
    logging.shutdown()  # Ensure all logs are written before exiting
    sys.exit(0)

# ========================
# Run Script
# ========================
if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, shutdown_gracefully)
    signal.signal(signal.SIGTERM, shutdown_gracefully)

    try:
        listen_for_controller_input()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
