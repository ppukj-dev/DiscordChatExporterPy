import discord
import chat_exporter
import os
import io
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Live: " + bot.user.name)
    chat_exporter.init_exporter(bot)


@bot.command()
async def save(ctx, begin_message_id = None, end_message_id = None, limit: int = None, tz_info = "Asia/Jakarta"):
    end_time = None
    begin_time = None

    if begin_message_id:
        begin_time = (await ctx.fetch_message(begin_message_id)).created_at - timedelta(milliseconds=1)
    
    if end_message_id:
        end_time = (await ctx.fetch_message(end_message_id)).created_at + timedelta(milliseconds=1)


    transcript = await chat_exporter.export(ctx.channel, ctx.guild, limit=limit,  begin_time=begin_time, end_time=end_time, set_timezone=tz_info)

    if transcript is None:
        return

    transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                    filename=f"transcript-{ctx.channel.name}.html")

    await ctx.send(file=transcript_file)

if __name__ == "__main__":
    ENV = os.getenv("ENV")

    if ENV == 'dev':
        load_dotenv('.env.dev')
    else:
        load_dotenv('.env')

    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
