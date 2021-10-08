import discord, random, aiohttp
from discord import message
from discord.ext import commands


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='.help'))
    print('Bot Online!')

@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title='', description='')

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command()
async def hug(ctx, *, member):
    author_name = ctx.message.author.name
    await ctx.send(f'{author_name} has hugged {member}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', '8Ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]
    await ctx.send(f'`Question:` {question}\n `Answer:` {random.choice(responses)}')

@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} was kicked.\n Reason: {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} was banned.\n Reason: {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member ):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entery in banned_users:
        user = ban_entery.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'User {user.name}#{user.discriminator} unbanned')
            return

@client.command()
async def dm(ctx, member: discord.Member, *, content):
    author = ctx.message.author.name
    guild = ctx.message.guild.name
    channel = await member.create_dm()
    await channel.send(f'`Server |` **{guild}** \n `User |` **{author}** \n `Message |` **{content}**')

client.run('TOKEN')
