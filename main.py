import discord
import os
from discord.ext import commands
from googletrans import Translator
from dotenv import load_dotenv
from art import text2art  
from colorama import Fore, Style, init

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

@bot.event
async def on_ready():
    try:
        ascii_art_text = text2art("Skoda Studio")

        print(Fore.LIGHTCYAN_EX + ascii_art_text + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX + f"Logged in as {bot.user}" + Style.RESET_ALL)

        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Skoda®Studio"))
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error in on_ready event: {e}" + Style.RESET_ALL)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if bot.user in message.mentions:
        if message.reference:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            original_text = original_message.content

            detected_lang = translator.detect(original_text).lang
            
            if detected_lang == "ar":
                target_lang = "en"
            elif detected_lang == "en":
                target_lang = "ar"
            else:
                await message.channel.send(f"{message.author.mention} \n The message is neither in Arabic nor English.")
                return

            try:
                translation = translator.translate(original_text, dest=target_lang)
                await message.channel.send(f"{message.author.mention}\n{translation.text}")
            except Exception as e:
                await message.channel.send(f"{message.author.mention} \n An error occurred during translation.")
    
    await bot.process_commands(message)

bot.run(TOKEN)
