#This is a discord bot with a range of different commands, however some of the commands utilse the ctx element which does not support slash commands meaning you need
#to type the "equal symbol" instead.
#To change these to slash commmands you will need to swap elements like def ctx to this and follow the other ones. @client.tree.command

#This is a discord bot named Kian which has a range of different features including kicking members,banning members,opening tickets and many more intesting things such as chat gpt.
#This discord bot includes memes and funny commands too so be sure to try it out, just replace the token key at the bottom of this with yours and the open ai key on the offical website.

#Simple discord Bot, you will need the follwing libraies shown in the imports for this to work.


import discord
from discord import app_commands
from itertools import cycle
import random
from discord.ext import commands, tasks
from discord.utils import get
import time
import random
import aiohttp
import asyncio
import feedparser
import json
import openai



















#key commands


intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix="=", intents=discord.Intents.all())
ROLE = "TECHGUIN"







    




status = cycle(["Type =help for support", "Skibidi rizz in Ohio Gyatt", "Discord https://discord.gg/zcs9XYBx", "I love everyone ", "Be as positive as a proton and as negative as a electron"])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))







#run the discord bot

@client.event
async def on_ready():
    print("DISCORD BOT IS ONLINE")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    change_status.start()
    send_news.start()  # Start the send_news task




openai.api_key = "Insert OpenAI key here to add chatgpt element to the bot"


@client.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    if client.user in message.mentions:
        content = message.content.replace(f'<@!{client.user.id}>', '').strip()

        await message.channel.send("Generating response...")

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
  
                prompt=content,
                max_tokens=100
            )
            await message.channel.send(response.choices[0].text.strip())
        except openai.error.OpenAIError as e:
            await message.channel.send(f"Error from OpenAI: {e}")
        except Exception as e:
            await message.channel.send(f"Unexpected error: {e}")







#latest technology news


CHANNEL_ID = 870757500486578217 # Replace with your channel ID


sent_news_links = set()

@tasks.loop(minutes=15)  # Check for updates every 10 minutes
async def send_news():
    # URL of the XML feed
    rss_feed_url = 'https://rss.app/feeds/_05NmCLUJjlI9Qwur.xml' #To get the link for this You visit "rss.app" website and add websites together and copy the link

    feed = feedparser.parse(rss_feed_url)

    news_entries = [(entry.title, entry.link) for entry in feed.entries]

    channel = client.get_channel(CHANNEL_ID)

    num_news_to_send = random.randint(2, 6)
    selected_news = random.sample(news_entries, min(len(news_entries), num_news_to_send))

    for title, link in selected_news:
        if link not in sent_news_links:
            await channel.send(f"\n{link}")
            sent_news_links.add(link)  


# Command to start sending news immediately
@client.command()
@commands.has_permissions(administrator=True)  # Only administrators can use this command
async def latest_news(ctx):
    await send_news.start()
    await ctx.send("Sending the latest technology news!")

@client.command()
@commands.has_permissions(administrator=True)  # Only administrators can use this command
async def generate(ctx):
    await send_news.start()
    await ctx.send("Generating and sending the latest technology news!")













# Setup

@client.command()
async def setup(ctx):
    embed = discord.Embed(colour=discord.Colour.green())

    # Ticket System
    embed.description= 'Do you want me to setup my ticket system? Type y for YES and n for NO'
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', timeout=30)
    if msg.content == "yes" or msg.content == "y":
        guild = ctx.guild
        support_perms = discord.Permissions(administrator=True)
        await guild.create_role(name='Support Team', permissions=support_perms)
        await ctx.guild.create_category('tickets')
        embed.description= """I created ``Support Team`` role for my ticket system.\nI created ``TICKETS`` category for my ticket system."""
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)
    else:
        await ctx.send('Kian nods his head')

    # Mute System
    embed.description = 'Do you want me to create ``Muted`` role for my mute system? Type y for YES and n for NO'
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', timeout=30)
    if msg.content == "yes" or msg.content == "y":
        mute_perms = discord.Permissions(send_messages=False, read_messages=True)
        await guild.create_role(name='Muted', permissions=mute_perms)
        embed.description='I created ``Muted`` role for my mute system.'
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)
    else:
        await ctx.send('Kian nods his head')

    # Verification System
    embed.description = 'Do you want me to setup my verification system? Type y for YES and n for NO'
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', timeout=30)
    if msg.content == "yes" or msg.content == "y":
        # Member Role
        perms = discord.Permissions(send_messages=True, read_messages=True)
        await guild.create_role(name='Member', permissions=perms)
        # Verification Channel
        await ctx.guild.create_text_channel(name='verification')
        channel = discord.utils.get(ctx.guild.channels, name="verification")
        everyone = get(ctx.guild.roles, name='@everyone')
        Member = get(ctx.guild.roles, name='Member')
        await channel.set_permissions(everyone, read_messages=True,
                                      send_messages=True)
        await channel.set_permissions(Member, read_messages=False,
                                      send_messages=False)
        await channel.send("**``.verify {@user}`` To verify yourself and get access to all server channels!**\n\n @everyone")
        embed.description= 'I created my verification system.'
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)
    else:
        await ctx.send('Kian nods his head')

