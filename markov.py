import nextcord
from nextcord.ext import commands
import os


client = commands.AutoShardedBot(command_prefix = "!", intents = nextcord.Intents.default()) 
client.remove_command("help") 

SPECIFIC_USER_ID = 768362094562639893


@client.event
async def on_ready():
    print(f"Bot successfully started!")
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Comet")) 
    
@client.event
async def on_message(message):
    if message.author.id == SPECIFIC_USER_ID:
        
        response = "f{user_mention}, Okay but Who asked ?"
        await message.channel.send(response)

client.run("MTEzNjIxMzY2OTUzODE3Mjk1OQ.G8tjul.ruenZ_itrbhXuLLpziT57eykXlkclf7iZBNdes") 