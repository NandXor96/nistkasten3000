#!/usr/bin/env python3

import os
import time
import sys
import telegram_bot
import motion_api
import config
from helpers import log, cleanup_media_directory

def main():
    # Validate Configuration
    config.validate()
    
    # Welcome MSG
    log(f"{config.BOT_NAME} starting!", "INFO")

    # Delete old files
    cleanup_media_directory()

    # Start Motion Process
    motion_api.start_motion_process()

    # Init Bot
    telegram_bot.init()

    # Start Bot
    telegram_bot.start()

    # Stop Motion Process
    motion_api.stop_motion_process()

def movie_end(file):
    """Create a symlink for the latest video file"""
    symlink_path = os.path.join(config.MEDIA_DIR, "lastvideo.mp4")

    if os.path.islink(symlink_path):
        os.remove(symlink_path)

    # Check if the file is growing
    for i in range(5):
        size = os.path.getsize(file)
        time.sleep(2)
        if os.path.getsize(file) == size:
            break
        elif i == 4:
            return

    os.symlink(file, symlink_path)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 3 and sys.argv[1] == "movie_end":
        movie_end(sys.argv[2])