# Warning System
    embed.description= 'Do you want me to setup my warning system? Type y for YES and n for NO'
    await ctx.send(embed=embed)
    msg = await client.wait_for('message', timeout=30)
    if msg.content == "yes" or msg.content == "y":
        await guild.create_role(name='warn1')
        await guild.create_role(name='warn2')
        await guild.create_role(name='warn3')
        embed.description= 'I created my warning system.'
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)
    else:
        await ctx.send("Kian nods his head")

    # Done Setup
    await ctx.send('**The setup has been done!**\nThanks for choosing me <3')

# Ping

@client.tree.command(name="marko", description="tells you the milliseconds between you and Kian")
async def marko(interaction:discord.Interaction):
    embed = discord.Embed(colour = discord.Colour.green())
    embed.add_field(name='POLLO!', value=f'Kian says the milliseconds between us is {round(client.latency *1000)}', inline=False)

    await interaction.response.send_message(embed=embed)






# Dox

@client.tree.command(name="dox", description="dox someone you mention")
async def dox(interaction: discord.Interaction, *, user: discord.Member):
    embed = discord.Embed(colour=discord.Colour.green())
    responses1 = ['142',
                  '153',
                  '179',
                  '196',
                  '168',
                  '158',
                  '134',
                  '176']

    responses2 = ['246',
                  '159',
                  '169',
                  '239',
                  '276',
                  '147',
                  '308',
                  '207']

    countries = ['Mexico',
                 'China',
                 ' Australia',
                 'Dominican Republic',
                 'Mali, Algeria',
                 'North Korea',
                 'Sweden',
                 'Swaziland',
                 'Trinidad and Tobago',
                 'Sierra Leone',
                 'Togo',
                 'Comoros',
                 'Chad',
                 'Estonia',
                 'Taiwan',
                 'United States',
                 'Azerbaijan',
                 'Central African Republic',
                 'Gabon',
                 'Namibia',
                 'Lithuania,',
                 'Germany',
                 'United Kingdom',
                 'Israel',
                 'Russia',
                 'Canada',
                 'Alaska',
                 'France',
                 'Ohio',
                 'UNKNOWN']

    computer = ['Windows', 'Mac', 'Linux', 'IOS', 'Android', 'UNKNOWN']

    embed.add_field(name=f':skull_crossbones: Doxxed {user} successfully\n  ㅤ', value=f"""{user} IP: **192.{random.choice(responses1)}.{random.choice(responses2)}**\n {user} country: **{random.choice(countries)}**\n{user} Computer: **{random.choice(computer)}**""", inline=False)
    embed.add_field(name='  ㅤ', value='  ㅤ\nNOTE- This information is REAL, Unless they VPN user!', inline=True)
    embed.set_footer(text='© TECHGUIN')
    embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJwd2VjZXlia3dya25yNnVqdnVkZ3hsYnR4NDlzMXF4ODIxOWc3dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Z3VgQu8hkVeB1bakS9/giphy.gif")

    await interaction.response.send_message(embed=embed)

