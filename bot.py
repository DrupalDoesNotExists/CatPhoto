""" BadCat uses thiscatdoesnotexists service to generate cool cat avatars """
from discord.ext.commands import Bot, Context
from discord import Embed, Intents, File
import httpx
from pathlib import Path

from random import choice

import settings


temp_path: Path = Path('catphoto.png')
url: str = "https://thiscatdoesnotexist.com/"
phrases = (
    "Лови милоту!",
    "Вот ваш котан",
    "Кошаки в атаку!",
    "Котик присоединился к чату",
    "Котика звали?",
    "Вы ж мои котики!",
    "Святые котики! У него же лапки!"
)

intents = Intents.default()
intents.message_content = True
bot: Bot = Bot(command_prefix=settings.PREFIX, intents=intents)

@bot.command(name="avatar")
async def avatar(ctx: Context) -> None:
    """ Generate new avatar """
    if ctx.channel.id != settings.CHANNEL:
        return

    await ctx.message.delete()

    image: httpx.Response = httpx.get(url)
    if image.status_code != 200:
        await ctx.send(f"Ooops! Cat does not exists! {image.status_code}")
        return

    with open(temp_path, 'wb') as file:
        file.write(image.content)

    await ctx.send(choice(phrases), file=File(fp=temp_path, filename="Cat.png"))

bot.run(settings.TOKEN)