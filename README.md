# 🤖 BrutalBot

> The Telegram bot that tells you the truth without mercy 😈

BrutalBot is an AI-powered Telegram bot with multiple personality modes, built with aiogram 3.x and Mistral AI. Choose between brutal honesty, philosophical wisdom, or sarcastic humor for your conversations.

## ✨ Features

- 🎭 **Multiple AI Modes**
  - **Brutal Mode** 😈 - Unfiltered, honest responses
  - **Philosophical Mode** 🧠 - Thoughtful, deep insights
  - **Sarcastic Mode** 😂 - Witty, humorous replies

- 💬 **Smart Conversations**
  - Powered by Mistral AI (mistral-large-latest)
  - Context-aware responses
  - Customizable response length

- 📊 **Usage Management**
  - Daily message limits for free users
  - Premium subscription via Telegram Stars
  - Usage tracking and statistics

- 💳 **Payment Integration**
  - Telegram Stars payment support
  - Easy premium upgrade
  - Automated subscription management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Mistral AI API Key (from [Mistral AI](https://mistral.ai))

### Installation

1. Clone the repository
```bash
git clone https://github.com/NotAnyOneMe/BrutalBot.git
cd BrutalBot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` file with your credentials:
```env
TOKEN=your_telegram_bot_token
MISTRAL_KEY=your_mistral_api_key
BOT_NAME=BrutalBot
PAYMENT_CUR=XTR
MAX_RESPONSE_LENGTH=500
```

4. Configure the bot

Edit `utils/config.py` to customize:
- AI prompt templates
- Daily message limits
- Premium pricing
- Response settings

5. Run the bot
```bash
python bot/main.py
```

## 📁 Project Structure

```
BrutalBot/
├── bot/
│   └── main.py              # Main bot logic and handlers
├── database/
│   └── general.py           # Database operations
├── utils/
│   └── config.py            # Configuration settings
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🎮 Usage

### Bot Commands

- `/start` - Register and view bot status
- Send any text message to chat with the AI

### Available Modes

**Brutal Mode** 😈
- Direct, unfiltered responses
- No sugar-coating
- Honest feedback

**Philosophical Mode** 🧠
- Deep, thoughtful insights
- Reflective answers
- Wisdom-focused

**Sarcastic Mode** 😂
- Witty, humorous responses
- Playful sarcasm
- Entertainment-focused

### Inline Buttons

- **Change Mode** - Switch between AI personalities
- **Updates Channel** - Follow bot updates
- **Donate Project** - Support development
- **Upgrade Premium** - Get unlimited messages

## 💎 Premium Features

Free users get 10 messages per day. Premium subscribers enjoy:
- ♾️ Unlimited messages
- 🚀 Priority response times
- ⭐ Support development

Upgrade via Telegram Stars payment directly in the bot.

## 🛠️ Configuration

### Database Schema

Users are stored with the following structure:
```python
{
    "user_id": int,
    "username": str,
    "preferences": {
        "default_mode": "brutal|philosophical|sarcastic"
    },
    "subscription": {
        "plan": "free|premium"
    },
    "usage": {
        "messages_sent": int,
        "daily_limit": int
    }
}
```

### AI Prompt Template

Customize the AI behavior in `utils/config.py`:
```python
AI_PROMPT_TEMPLATE = """
You are a {mode} assistant.
User message: {user_message}
Maximum response length: {max_length} characters
"""
```

## 🔧 Development

### Requirements

```txt
aiogram>=3.0.0
mistralai>=0.1.0
python-dotenv>=1.0.0
```

### Adding New Modes

1. Add mode to `select_mode()` keyboard
2. Update `AI_PROMPT_TEMPLATE` to handle new mode
3. Add mode to database schema if needed

### Database Methods

The bot requires these database methods:
- `register_user(user_id, username, mode)`
- `search_user(user_id)`
- `update_mode(user_id, mode)`
- `increment_message_count(user_id)`
- `upgrade_to_premium(user_id)`

## 🐛 Troubleshooting

**"Payment system not configured"**
- Ensure bot has payment rights from @BotFather
- Use `PAYMENT_CUR=XTR` for Telegram Stars

**"Mistral API error"**
- Check API key is valid
- Verify API quota/limits
- Check network connectivity

**"User not registered"**
- User must send `/start` before chatting
- Check database connection

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

**Created by MLBOR**
- Telegram: [@MLBOR](https://t.me/MLBOR)
- GitHub: [@NotAnyOneMe](https://github.com/NotAnyOneMe)
- Repository: [BrutalBot](https://github.com/NotAnyOneMe/BrutalBot)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support

For support and updates:
- Join our Telegram channel: [@asqlan](https://t.me/asqlan)
- Open an issue on GitHub
- Contact developer: [@MLBOR](https://t.me/MLBOR)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by MLBOR**