@dox.error
async def dox_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour= discord.Colour.red())
        embed.add_field(name=':x: **Dox Error**\n', value=' ㅤ\n``.dox {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await interaction.response.send_message(embed = embed)


# 8ball

@client.command(aliases=['ball', 'question'])
async def _8ball (ctx, *, user: discord.Member, question):
    embed = discord.Embed(colour=discord.Colour.green())
    responses = ['yes',
                 'no',
                 'yep',
                 'nah',
                 'frick no',
                 'fuck yeah',
                 'idk']
    embed.add_field(name=f'The question: {question}', value=f'\n\n**Answer: {random.choice(responses)}**', inline=False)
    embed.set_footer(text='© TECHGUIN')

    await ctx.send(embed=embed)

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour= discord.Colour.red())
        embed.add_field(name=':x: **Ball Error**\n', value=' ㅤ\n``.ball {question}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed = embed)

# Purge

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount : int):
    embed = discord.Embed(colour=discord.Colour.green())
    await ctx.channel.purge(limit=amount)
    embed.description= f'**Purge**\nI purged {amount}'

@purge.error
async def purge_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Purge Error**\n', value=' ㅤ\n``.purge {amount}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

# Kick member

@client.tree.command(name="kick", description="Administrators kick members")
@commands.bot_has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
    author = interaction.user
    
    # Check if the author is an administrator
    if not interaction.guild.get_member(author.id).guild_permissions.administrator:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**', value='You must be an administrator to use this command!', inline=False)
        await interaction.response.send_message(embed=embed)
        return
    
    # Proceed with kicking if the author is an administrator
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name=f'Kicked- {member}', value=f'Reason: {reason}', inline=False)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExajhtaDhpc2d4ajF1YW9kNjBidGpsOWswOWNhZ2lhYmY5Z28wMXZoaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tPoLnAoL7pY8p8c/giphy.gif")

    await member.kick(reason=reason)
    await interaction.response.send_message(embed=embed)


@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**', value='Usage: .kick {@mention}', inline=False)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**', value='You do not have permission to use this command!', inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Kick Error**', value='An error occurred while processing the command.', inline=False)
        await interaction.response.send_message(embed=embed)






# Ban
        
@client.tree.command(name="ban", description="administrators remove members")
@commands.bot_has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
    author = interaction.user
    
    # Check if the author is an administrator
    if not interaction.guild.get_member(author.id).guild_permissions.administrator:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Ban Error**', value='You must be an administrator to use this command!', inline=False)
        await interaction.response.send_message(embed=embed)
        return
    
    # Proceed with banning if the author is an administrator
    embed = discord.Embed(colour=discord.Colour.green())
    embed.add_field(name=f'Banned- {member}', value=f'Reason: {reason}', inline=False)
    embed.set_image(url="https://media1.tenor.com/m/3zg6UVAaWTsAAAAC/ban-elmo.gif")

    await member.ban(reason=reason)
    await interaction.response.send_message(embed=embed)


@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Ban Error**', value='Usage: .ban {@mention}', inline=False)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Ban Error**', value='You do not have permission to use this command!', inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Ban Error**', value='An error occurred while processing the command.', inline=False)
        await interaction.response.send_message(embed=embed)












@client.tree.command(name="ben", description="Administrators ban members")
@commands.has_permissions(ban_members=True)
async def ben(interaction: discord.Interaction, content: str, member: discord.Member, *, reason: str = None, id: int):
    if content == 'ed':
        guild = interaction.guild
        await guild.ban(discord.Object(id=id))
        await interaction.response.send_message(f'banned <@!{id}>')


# Unban member

@client.tree.command(name="unban", description="Administrators unban members")
@commands.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, *, user_id: str):
    banned_users = await interaction.guild.bans()
    for ban_entry in banned_users:
        if str(ban_entry.user.id) == user_id:
            embed = discord.Embed(colour=discord.Colour.green())
            embed.description = f'**Unbanned- {ban_entry.user} **'
            await interaction.guild.unban(ban_entry.user)
            await interaction.response.send_message(embed=embed)
            return

    # If the user is not found in the banned users list
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(name=':x: **Unban Error**', value=f'User with ID {user_id} is not banned.', inline=False)
    await interaction.response.send_message(embed=embed)

@unban.error
async def unban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Unban Error**', value='Usage: .unban {user_id}', inline=False)
        await interaction.response.send_message(embed=embed)


