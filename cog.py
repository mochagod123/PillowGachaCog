from discord.ext import commands
import discord
import io
from PIL import ImageFont, Image, ImageDraw, ImageSequence

class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f"init -> Cog")

    @commands.command(name="gacha")
    @commands.is_owner()
    async def gacha(self, ctx: commands.Context, user: discord.User):
        base = Image.open("data/gacha.jpg").convert("RGBA")
        read = await user.avatar.read()
        avatar = Image.open(io.BytesIO(read)).convert("RGBA").resize((423, 411))
        paste_position = (150, 385)
        background_part = base.crop((
            paste_position[0], paste_position[1],
            paste_position[0] + avatar.width, paste_position[1] + avatar.height
        ))
        avatar_with_bg = Image.alpha_composite(background_part, avatar)
        mask = Image.new("L", avatar_with_bg.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, avatar_with_bg.width, avatar_with_bg.height), fill=255)
        avatar_with_bg.putalpha(mask)
        base.paste(avatar_with_bg, paste_position, avatar_with_bg)
        save_ = io.BytesIO()
        base.save(save_, format="PNG")
        save_.seek(0)
        await ctx.reply(file=discord.File(save_, "gacha.png"))
        save_.close()

async def setup(bot):
    await bot.add_cog(Cog(bot))
