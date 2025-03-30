# Nistkasten 3000

Nistkasten 3000 is an easy-to-use Telegram bot designed to work with Motion.  
It automatically sends videos or photos of a webcam to a Telegram chat when motion is detected.  
Additionally, users in the Telegram chat can manually control the bot to start/stop motion detection or request videos/photos.

I use it for a birds nesting box (german: Nistkasten).

---

## Features

- **Motion Detection**: Automatically sends videos/photos to a Telegram chat when motion is detected.  
- **Manual Control**: Users can manually request videos or photos via Telegram commands.  
- **Start/Stop Motion Detection**: Control motion detection directly from the Telegram chat.  

---

## Installation  

Follow these steps to set up and run Nistkasten 3000:  

### 1. Prerequisites
- Ensure Docker and Docker Compose are installed on your system.  
- Ensure that the access to the webcam (f.e. /dev/video0) is granted for every user
- Clone this repo and cd into it

### 2. Create Telegram Bot  
- Open Telegram and search for the BotFather.  
- Use the /newbot command to create a new bot.  
- Follow the instructions to get your bot's API token and save it for later.  

### 3. Get Your Chat ID  
- Start a private or group chat with your bot where it should operate and send the message `/start`.  
- Now visit `https://api.telegram.org/botTOKEN/getUpdates` and replace TOKEN by your API token.  
- Extract the ChatID and save it for later.
- If you can't find the chat in the json keep sending `/start` and refresh the website.

### 4. Configure the Environment  
- Rename `example.env` to `secrets.env`.  
- Fill in `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.  

### 5. Start the Bot on the machine  
- Run `docker-compose up -d` in the root directory of this repo.

### 6. /start the Bot in Telegram  
- Type `/start` into the chat where the bot should operate.  
- Try it...  

## Configuration

- You can configure Motion via the `conf/motion.conf` file.  
- You can configure the Bot's Name, Timeout and Language in the docker-compose.yml
