import os
import config
import glob
import telegram_bot
from typing import Dict
from helpers import log, log_error, del_file

monitor_video_locked = False
send_errors: Dict[str, int] = {}

async def send_media(context):
    """Sends media (video/photo) to the Telegram chat"""
    global monitor_video_locked
    monitor_video_locked = True
    media_type, msg = context.job.data

    media_path = f"{config.MEDIA_DIR}/last{'video' if media_type == 'mp4' else 'snap'}.{media_type}"

    if not os.path.exists(media_path):
        monitor_video_locked = False
        return

    try:
        with open(media_path, "rb") as media:
            if media_type == "mp4":
                await telegram_bot.send_video(media, msg)
            elif media_type == "jpg":
                await telegram_bot.send_photo(media, msg)
        
        # Cleanup
        os.remove(media_path)
        for file in glob.glob(f"{config.MEDIA_DIR}/*.{media_type}"):
            del_file(file)
        
        if media_path in send_errors:
            del send_errors[media_path]
            
    except Exception as e:
        if media_path not in send_errors:
            send_errors[media_path] = 0

        if send_errors[media_path] == 0:
            await telegram_bot.send_msg(config.ERROR_MESSAGE)
        send_errors[media_path] += 1
        log_error(f"Failed to send {media_type}", e)
    finally:
        monitor_video_locked = False

async def monitor_videos(context):
    """Monitors the media directory for new videos/photos"""
    if not monitor_video_locked:
        if os.path.exists(f"{config.MEDIA_DIR}/lastvideo.mp4"):
            context.job_queue.run_once(send_media, 0, data=("mp4", config.VIDEO_MESSAGE))
        if os.path.exists(f"{config.MEDIA_DIR}/lastsnap.jpg"):
            context.job_queue.run_once(send_media, 0, data=("jpg", config.PHOTO_MESSAGE))

