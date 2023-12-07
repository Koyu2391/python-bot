import nextcord
from nextcord.ext import commands
from nextcord import member
from nextcord import Interaction
from nextcord.ext.commands import has_permissions, MissingPermissions
from pytube import YouTube
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io



intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.members = True
intents.messages = True

#ye wala function pytube ko call lga kr video ko download krega 
def download_video(video_url):
    try:
        youtube_video = YouTube(video_url)
        video_title = youtube_video.title
        stream = youtube_video.streams.get_highest_resolution()  #highest resolution stream
        download_url = stream.url
        return video_title, download_url
    except Exception as e:
        raise ValueError("Error downloading video. Please check the URL and try again.")

# my_user_id = 741689211127857293 
# ye koyu_2931 ka user id hai 

client = commands.Bot(command_prefix= '!', intents = intents)

# launch command/event
@client.event
async def on_ready():
    print("The College_Bot has Deployed and ready to use")
    print("_____________________________________________")

# greet/ welcome quite useless to be honest
@client.command()
async def hello(ctx):
    print("Command received, Executing function hello")
    await ctx.send(f"Hello, {ctx.author.mention}! I am a bot under development by koyu")
    await ctx.send('and i am a dumb bot do not expect much form me')

# again a useless interaction command
@client.command() 
async def test(ctx, *, message_to_send):
    print("Command received, Executing function")
    print("printing " + " : " + message_to_send)
    await ctx.send(message_to_send)

# yup ye member join waala event brhiya h iska use case bhi h
@client.event
async def on_member_join(member : nextcord.member):
    print("New member joined, executing function on_member_join")
    channel = client.get_channel(1050168286437986406)
    embed = nextcord.Embed(title="Welcome To GeekyMACET", description=None, color=0xFFF8DC)
    embed.set_author(name=member.name, url="https://discord.gg/AJNTytWkKd", icon_url= member.avatar.url)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2023/06/08/13/04/fichtelbergbahn-8049565_1280.jpg")
    embed.add_field(name="Instruction", value=f"Welcome {member.mention} to GeekyMacet!\n\n"
                                               f"Make sure to check out https://discord.com/channels/1050155100557017099/1050725886145605654 and be sure to assign roles in https://discord.com/channels/1050155100557017099/1050727362972622908.\n\n"
                                               f"Also, please briefly introduce yourself on https://discord.com/channels/1050155100557017099/1050725966210666506 and good luck exploring the GeekyMacet.\n\n"
                                               f"If you have any questions or queries, feel free to ask.", inline=False)
    embed.set_footer(text="Developed by Fahad")
    await channel.send(embed=embed)

# gotta improve this one as it was merely for the testing purpose in the beginning 
@client.event
async def on_member_remove(member):
    print("Command received, Executing function on_member_leave")
    channel = client.get_channel(1050168286437986406)
    await channel.send(f'Dekh bhai koi server leave kiya: {member.mention}')


# this can be useful only when my bot performs something in the voice channel i don't know why do i even have these command
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Already with you in the voice channel")
    else: 
        await ctx.send("You need to join a Voice channel first")

# and again the same thing there are no use of this as well 
@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("As per your commands I left the voice channel")
    else: 
        await ctx.send("I am not in a voice Channel") 

#completely useless as for now but i gotta make it meaningful 
@client.event
async def on_message(message):
    #specific_user = nextcord.utils.get(message.mentions, id=my_user_id)
    #ye check kr rha ki kya specific user, mere user id ko mention kiya hai ya nhi
    
    # Check if the bot is mentioned in the message
    
    if client.user.mentioned_in(message):
        await message.channel.send("Ohh yes Hello! I can respond to pings now")
        
    await client.process_commands(message)
    
# /help command- gotta make it more personalized and mgotta add more visuals 
@client.slash_command(guild_ids=[1135433610040725524, 1050155100557017099], name="help", description="help")
async def help_command(interaction: nextcord.Interaction):
    channel = interaction.channel
    userName = interaction.user.name

    embed = nextcord.Embed(title="Help", description="All the available bot commands", color=0xFFF8DC)
    embed.set_author(name=userName, url="https://discord.gg/AJNTytWkKd", icon_url=interaction.user._avatar)
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2023/06/08/13/04/fichtelbergbahn-8049565_1280.jpg")
    embed.add_field(name="Resend Message", value="Using !test will resend the message that was written after the command", inline=False)
    embed.add_field(name="Join Voice channel", value="Using !join will make the bot join voice channel", inline=False)
    embed.add_field(name="Leave Voice channel", value="Using !leave will make the bot leave voice channel", inline=False)
    embed.add_field(name="Greetings", value="Using !hello will make the bot greet you", inline=False)
    embed.add_field(name="Download", value="You can download YT videos using /download", inline=False)
    embed.add_field(name="Profile", value= "You can see your profile", inline=False)
    await channel.send(embed=embed)


# /download - to download yt videos from the yt url 
@client.slash_command(guild_ids=[1135433610040725524, 1050155100557017099], name="download", description="Paste YT video Url to download it")
async def download_command(interaction: nextcord.Interaction, video_url: str):
    # calling the pytube function
    try:
        print(video_url)
        video_title, download_url = download_video(video_url)
    except ValueError as e:
        await interaction.channel.send(e)
        return

    user = interaction.user
    await user.send(f"Here's the download link for '{video_title}': {download_url}")
    await interaction.channel.send(f'{user.mention}Video download link sent to your DM!')

@client.slash_command(guild_ids=[1135433610040725524, 1050155100557017099], name="profile", description="Check Your Profile")
async def profile(interaction : nextcord.Interaction):
    user = interaction.user

    
    image = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    
    font = ImageFont.truetype("arial.ttf", 20)
    
    border_color = (255, 165, 0)  
    border_width = 5
    draw.rectangle([(border_width, border_width), (image.width - border_width, image.height - border_width)], outline=border_color, width=border_width)

    
    avatar = await interaction.user.display_avatar.read()
    
    avatar_image = Image.open(io.BytesIO(avatar))
    avatar_image = avatar_image.resize((100, 100))
    image.paste(avatar_image, (20, 50))
    
    mask = Image.new("L", avatar_image.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_image.width, avatar_image.height), fill=255)

    avatar_image = ImageOps.fit(avatar_image, mask.size, centering=(0.5, 0.5))
    avatar_image.putalpha(mask)
    

    
    name_color = (255, 0, 0)  
    draw.text((150, 50), interaction.user.display_name, fill=name_color, font=font)
    

    
    date_color = (0, 128, 0)  
    draw.text((150, 100), f"Join Date: {user.created_at.strftime('%Y-%m-%d')}", fill=date_color, font=font)

   
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Send the image
    await interaction.channel.send(file=nextcord.File(buffer, filename="profile.png"))



client.run('MTEzNTU5MjQyNDE1MzA0Mjk5NA.GohfLS.EGPLPOiSsjWgNn8V05bzKFmZQWdLmvloUNg0Cg')
#bot api token