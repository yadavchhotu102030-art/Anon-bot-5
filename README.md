# Anonymous Telegram Bot

## 🚀 Features
- Anonymous random chat matching
- "Start", "Stop", "Help" buttons with emojis
- Spectator group mirroring for admins
- Admins can watch all conversations live
- `/getid` command → easily get group IDs

## 🛠 Deployment (Render + GitHub)
1. Push this code to a GitHub repo.
2. Go to Render.com → New Web Service → Connect this repo.
3. Render will read `render.yaml` and deploy your bot as a Web Service (not worker).
4. Set environment variables in Render:
   - BOT_TOKEN = your Telegram bot token
   - ADMIN_IDS = comma-separated Telegram user IDs of admins (e.g., 123456,987654)
   - SPECTATOR_GROUP_ID = Telegram group ID for moderation feed
5. Start the service.

## 📋 Usage
- Users: `/start` to begin, buttons for chatting.
- Moderators: add bot to your group, set group ID as SPECTATOR_GROUP_ID, all chats mirrored.
- Use `/getid` in any group to get its numeric ID.
