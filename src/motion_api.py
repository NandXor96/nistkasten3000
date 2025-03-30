import requests
import config
import subprocess
import time
from helpers import log, log_error

webinterface_session = requests.Session()

def make_request(api: str, method: str = "GET") -> requests.Response:
    """Does a request to the web interface"""
    url = f"{config.WEB_URL}{api}"
    try:
        with webinterface_session.request(method, url) as response:
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            return response
    except Exception as e:
        log_error(f"Webinterface request error", e)

async def create_snapshot():
    action = f"/0/action/snapshot"
    make_request(action)

async def start_video_recording(context=None):
    log("Start recording")
    action = f"/0/action/eventstart"
    make_request(action)

async def stop_video_recording(context=None):
    log("End recording")
    action = f"/0/action/eventend"
    make_request(action) 

async def activate_motion_detection():
    action = f"/0/detection/start"
    make_request(action)

async def deactivate_motion_detection():
    action = f"/0/detection/pause"
    make_request(action)

async def status_motion_detection():
    action = f"/0/detection/status"
    response = make_request(action)
    return True if "ACTIVE" in response.text else False

def start_motion_process() -> bool:
    """Starts the Motion application"""
    try:
        if subprocess.run("pgrep -x motion", shell=True, executable='/bin/bash').returncode == 0:
            subprocess.run("pkill -9 motion", shell=True, executable='/bin/bash')
            time.sleep(2)
        subprocess.run("motion", shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)
        log("Motion-Process started")
    except Exception as e:
        log_error("Error starting the Motion application", e)

def stop_motion_process() -> bool:
    """Stops the Motion application"""
    try:
        subprocess.run("pkill -9 motion", shell=True, executable='/bin/bash')
    except Exception as e:
        log_error("Error stopping the Motion application", e)