# Mute

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member):
    embed = discord.Embed(colour=discord.Colour.green())
    role = discord.utils.get(user.guild.roles, name='Muted')
    await user.add_roles(role)
    embed.description= f':mute: **Mute**\n ㅤ\nI muted {user}'

    await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Mute Error**\n', value=' ㅤ\n``.mute {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Unmute

@client.command()
async def unmute(ctx, user:discord.Member):
    embed = discord.Embed(colour=discord.Colour.green())
    role = discord.utils.get(user.guild.roles, name='Muted')
    await user.remove_roles(role)
    embed.description = f':loud_sound: **Unmute**\n ㅤ\nI Unmuted {user}'
    embed.set_footer(text='© TECHGUIN')

    await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Unmute Error**\n', value=' ㅤ\n``.unmute {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Say

@client.command()
async def say(ctx, *, say):
    embed= discord.Embed(colour=discord.Colour.green())
    embed.description = f"{say}"
    embed.set_footer(text='© TECHGUIN')

    await ctx.send(embed=embed)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Say Error**\n', value=' ㅤ\n``.say {something}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Nuke channel

@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    await ctx.send("Nuking this channel")
    time.sleep(1)
    channel_id = ctx.channel.id
    channel = client.get_channel(channel_id)
    new_channel = await ctx.guild.create_text_channel(name=channel.name, topic=channel.topic, overwrites=channel.overwrites, nsfw=channel.nsfw, category=channel.category, slowmode_delay=channel.slowmode_delay, position=channel.position)
    await channel.delete()
    await new_channel.send("Nuked this channel.\nhttps://imgur.com/LIyGeCR")

# Server info

@client.command(aliases=['srvinfo', 'svf'])
async def _svf(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",colour = discord.Colour.green())
    embed.add_field(name=f"Server Created At:", value=f"""{ctx.guild.created_at.strftime("%A, %B %d %Y")}""", inline=False)
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}", inline=False)
    embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}", inline=False)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    await ctx.send(embed=embed)

# Add Role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, mention):
    role = discord.utils.get(user.guild.roles, name=f'{mention}')
    await user.add_roles(role)
    await ctx.send(f'''I added {user} '{mention}' role!''')

@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Addrole Error**\n', value=' ㅤ\n``.addrole {@role}+{@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Remove Role

@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.Member, mention):
    role = discord.utils.get(user.guild.roles, name=f'{mention}')
    await user.remove_roles(role)
    await ctx.send(f'''I removed {user} '{mention}' role!''')

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Removerole Error**\n', value=' ㅤ\n``.removerole {@role}+{@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Verify

@client.command()
async def verify(ctx, user: discord.Member):
    if 'member' not in user.guild.roles:
        role = discord.utils.get(user.guild.roles, name='Member')
        await user.remove_roles(role)
        await ctx.send("I just verified you!")
    elif 'Member' in user.guild.roles:
        await ctx.send('You are already verified.')

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name=':x: **Verify Error**\n', value=' ㅤ\n``.verify {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Warn System

@client.command(pass_context = True)
@commands.has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx, user: discord.Member):
    warn1 = discord.utils.get(ctx.guild.roles, name= "warn1")
    warn2 = discord.utils.get(ctx.guild.roles, name= "warn2")
    warn3 = discord.utils.get(ctx.guild.roles, name= "warn3")
    if warn1 not in ctx.author.roles:
        role = discord.utils.get(user.guild.roles, name="warn1")
        await user.add_roles(role)
        await ctx.send(f""" ``{user}`` **received a warn!** """)

    elif warn1 in ctx.author.roles and warn2 not in ctx.author.roles:
        role = discord.utils.get(user.guild.roles, name="warn2")
        await user.add_roles(role)
        await ctx.send(f""" ``{user}`` **received another warn!** """)

    elif warn1 and warn2 in ctx.author.roles and warn3 not in ctx.author.roles:
        role = discord.utils.get(user.guild.roles, name="warn3")
        await user.add_roles(role)
        await ctx.send(f""" ``{user}`` **received his third warn!**""")

    elif warn3 and warn2 and warn1 in ctx.author.roles:
        await ctx.send('This user already has **3 warns!**')

@warn.error
async def warn_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Warn Error**\n', value=' ㅤ\n``.warn {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Unwarn

@client.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def unwarn(ctx, user: discord.Member):
    warn1 = discord.utils.get(ctx.guild.roles, name= "warn1")
    warn2 = discord.utils.get(ctx.guild.roles, name= "warn2")
    warn3 = discord.utils.get(ctx.guild.roles, name= "warn3")

    if warn1 in ctx.author.roles and warn2 not in ctx.author.roles:
        await user.remove_roles(warn1)
        await ctx.send(f"""Now ``{user}`` has **0 warns**""")

    elif warn2 in ctx.author.roles and warn3 not in ctx.author.roles:
        await user.remove_roles(warn2)
        await ctx.send(f"""Now ``{user}`` has **1 warn**""")

    elif warn3 in ctx.author.roles:
        await user.remove_roles(warn3)
        await ctx.send(f"""Now ``{user}`` has **2 warns**""")

@unwarn.error
async def unwarn_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Unwarn Error**\n', value=' ㅤ\n``.unwarn {@mention}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Ticket

@client.command()
async def ticket(ctx, *, content):
    embed = discord.Embed(colour=discord.Colour.green())
    y = 0
    for guild in client.guilds:
        for role in guild.roles:
            if "Support Team" in str(role):
                y = y + 1
    if y == 0:
        await guild.create_role(name="Support Team")
    x = 0
    for guild in client.guilds:
        for category in guild.categories:
            if "tickets" in str(category):
                x = x + 1
                tickets_category = category
    if x == 0:
        tickets_category = await ctx.guild.create_category("tickets")
    author = ctx.author.name.replace(" ", "-")
    author = author.lower()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if "ticket-"+author in channel.name:
                 embed.description= 'You already made a ticket!'
                 return
    admin_role = get(guild.roles, name="Support Team")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(send_messages=True,read_messages=True),
        admin_role: discord.PermissionOverwrite(send_messages=True,read_messages=True)
    }
    ticket_channel = await ctx.guild.create_text_channel(name="ticket-"+author, topic=content, overwrites=overwrites, nsfw=None, category=tickets_category, slowmode_delay=None,position=None)
    embed.description= "You successfully created a ticket! in <#"+str(ticket_channel.id)+">"
    await ctx.send(embed=embed)

    embed.description= "**New ticket**\n\n<@"+str(ctx.author.id)+"> Opened ticket with reason "+str(content)
    await ticket_channel.send(embed=embed)

@ticket.error
async def ticket_error(ctx, error):
    embed = discord.Embed(colour=discord.Colour.red())
    if isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name=':x: **Ticket Error**\n', value=' ㅤ\n``.ticket {Reason/Subject}``', inline=False)
        embed.set_footer(text='© TECHGUIN')

        await ctx.send(embed=embed)

