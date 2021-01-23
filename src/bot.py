import discord
import random
from discord.ext import commands
from itertools import cycle

client = commands.Bot(command_prefix = '/')
client.remove_command('help')
token = "enter your token between these quotes"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Minecraft'))
    print('Bot online!')

your_server = 'the location of his super suit'
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    await member.send(f'Welcome to {your_server}!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='/ping', value='Returns Pong!', inline=False)
    embed.add_field(name='/8ball [enter question here]', value='Answers Your Question!', inline=False)
    embed.add_field(name='/clear [enter number of messages here]', value='Clears The Amount Of Messages Entered', inline=False)
    embed.add_field(name='/kick [enter user here]', value='Kicks The User You Entered!', inline=False)
    embed.add_field(name='/ban [enter user here]', value='Bans The User You Entered!', inline=False)
    embed.add_field(name='/unban', value='Unbans The User You Entered!', inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx):
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
    await ctx.send(f'{random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.send(f'You got kicked cuz\' {reason}')
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}\nReason: {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.send(f'You got banned cuz\' {reason}')
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}\nReason: {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.event
async def on_command_error(ctx, error):
    print(ctx.command.name + ' was invoked incorrectly.')
    print(error)

@client.event
async def on_command(ctx):
    if ctx.command is not None:
        if ctx.command.name in commands_tally:
            commands_tally[ctx.command.name] += 1
        else:
            commands_tally[ctx.command.name] =1
            print(commands_tally)

@client.event
async def on_command_completion(ctx):
    print(ctx.command.name + ' was invoked successfully.')

client.run(token)
