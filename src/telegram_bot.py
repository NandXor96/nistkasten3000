from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Application, ContextTypes, CallbackContext, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest
import config
import media
from helpers import log
import motion_api

__bot_request = HTTPXRequest(connection_pool_size=10)
__bot = Bot(token=config.BOT_TOKEN, request=__bot_request)
__application = Application.builder().token(config.BOT_TOKEN).read_timeout(config.CHAT_TIMEOUT).write_timeout(config.CHAT_TIMEOUT).build()

def init():
    """Initializes the Telegram Bot"""
    __application.add_handler(CommandHandler("start", __handle_start))
    __application.add_handler(MessageHandler(filters.Text("📹 Video"), __handle_video))
    __application.add_handler(MessageHandler(filters.Text("📸 Photo"), __handle_snapshot))
    __application.add_handler(MessageHandler(filters.Text("▶️ Motion Detection"), __handle_activate_motion_detection))
    __application.add_handler(MessageHandler(filters.Text("🛑 Motion Detection"), __handle_deactivate_motion_detection))
    __application.add_handler(MessageHandler(filters.Text("🔍 Status"), __handle_status_motion_detection)) 

    # Add monitor_videos as a repeating job to the job queue
    __application.job_queue.run_repeating(media.monitor_videos, interval=5, first=0)
    log("Telegram Bot initialized", "INFO")

def start():
    """Start the Telegram Bot"""
    __application.run_polling()

async def send_video(video, msg):
    await __bot.send_video(chat_id=config.CHAT_ID, video=video, caption=msg, read_timeout=config.CHAT_TIMEOUT, write_timeout=config.CHAT_TIMEOUT)
    log(f"Video sent: {video.name}")

async def send_photo(photo, msg):
    await __bot.send_photo(chat_id=config.CHAT_ID, photo=photo, caption=msg, read_timeout=config.CHAT_TIMEOUT, write_timeout=config.CHAT_TIMEOUT)
    log(f"Photo sent: {photo.name}")

async def send_msg(msg):
    await __bot.send_message(chat_id=config.CHAT_ID, text=msg)
    log(f"Message sent: {msg}")

def __chat_filter(update: Update):
    """Returns True if the update is not from the configured chat"""
    return update.effective_chat.id != int(config.CHAT_ID)

async def __handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    if __chat_filter(update):
        return

    await context.bot.send_message(text=f"{config.BOT_NAME}!", chat_id=config.CHAT_ID, reply_markup=ReplyKeyboardMarkup([
        ["📹 Video"],
        ["📸 Photo"],
        ["▶️ Motion Detection"],
        ["🛑 Motion Detection"],
        ["🔍 Status"]
    ], resize_keyboard=True, one_time_keyboard=False)) 

async def __handle_video(update: Update, context: CallbackContext):
    """Handler for video command"""
    if __chat_filter(update):
        return
        
    log("Video requested")
    
    context.job_queue.run_once(motion_api.start_video_recording, 0)
    context.job_queue.run_once(motion_api.stop_video_recording, config.VIDEO_DURATION)
    await send_msg("Videoaufnahme gestartet.")

async def __handle_snapshot(update: Update, context: CallbackContext):
    """Handler for snapshot command"""
    if __chat_filter(update):
        return
    log("Snapshot requested")
    await motion_api.create_snapshot()

async def __handle_activate_motion_detection(update: Update, context: CallbackContext):
    """Handler for activating motion detection"""
    if __chat_filter(update):
        return
    log("Motion detection start requested")
    await motion_api.activate_motion_detection()
    await send_msg(config.MOTION_DETECTION_IS + " " + config.ACTIVATED)

async def __handle_deactivate_motion_detection(update: Update, context: CallbackContext):
    """Handler for deactivating motion detection"""
    if __chat_filter(update):
        return
    log("Motion detection stop requested")
    await motion_api.deactivate_motion_detection()
    await send_msg(config.MOTION_DETECTION_IS + " " + config.DEACTIVATED)

async def __handle_status_motion_detection(update: Update, context: CallbackContext):
    """Handler for motion detection status"""
    if __chat_filter(update):
        return
    log("Motion detection status requested")
    status = await motion_api.status_motion_detection()
    await send_msg(f"{config.MOTION_DETECTION_IS} " + (config.ACTIVATED if status else config.DEACTIVATED))