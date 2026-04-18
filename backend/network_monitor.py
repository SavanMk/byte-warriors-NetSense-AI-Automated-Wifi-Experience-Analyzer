import subprocess
import platform
import speedtest
import json
import os
from datetime import datetime

# Define where to save the JSON file (saving it in the frontend folder for easy access)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')
JSON_FILE_PATH = os.path.join(FRONTEND_DIR, 'metrics.json')

def run_ping(host="8.8.8.8"):
    """Runs a basic ping test to a reliable public DNS server."""
    print(f"[*] Pinging {host}...")
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        print("--- Ping Results ---\n", output.strip())
        return True
    except subprocess.CalledProcessError as e:
        print("[-] Ping failed:\n", e.output)
        return False

def run_speed_test():
    """Runs a speed test and returns a dictionary of the results."""
    print("[*] Finding best server and running speed test... (This may take a minute)")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        # Convert bps to Mbps and round to 2 decimal places
        download_speed = round(st.download() / 1_000_000, 2)
        upload_speed = round(st.upload() / 1_000_000, 2)
        ping_latency = round(st.results.ping, 2)

        print(f"[*] Speed Test Complete: {download_speed} Down / {upload_speed} Up / {ping_latency}ms Ping")
        
        # Structure the data for our frontend
        return {
            "status": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "download": download_speed,
            "upload": upload_speed,
            "ping": ping_latency
        }
    except Exception as e:
        print(f"[-] Speed test failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def save_to_json(data):
    """Saves the metrics dictionary to a JSON file."""
    # Ensure the frontend directory exists
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[*] Real-time metrics saved to {JSON_FILE_PATH}")

if __name__ == "__main__":
    print("="*40)
    print(" NetSense AI: Generating Real Data")
    print("="*40)
    
    # Run the tests
    run_ping()
    metrics_data = run_speed_test()
    
    # Save the data to JSON if successful
    if metrics_data["status"] == "success":
        save_to_json(metrics_data)
        
    print("========================================")
