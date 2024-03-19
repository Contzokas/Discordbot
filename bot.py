import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

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
        embed.add_field(name="Channel", value=message.channel, inline=False)
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
                embed.color = 0xff0000 
                embed.description = f'{member.display_name} has disconnected from voice channel {before.channel.name}'
            else:
                embed.color = 0xFFFFE0
                embed.description = f'{member.display_name} has moved from voice channel {before.channel.name} to {after.channel.name}'
            
            await log_channel.send(embed=embed)


@bot.command()
async def sotiris(ctx):
    user_id = 934854583187046431
    await ctx.send(f"<@{user_id}> ΓΑΜΙΕΣΑΙ")
    await ctx.message.delete()

@bot.command()
async def thanos(ctx):
    await ctx.send(f"Αντί για 2 αυτονίκητο 2 κινητά έχω 2 κοπέλες")
    await ctx.message.delete()

@bot.command()
async def zaharakis(ctx):
    user_id = 505680342682959882
    await ctx.send(f"https://tenor.com/bRrcQ.gif")
    await ctx.message.delete()

@bot.command()
async def mitsos(ctx):
    user_id = 505680342682959882 
    await ctx.send(f"https://cdn.discordapp.com/attachments/1212303321277407252/1217934973898850465/3775046.png?ex=6605d555&is=65f36055&hm=e9b8997ba9761bc590749b6f45c6c50304eb7200dde65eeedf446b20d8bf233f&")
    await ctx.message.delete()

@bot.event
async def on_invite_create(invite):
    log_channel = discord.utils.get(invite.guild.channels, name=log_channel_name)
    if log_channel:
        creation_time = invite.created_at
        uses = invite.uses
        duration = invite.max_age

        # Convert duration to a readable format
        duration_str = 'Unlimited' if duration == 0 else str(timedelta(seconds=duration))

        embed = discord.Embed(title="Invite Created", color=discord.Color.purple())
        embed.set_author(name=invite.inviter.display_name, icon_url=invite.inviter.avatar)
        embed.add_field(name="Created At", value=creation_time.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Uses", value=uses, inline=False)
        embed.add_field(name="Duration", value=duration_str, inline=False)

        await log_channel.send(embed=embed)

@bot.event
async def on_invite_delete(invite):
    log_channel = discord.utils.get(invite.guild.channels, name=log_channel_name)
    if log_channel:
        embed = discord.Embed(title="Invite Revoked", color=0xff0000)
        embed.add_field(name="Time Revoked", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Revoked By", value=invite.revoked.display_name if invite.revoked else "Unknown", inline=True)
        await log_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    log_channel = discord.utils.get(guild.channels, name=log_channel_name)
    if log_channel:
        embed = discord.Embed(title="Member Banned", color=0xff0000)
        embed.set_author(name=user.display_name, icon_url=user.avatar)
        embed.add_field(name="Banned By", value=guild.me.display_name)
        await log_channel.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except discord.HTTPException:
        await ctx.send("Banning the member failed.")



bot.run(TOKEN)

