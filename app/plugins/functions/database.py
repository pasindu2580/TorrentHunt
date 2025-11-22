from database.models import BotConfig, Setting
from pyrogram import Client
from sqlalchemy import select


async def get_restricted_mode(user_id: int):
    query = select(Setting.restricted_mode).where(Setting.user_id == user_id)
    restricted_mode = await Client.DB.execute(query)

    return restricted_mode.scalar()


async def get_bot_config():
    """Get bot configuration. Creates default config if not exists."""
    config = await Client.DB.get(BotConfig, 1)

    if not config:
        config = BotConfig(id=1)
        await Client.DB.add(config)

    return config


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
