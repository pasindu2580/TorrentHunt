from database.models import BotConfig
from py1337x import py1337x
from pyrogram import Client, filters, types
from sqlalchemy import update

from .proxies import proxies

proxies_buttons = [
    [
        types.InlineKeyboardButton(
            text=proxy,
            callback_data=f"proxy_{proxy}",
        ),
    ]
    for proxy in proxies
]


@Client.on_message(filters.command("1337x") & filters.custom.admin)
async def stats(Client, message):
    await Client.send_message(
        message.chat.id,
        text="🌐 Choose the proxy you want to use",
        reply_markup=types.InlineKeyboardMarkup(proxies_buttons),
    )


@Client.on_callback_query(filters.regex(r"^proxy_"))
async def proxy(Client, callback):
    proxy = callback.data.split("_")[1]

    # Update py1337x instance with new proxy
    Client.py1337x = py1337x.AsyncPy1337x(base_url=f"https://www.{proxy}")

    # Update proxy in database
    await Client.DB.execute(update(BotConfig).where(BotConfig.id == 1).values(proxy_1337x=proxy))

    await Client.delete_messages(
        chat_id=callback.message.chat.id,
        message_ids=callback.message.id,
    )

    await Client.misc.message_admins(
        f"ℹ️ @{callback.from_user.username} just set the proxy of 1337x to <code>{proxy}</code>"
    )