# Close a ticket

@client.command()
async def close(ctx):
    channel_id = ctx.channel.id
    channel = client.get_channel(channel_id)
    if "ticket" in channel.name:
        await ctx.send("Are you sure that you want to close the ticket?\ny or yes to close or write any other message to stay it open")
        msg = await client.wait_for('message', timeout=30)
        if msg.content == "yes" or msg.content == "y":
            await ctx.send("closing")
            await channel.delete()
        else:
            await ctx.send("Np")







#rock paper scissors

@client.tree.command(name="rps", description="Play rock paper scissors against the bot")
async def rps(interaction: discord.Interaction):
    rpsGame = ['rock', 'paper', 'scissors']
    await interaction.response.send_message("Rock, paper, or scissors? Choose wisely...")

    def check(message):
        return message.author == interaction.user and message.content.lower() in rpsGame

    try:
        user_choice_msg = await client.wait_for('message', check=check, timeout=30)
        user_choice = user_choice_msg.content.lower()

        comp_choice = random.choice(rpsGame)

        if user_choice == comp_choice:
            await interaction.followup.send(f"Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        elif (user_choice == 'rock' and comp_choice == 'paper') or \
             (user_choice == 'paper' and comp_choice == 'scissors') or \
             (user_choice == 'scissors' and comp_choice == 'rock'):
            await interaction.followup.send(f"Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        else:
            await interaction.followup.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")
    except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond.")




















# Cat
@client.tree.command(name="cat", description="shows a cute uwu cat for you")
async def cat(interaction: discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.green(), title="""Here's a cat""")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
            res = await r.json()
            image_url = res[0]['url']
            embed.set_image(url=image_url)

            await interaction.response.send_message(embed=embed)


# Meme

@client.tree.command(name="meme", description="shows a random meme")
async def meme(interaction: discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.green(), title="""Here's a meme bro from Kian""")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])

            await interaction.response.send_message(embed=embed)
    ephemeral=True




