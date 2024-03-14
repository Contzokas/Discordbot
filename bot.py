import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

log_channel_name = '🧾⁝logs'

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_message(message):
    # Ensure the message is not from the bot itself
    if message.author == bot.user or message.author.bot:
        return

    # Log the message to the logs channel
    log_channel = discord.utils.get(message.guild.channels, name=log_channel_name)
    if log_channel:
        embed = discord.Embed(title="Message Log", color=0x00ff00)
        embed.set_author(icon_url=message.author.avatar, name=str(message.author))
        embed.add_field(name="Content", value=message.content, inline=False)
        
        # Include attachment URLs if any
        attachment_urls = []
        for attachment in message.attachments:
            if attachment.content_type.startswith('image/'):
                embed.set_image(url=attachment.url)
            elif attachment.content_type.startswith('video/'):
                attachment_urls.append(attachment.url)
            else:
                attachment_urls.append(attachment.url)
        
        if attachment_urls:
            embed.add_field(name="Attachments", value="\n".join(attachment_urls), inline=False)
        
        await log_channel.send(embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = discord.utils.get(member.guild.channels, name=log_channel_name)
    if log_channel:
        if before.channel != after.channel:
            embed = discord.Embed(title="Voice Channel Log", color=0x00ff00)
            embed.set_author(icon_url=member.avatar, name=str(member))
            if before.channel is None:
                embed.description = f'{member.display_name} has connected to voice channel {after.channel.name}'
            elif after.channel is None:
                embed.color = 0xff0000  # Change color to red
                embed.description = f'{member.display_name} has disconnected from voice channel {before.channel.name}'
            else:
                embed.description = f'{member.display_name} has moved from voice channel {before.channel.name} to {after.channel.name}'
            
            await log_channel.send(embed=embed)


@bot.command()
async def sotiris(ctx):
    # Tagging user "sotosdr" by mentioning their user ID
    user_id = 934854583187046431 # Replace with the actual user ID of sotosdr
    await ctx.send(f"<@{user_id}> ΓΑΜΙΕΣΑΙ")
    await ctx.message.delete()

@bot.command()
async def thanos(ctx):
    await ctx.send(f"Αντί για 2 αυτονίκητο 2 κινητά έχω 2 κοπέλες")
    await ctx.message.delete()

@bot.command()
async def zaharakis(ctx):
    # Tagging user "sotosdr" by mentioning their user ID
    user_id = 505680342682959882 # Replace with the actual user ID of sotosdr
    await ctx.send(f"https://tenor.com/bRrcQ.gif")
    await ctx.message.delete()

@bot.command()
async def mitsos(ctx):
    # Tagging user "sotosdr" by mentioning their user ID
    user_id = 505680342682959882 # Replace with the actual user ID of sotosdr
    await ctx.send(f"https://cdn.discordapp.com/attachments/1212303321277407252/1217934973898850465/3775046.png?ex=6605d555&is=65f36055&hm=e9b8997ba9761bc590749b6f45c6c50304eb7200dde65eeedf446b20d8bf233f&")
    await ctx.message.delete()

@bot.event
async def on_message(message):
    # Check if the message author's ID matches the specified user ID
    if message.author.id == 934854583187046431:
        # Send the message with the word "ανήλικα"
        await message.channel.send(f"<@{934854583187046431}> Πάμε για ανήλικα?")
    
    # Continue processing other commands and events
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Check if the message author's ID matches the specified user ID
    if message.author.id == 505680342682959882:
        # Send the message with the word "ανήλικα"
        await message.channel.send(f"<@{505680342682959882}> https://cdn.discordapp.com/attachments/1212303321277407252/1217931559227887687/s-l1600.jpg?ex=6605d227&is=65f35d27&hm=c34943256a834f3be6f4c4cb0edea35c7883119e64a037b96921c14f16e71de0&")
    
    # Continue processing other commands and events
    await bot.process_commands(message)

bot.run(TOKEN)


