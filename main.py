import discord
from discord.ext import commands
import os
from os.path import join, dirname
from dotenv import load_dotenv
from keep_alive import keep_alive

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN=os.environ.get("DISCORD_TOKEN")
tag=os.environ.get("BOT_TAG")
role=os.environ.get("BOT_ROLE")
client = discord.Client()
ctx=tag
k=8

def numOfCommand():
  f = open("commands.txt", "r")
  Lines = f.readlines()
  count=1
  for line in Lines:
    count+=1
  f.close()
  return count

def removeCommand(command):
  pos=0
  for x in range(1,numOfCommand()):
    if getCommand(x).casefold()==command.casefold():
      pos=x
  if pos==0:
    return 0
  else:
    c=open("commands.txt","r")
    r=open("rep.txt","r")

    commandlines=c.readlines()
    replines=r.readlines()

    c=open("commands.txt","w")
    r=open("rep.txt","w")

    for x in range(0,len(commandlines)):
      if x!=pos-1:
        if pos==len(commandlines):
          if (x!=len(commandlines)-2):
            c.write(commandlines[x])
            r.write(replines[x])
          else:
            c.write(commandlines[x].strip("\n"))
            r.write(replines[x].strip("\n"))
        else:
          if (x!=len(commandlines)-1):
            c.write(commandlines[x])
            r.write(replines[x])
          else:
            c.write(commandlines[x].strip("\n"))
            r.write(replines[x].strip("\n"))
        
    
    c.close()
    r.close()
    return 1

  
def setCommandnRep(command, rep):
  for x in range(1,numOfCommand()):
    if getCommand(x).casefold()==command.casefold():
      if (x<numOfCommand()-1):
        r = open("rep.txt","r")
        allRep=r.readlines()
        allRep[x-1]=rep+" "+"\n"
      else:
        r = open("rep.txt","r")
        allRep=r.readlines()
        allRep[x-1]=rep+" "


      if x==numOfCommand():
        allRep[x-1]=allRep[x-1]+"\n"

      r=open("rep.txt","w")
      r.writelines(allRep)
      r.close()
      return

  c = open("commands.txt","a")
  r = open("rep.txt","a")

  c.writelines("\n"+command.casefold())
  r.writelines("\n"+rep+" ")

  r.close()
  c.close()
  return

def getCommand(n):
  f = open("commands.txt", "r")
  Lines = f.readlines()
  count=0
  command=""
  for line in Lines:
    count+=1
    if count == n:
      command=line.strip()
  f.close()
  return command

def numOfRep():
  f = open("rep.txt", "r")
  Lines = f.readlines()
  count=1
  for line in Lines:
    count+=1
  f.close()
  return count
  

def getRep(n):
  f = open("rep.txt", "r")
  Lines = f.readlines()
  count=0
  rep=""
  for line in Lines:
    count+=1
    if count == n:
      rep=line.strip()
  return rep

def embed(n,message):
  embed=discord.Embed(title="All commands of discord bot", description="Created by "+str(message.author.name), color=0xe58585)
  if k+n*k < numOfCommand():
    for x in range(1+n*k,k+n*k+1):
      embed.add_field(name=tag+getCommand(x), value=getRep(x)+"\n", inline=False)
  else:
    for x in range(1+n*k,numOfCommand()):
      embed.add_field(name=tag+getCommand(x), value=getRep(x)+"\n", inline=False)
  return embed

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for x in range(1,numOfCommand()):
      command=tag+getCommand(x).casefold()
      if message.content.casefold() == command:
        rep=getRep(x)
        await message.channel.send(rep)

    if message.content.casefold().split()[0] == tag+"commands":
      if len(message.content.casefold().split()) == 1 : 
        numOfPages=numOfCommand()
        numOfPages = numOfPages//k
        if numOfPages*k+1 < numOfCommand():
          numOfPages=numOfPages + 1
        
        n=0
        
        mess = await message.channel.send(embed=embed(0,message))
        await mess.add_reaction('⏮')
        await mess.add_reaction('◀')
        await mess.add_reaction('▶')
        await mess.add_reaction('⏭')

        reaction = None
        def check(reaction, user):
          return user == message.author

        while True:
            if str(reaction) == '⏮':
                n = 0
                await mess.edit(embed = embed(n,message))
            elif str(reaction) == '◀':
                if n > 0:
                    n -= 1
                    await mess.edit(embed = embed(n,message))
            elif str(reaction) == '▶':
                if n < numOfPages-1:
                    n += 1
                    await mess.edit(embed = embed(n,message))
            elif str(reaction) == '⏭':
                n = numOfPages-1
                await mess.edit(embed = embed(n,message))

        
            try:
              reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
              await mess.remove_reaction(reaction, user)
            except:
              break

        await mess.clear_reactions()

      if role in [y.name.lower() for y in message.author.roles]:
        if len(message.content.casefold().split()) > 2 :
          if(message.content.casefold().split()[1]!="commands" and message.content.casefold().split()[1]!="remove"):
            setCommandnRep(message.content.casefold().split()[1],message.content.split(' ', 1)[1].split(" ",1)[1])
            await message.channel.send("Add "+tag+message.content.casefold().split()[1]+" successful : D")
          else:
            await message.channel.send("!"+message.content.casefold().split()[1]+" is the system command. Dont try to fix :3")

    if role in [y.name.lower() for y in message.author.roles]:

      if message.content.casefold().split()[0] == tag+"remove":
        if len(message.content.casefold().split()) == 2 : 
          if(message.content.casefold().split()[1]!="commands" and message.content.casefold().split()[1]!="remove"):
            if removeCommand(message.content.casefold().split()[1]):
              await message.channel.send("Remove "+tag+message.content.casefold().split()[1]+" successful : D")
            else:
              await message.channel.send("Dont found "+tag+message.content.casefold().split()[1])
          else:
            await message.channel.send("!"+message.content.casefold().split()[1]+" is the system command. Dont try to fix :3")

keep_alive()
client.run(TOKEN)