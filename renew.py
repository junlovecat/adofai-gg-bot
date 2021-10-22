import discord
from discord.ext import commands
from getdatafrom import getvalue
from identifier import returnthing
from discord.ext import tasks
import datetime
import os
import download
import math
#download.download("http://docs.google.com/spreadsheets/d/1PzLHfWmVWJHrBGnNSsLTsdH0ibdk0hB4MpKHET1nkpU/export?format=xlsx&id=1PzLHfWmVWJHrBGnNSsLTsdH0ibdk0hB4MpKHET1nkpU")
alist=getvalue()
ids=returnthing(alist,0)
names=returnthing(alist,1)
artists=returnthing(alist,2)
diffs=returnthing(alist,3)
creators=returnthing(alist,4)
ews=returnthing(alist,8)
bpms=returnthing(alist,9)
tiles=returnthing(alist,10)
tag1s=returnthing(alist,11)
tag2s=returnthing(alist,12)
tag3s=returnthing(alist,13)
tag4s=returnthing(alist,14)
tag5s=returnthing(alist,15)
client=commands.Bot(help_command=None,command_prefix='!')
directory=os.path.dirname(__file__)
agreement = discord.File(directory+"\\agreement.txt")

@client.event
async def on_ready():
    print('online and ready')
    change_status.start()

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hello! Before the start, the admin of this server should read the terms of agreement.')
            await channel.send(file=agreement)
        break
@client.event
async def on_command_error(ctx,error):
    await ctx.send('Error found!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('The permission is missing!')
    elif isinstance(error,commands.BotMissingPermissions) or isinstance(error,commands.BotMissingAnyRole) or isinstance(error,commands.BotMissingRole):
        await ctx.send('The bot has missing permissions!')
        embed = discord.Embed(title="Link", url="https://discord.com/api/oauth2/authorize?client_id=890455929030598716&permissions=8&scope=bot", 
        description="Click this link to invite to your server!", 
        color=discord.Color.blue())
        await ctx.send(embed=embed)
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send('No command found!')
    elif isinstance(error,commands.BadArgument):
        await ctx.send('Wrond argument!')
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('Missing argument!')
    else:
        await ctx.send(f'Please show this error to JUN#5661: {str(error)}')
@tasks.loop(seconds=10)
async def change_status():
    activity=discord.Game(name=datetime.datetime.today().strftime('%Y-%m-%d'))
    await client.change_presence(status=discord.Status.idle, activity=activity)

#@client.command()

@client.command()
async def find(ctx,query:str):
    embed=discord.Embed(
        title='list',
        description='found some of it',
        color=discord.Color.dark_red()
    )
    added=False
    counter=0
    embedlist=[]
    for x in range(len(names)):
        if str(query.lower())==str(str(names[x]).lower()):
            counter+=1
            embedlist.append([str(ids[x]),str(names[x])])
            added=True
    if not added:await ctx.send('Nothing found')
    else:
        for x in range(len(embedlist)):
            embed.add_field(name=f'id: {embedlist[x][0]}',value=embedlist[x][1],inline=False)
        await ctx.send(embed=embed)

@client.command()
async def id(ctx,id:int):
    await ctx.send('let me think...')
    legacyid=id
    found=False
    for x in range(len(ids)):
        if ids[x]==id:
            id=x
            found=True
            break
    if not found:
        await ctx.send('Not Found')
    else:
        embed=discord.Embed(
            title='id: '+str(legacyid),
            description='E.W. means : level can occur Photosensitive Epilepsy',
            color=discord.Color.dark_gold()
        )
        name=names[id]
        artist=artists[id]
        difficulty=diffs[id]
        creator=creators[id]
        ew=ews[id]
        bpm=bpms[id]
        tile=tiles[id]
        tag1=tag1s[id]
        tag2=tag2s[id]
        tag3=tag3s[id]
        tag4=tag4s[id]
        tag5=tag5s[id]
        embed.add_field(name='name: ',value=name,inline=True)
        embed.add_field(name='artist: ',value=artist,inline=True)
        embed.add_field(name='level: ',value=difficulty,inline=True)
        embed.add_field(name='maker: ',value=creator,inline=True)
        embed.add_field(name='E.W.: ',value=ew,inline=True)
        embed.add_field(name='BPM: ',value=bpm,inline=True)
        embed.add_field(name='tiles: ',value=tile,inline=True)
        if(tag1):
            if(tag2):
                if(tag3):
                    if(tag4):
                        if(tag5):embed.add_field(name='tag: ',value=f'{tag1}, {tag2}, {tag3}, {tag4}, {tag5}',inline=True)
                        else:embed.add_field(name='tag: ',value=f'{tag1}, {tag2}, {tag3}, {tag4}',inline=True)
                    else:embed.add_field(name='tag: ',value=f'{tag1}, {tag2}, {tag3}',inline=True)
                else:embed.add_field(name='tag: ',value=f'{tag1}, {tag2}',inline=True)
            else:embed.add_field(name='tag: ',value=f'{tag1}',inline=True)
        else:embed.add_field(name='tag: ',value='None',inline=True)
        await ctx.channel.purge(limit=2)
        message=await ctx.send(embed=embed)

def min(a,b):
    if a<b:
        return a
    elif a>b:
        return b
    else:
        return a

@client.command()
async def calculatepp(ctx,id:int,realacc:float,realpitch:float):
    pitch=realpitch/100
    difficulty=float(diffs[id])
    tile=int(tiles[id])
    acc=(realacc)/(100+0.01*tile)
    levelbasicrate=float(1600/(1+math.exp(-0.42*float(difficulty)+7.4)))
    accrate=float(0.013/(acc*(-1)+1.0125)+0.2)
    pitchrate=float(math.pow(
        ((1+pitch))/2,
        (min((0.1+math.pow(tile,0.5)/(math.pow(2000,0.5))),1.1))
    )) if pitch>=1 else math.pow(pitch,1.8)
    tilerate=float(0.84+tile/12500 if tile>2000 else math.pow((tile/2000),0.1))
    pp=math.pow(float(levelbasicrate*accrate*pitchrate*tilerate),1.01)
    embed=discord.Embed(
        title='Total Rate',
        description='This rate is from ADOFAI.GG',
        color=discord.Color.dark_blue()
    )
    embed.add_field(name='Rating by difficulty',value=str(levelbasicrate),inline=False)
    embed.add_field(name='Magnification by Accuracy',value=str(accrate),inline=False)
    embed.add_field(name='Magnification by Pitch',value=str(pitchrate),inline=False)
    embed.add_field(name='Magnification by tile',value=str(tilerate),inline=False)
    embed.add_field(name='Total PP',value=str(pp),inline=False)
    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title="Link", url="https://discord.com/api/oauth2/authorize?client_id=890455929030598716&permissions=8&scope=bot", 
    description="Click this link to invite to your server!", 
    color=discord.Color.blue())
    await ctx.send(embed=embed)
client.run('ODkwNDU1OTI5MDMwNTk4NzE2.YUwDtQ.ypjIQNM66uVj9SsZlZ7rwgKsYq8')
#https://discord.com/api/oauth2/authorize?client_id=890455929030598716&permissions=8&scope=bot