#dog

@client.tree.command(name="dog", description="Shows a random doggy woggy")
async def dog(interaction: discord.Interaction):
    embed = discord.Embed(colour=discord.Colour.green(), title="Here's a skibidi dog in Ohio")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/SillyDogs/random.json') as r:
            res = await r.json()
            # Ensure that the fetched data is an image
            if 'url' in res[0]['data']['children'][0]['data']:
                embed.set_image(url=res[0]['data']['children'][0]['data']['url'])
            else:
                embed.description = "Sorry, couldn't find a dog image this time."

            # Send the embed to the channel where the interaction occurred
            channel = await client.fetch_channel(interaction.channel_id)
            await channel.send(embed=embed)

            # Respond to the interaction with a message mentioning the user who triggered the command
            await interaction.response.send_message(f"You want a dog you say {interaction.user.mention}, well here you go", ephemeral=True)



















@client.tree.command(name="hello", description= "makes the bot say hello to you") 
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! How are you doing? ")
    ephemeral=True




@client.tree.command(name="ohiobeach", description= "Ohio beach") 
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("the skibidi beach in ohio is crazy ")
    ephemeral=True


@client.tree.command()
async def poop(ctx):
    await ctx.send("Kian and finatic is a silly goose")

@client.tree.command(name="tos", description="Tells you the terms of service")
async def tos(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.com/terms")

@client.tree.command(name="kian", description="Ask Kian your fate y/n")
async def kian(interaction: discord.Interaction, *, question: str):
    # Read random responses from the file
    with open("Discordbot/response.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    
    # Send the response to the user
    await interaction.response.send_message(f"Question: {question}\nKian's y/n response: {response}")



@client.tree.command(name="colour", description= "Says a random colour")
async def color(interaction: discord.Interaction):
    responses = ['red',
                 'blue',
                 'green',
                 'purple',
                 'pink',
                 'black']
    await interaction.response.send_message(f'Color: {random.choice(responses)}')
    ephemeral=True


@client.tree.command(name="ohio", description= "Says something random about Ohio!")
async def color(interaction: discord.Interaction):
    responses = ['Skibidi Rizz in Ohio',
                 'The ohio zoo has all the animals roaming',
                 'Down in ohio, Swag like Ohio',
                 'All the girls got GYATT in ohio, for real',
                 'SKIBIDI TOILET WAR IS ACTIVE THERE',
                 'There is SUPER MARIO ROAMING',
                 'Ohio is in the matrix or in upside down land']
    await interaction.response.send_message(f'OHIO: {random.choice(responses)}')
    ephemeral=True


@client.tree.command(name="unicorn", description="Tells you the unicorn process")
async def unicorn(interaction: discord.Interaction):
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        # Prompt for the first word
        await interaction.response.send_message("Please enter the first word:")

        msg1 = await client.wait_for('message', check=check, timeout=30.0)
        word1 = msg1.content
        await interaction.followup.send(f"Pink fluffy unicorns dancing on: {word1} ...")

        # Prompt for the second word
        await interaction.followup.send("Please enter the second word:")

        msg2 = await client.wait_for('message', check=check, timeout=30.0)
        word2 = msg2.content
        await interaction.followup.send(f"Pink fluffy unicorns dancing on: {word1} {word2} ...")

        # Prompt for the third word
        await interaction.followup.send("Please enter the third word:")

        msg3 = await client.wait_for('message', check=check, timeout=30.0)
        word3 = msg3.content
        await interaction.followup.send(f"Pink fluffy unicorns dancing on: {word1} {word2} celebrate failing, {word3} ...")

        # Prompt for the fourth word
        await interaction.followup.send("Please enter the fourth word:")

        msg4 = await client.wait_for('message', check=check, timeout=30.0)
        word4 = msg4.content
        await interaction.followup.send(f"Pink fluffy unicorns dancing on: {word1} {word2} celebrate failing, pink fluffy unicorns dancing on {word3} {word4} was very difficult")

    except asyncio.TimeoutError:
        await interaction.followup.send("Sorry, you took too long to respond. Please try again.")



client.run("Input token")
























