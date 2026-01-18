import os
import sys
import asyncio
from mistralai import Mistral
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.general import DataBase
from utils.config import (
    TOKEN, BOT_NAME, AI_PROMPT_TEMPLATE, 
    MAX_RESPONSE_LENGTH, PAYMENT_CUR
)
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = DataBase()

api_key = os.getenv("MISTRAL_KEY")

def user_mode(user_id: int) -> str:
    search = db.search_user(user_id)
    if search:
        mode = search.get("preferences", {}).get("default_mode", "brutal")
        return mode
    return "brutal"

def premium_key():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔐 Upgrade Premium", callback_data="upgrade")]
        ]
    )
    
def make_key():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Change Mode", callback_data="change_mode")],
            [InlineKeyboardButton(text="Updates Channel", url="https://t.me/asqlan")],
            [InlineKeyboardButton(text="Donate Project", callback_data="donate")]
        ]
    )


def select_mode():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="brutal 😈", callback_data="brutal")],
            [InlineKeyboardButton(text="philosophical 🧠", callback_data="philosophical")],
            [InlineKeyboardButton(text="sarcastic 😂", callback_data="sarcastic")]
        ]
    )


async def ask_ai(text: str, user_id: int) -> str:
    try:
        if not api_key:
            return "⚠️ Error: Mistral API key not configured"
        
        mode = user_mode(user_id)
        
        prompt = AI_PROMPT_TEMPLATE.format(
            user_message=text,
            mode=mode,
            max_length=MAX_RESPONSE_LENGTH
        )
        
        client = Mistral(api_key=api_key)
        
        chat_response = await asyncio.to_thread(
            client.chat.complete,
            model='mistral-large-latest',
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        if chat_response and chat_response.choices:
            content = chat_response.choices[0].message.content
            return content.strip() if content else "⚠️ Empty response from AI"
        
        return "⚠️ No response from AI"
        
    except Exception as e:
        error_msg = str(e)
        print(f"AI Error for user {user_id}: {error_msg}")
        return f"⚠️ Error generating response: {error_msg}"


@dp.message(Command("start"))
async def start(message: Message):
    user = message.from_user
    registered = db.register_user(user.id, user.username, "brutal")
    users = db.search_user(user.id)
    
    current_mode = users.get("preferences", {}).get("default_mode", "brutal") if users else "brutal"
    plan = users.get("subscription", {}).get("plan", "free") if users else "free"
    message_sent = users.get("usage", {}).get("messages_sent", 0) if users else 0
    usage = users.get("usage", {}).get("daily_limit", 10) if users else 10
    
    bot_desc = (
        f"Hello, I'm {BOT_NAME}.\n"
        f"The bot that tells you the truth without mercy 😈\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🤖 Bot Status: <code>ONLINE</code>\n"
        f"🆔 User ID: <code>{user.id}</code>\n"
        f"✅ Registered: <code>{'NO' if registered else 'YES'}</code>\n"
        f"🎭 Current Mode: <code>{current_mode.upper()}</code>\n"
        f"🎖 Plan: <code>{plan.upper()}</code>\n"
        f"📊 Usage: <code>{message_sent} / {usage}</code>\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    await message.answer(
        text=bot_desc,
        reply_markup=make_key(),
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )


@dp.callback_query(F.data == "change_mode")
async def change_mode(call: CallbackQuery) -> None:
    await call.message.answer(
        text="Choose a mode to start:",
        reply_markup=select_mode(),
        reply_to_message_id=call.message.message_id
    )
    await call.answer()


@dp.callback_query(F.data == "upgrade")
async def upgrade_premium(call: CallbackQuery) -> None:
    try:
        await call.message.answer_invoice(
            title="Premium Subscription",
            description="Upgrade to premium and upgrade daily usage to 100 usage with advanced features!",
            payload=f"premium_upgrade_{call.from_user.id}",
            currency=PAYMENT_CUR,
            prices=[
                LabeledPrice(label="Premium Plan", amount=250)
            ],
            reply_to_message_id=call.message.message_id
        )
        await call.answer()
    except Exception as e:
        error_message = str(e)
        print(f"Payment error: {error_message}")
        await call.answer(
            "⚠️ Payment system is temporarily unavailable. Please contact support.",
            show_alert=True
        )


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    user_id = message.from_user.id
    payment_info = message.successful_payment
    
    db.upgrade_user_plan(user_id, "premium")
    
    await message.answer(
        f"✅ Payment successful!\n\n"
        f"💳 Amount: {payment_info.total_amount // 100} {payment_info.currency.upper()}\n"
        f"🎖 You now have premium access!\n"
        f"📊 Unlimited messages available\n\n"
        f"Thank you for your support! 🙏",
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )


@dp.callback_query(F.data.in_(["brutal", "philosophical", "sarcastic"]))
async def choose_mode(call: CallbackQuery):
    user_id = call.from_user.id
    db.update_mode(user_id, call.data)
    
    await call.message.edit_text(
        f"✅ Mode updated to <b>{call.data}</b>",
        reply_markup=make_key(),
        parse_mode="HTML"
    )
    await call.answer()


@dp.callback_query(F.data == "donate")
async def donate_info(call: CallbackQuery):
    await call.answer("Donation feature coming soon!", show_alert=True)


@dp.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    
    user_data = db.search_user(user_id)
    if not user_data:
        await message.answer(
            "Please use /start first to register!",
            reply_to_message_id=message.message_id
        )
        return
    
    usage = user_data.get("usage", {})
    messages_sent = usage.get("messages_sent", 0)
    daily_limit = usage.get("daily_limit", 10)
    
    if messages_sent >= daily_limit:
        await message.answer(
            "⚠️ You've reached your daily message limit!\n"
            f"<b>{messages_sent}/{daily_limit}</b> messages used.\n\n"
            "Upgrade to premium for more messages!",
            parse_mode="HTML",
            reply_markup=premium_key(),
            reply_to_message_id=message.message_id
        )
        return
    
    await bot.send_chat_action(message.chat.id, "typing")
    
    response = await ask_ai(message.text, user_id)
    
    db.increment_message_count(user_id)
    
    await message.answer(
        response,
        parse_mode="HTML",
        reply_to_message_id=message.message_id
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print(f"Bot {BOT_NAME} started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())