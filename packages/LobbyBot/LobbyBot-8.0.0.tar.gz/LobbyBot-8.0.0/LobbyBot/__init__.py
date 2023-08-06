"""
Hello Skids,
Today is Your Lucky Day!

I will Let You Take Whatever You want from This Code.
If You Want To Know How i Made Any of The Functions
Or How You Can implement Them Into Your Script
Just Join The Discord and Message anyone with The Highest Role!
https://discord.gg/VHtvszBAx3

P.S I dont Recommend You Skidding!
Its a bad crime and can get you into serious trouble.
You Should Only Skid My Projects Since I allow People Todo So!

People Spend Hours Coding These Scripts Just For You!
Not To Steal The Code But For You To Use The Service.
I Spent Alot Of Time On This Bot So if You Could Support Me I would appreciate it!
    - Pirxcy
""" 
import fortnitepy
import traceback
import sanic
import logging
import random
import string
import PirxcyPinger
import crayons
import json
import sys
import os
import asyncio
import aiohttp

from fortnitepy.ext import commands
from sanic import Sanic


def cyan(string):
  output = crayons.cyan(string)
  return str(output)

def red(string):
  output = crayons.red(string)
  return str(output)

def green(string):
  output = crayons.green(string)
  return str(output)

app = Sanic("pb4")
loop = asyncio.get_event_loop()

code = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(cyan('[PirxcyBot] [%(asctime)s] [%(levelname)s] - %(message)s'))
ch.setFormatter(formatter)
logger.addHandler(ch)

def clear():
  os.system('cls || clear')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

@app.route("/")
async def index(request):
  return sanic.response.html(
  """
<html>
   <head>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
      <style>
         body {
         font-family:sans-serif;
         position: absolute;
         left: 50%;
         top: 50%;  
         -webkit-transform: translate(-50%, -50%);
         transform: translate(-50%, -50%);
         background-repeat: no-repeat;
         background-attachment:local;
         background-size: cover;
         background-color: #87CEEB;
         color: #f1f1f1;
         }
      </style>
      <style type="text/css">
        @font-face {
            font-family: "fn";
            src: url(https://devboogiefncf.n-dev.repl.co/Burbank.otf) format("truetype");
        }
        .font { 
            font-family: "fn", Verdana, Tahoma;
            font-size: 100px;
        }
        </style>
   </head>
   <body>
      <center>
            <h2 class="font">
""" +
f"""
            Client Logged in as {bot.user.display_name}
            <h2>
              <button onclick="location.href='/dash';" class="btn btn btn-outline-light  btn-lg">
                Dashboard
              </button>
            </h2>
         </h2>
      </center>
   </body>
</html>
  """
  )

@app.route(
  "/dash",
  methods=[
    "GET",
    "POST",
  ]
)
async def dashboard(request):
  method = request.method
  config = open_config()
  if method == "GET":
    user = await bot.fetch_profile(
      user=config['owner'],
      cache=True
    )
    displayName = user.display_name
    global code
    code = str(id_generator(size=4))
    return sanic.response.html(
      """
<html>
   <head>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
      <style>
         body {
         font-family:sans-serif;
         position:fixed;
         left: 50%;
         top: 50%;  
         -webkit-transform: translate(-50%, -50%);
         transform: translate(-50%, -50%);
         background-repeat: no-repeat;
         background-attachment:local;
         background-size: cover;
         background-color: #87CEEB;
         color: #f1f1f1;
         }
      </style>
      <style type="text/css">
        @font-face {
            font-family: "fn";
            src: url(https://devboogiefncf.n-dev.repl.co/Burbank.otf) format("truetype");
        }
        .ptitle {
            font-family: Arial, sans-serif;
            font-size: 50px;
        }
        .font { 
            font-family: "fn", Verdana, Tahoma;
            font-size: 75px;
        }
        .fontn{ 
         font-family: "fn", Verdana, Tahoma;
         color: black;
         font-size: 75px
         }
         .fontf{ 
            font-family: "fn", Verdana, Tahoma;
            color: black;
            }
        </style>
   </head>
   <body>
   """ +
   f"""
      <center>
         <h2 class = "ptitle">
            Whisper <span class="font">{bot.user.display_name}</span> The Following Command:<br>"!verify <span class="fontn">{code}</span>"
         </h2>
         <h2 class>
            Make sure your using the admin account (<span class="fontf">{displayName}</span>)<br>
            Dont Message the quotation marks or it wont work.<br>
            This is in beta dont expect this shit to work
         </h2>
      </center>
   </body>
</html>
      """
    )
  elif method == "POST":
    return sanic.response.html()
  return sanic.response.json({"error": "Invalid Request Method"})

async def get_items():
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="GET",
      url="https://fortnite-api.com/v2/cosmetics/br/"
      ) as r:
      items = await r.json()
  items = items['data']
  file = open(
    "items.json", 
    "w"
  )
  json.dump(items, file, indent=2)
  file.close()
  logger.info(green('Cached All bot Items'))
  return

async def get_settings():
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="GET",
      url="https://lobbybotconfiguration.pirxcy1942.repl.co/blacklist"
      ) as r:
          main = await r.json()
  return main

async def post_blacklist(id):
  blacklist = await get_settings()
  blacklist['blocked_names'].append(id)
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",
      url="https://lobbybotconfiguration.pirxcy1942.repl.co/blacklist",
      json=(blacklist)
      ) as r:
      return

def open_config():
  with open('config.json') as f:
    try:
      data = json.load(f)
      return data
    except json.decoder.JSONDecodeError:
      print("An Json Decode Error Occured While Reading config.json (Contact Pirxcy for Help)")
      sys.exit()
    except FileNotFoundError:
      pass

def is_admin():
  async def predicate(ctx):
    config = open_config()
    try:
      settings = await get_settings()
      owners = [i for i in settings['whitelist_id']]
    except:
      owners = []
    owners.append(config['owner'])
    return str(ctx.author.id) in owners
  return commands.check(predicate)

def load_cosmetics():
  with open('items.json') as f:
    try:
      data = json.load(f)
      return data
    except json.decoder.JSONDecodeError:
      print("An Json Decode Error Occured While Reading items.json (Contact Pirxcy for Help)")
      sys.exit()

clear()


async def code_to_auths():
  response = input('Enter A Valid Authorization Code: ')
  clear()
  try:
    url = PirxcyPinger.get_url(platform='replit')
  except:
    logger.warning(red('Invalid Platform Please Use on Replit!'))

  if "redirectUrl" in response:
    response = json.loads(response)
    if "?code" not in response["redirectUrl"]:
      print('You Have Entered An Invalid Authorization Code!')
      sys.exit()
    code = response["redirectUrl"].split("?code=")[1]
  else:
    if "https://accounts.epicgames.com/fnauth" in response:
      if "?code" not in response:
        print('You Have Entered An Invalid Authorization Code!')
        sys.exit()
      code = response.split("?code=")[1]
    else:
      code = response
  logger.info('Proceeding To Generate Auths!')
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",
      url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
      data=f"grant_type=authorization_code&code={code}",
      headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
      }
      ) as r:
      data_ = await r.text()
      data = json.loads(data_)
  async with aiohttp.ClientSession() as session:
    async with session.request(
      method="POST",            
      url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}/deviceAuth",
      headers={
        "Authorization": f"Bearer {data['access_token']}",
        "Content-Type": "application/json"
      }
    ) as r:
      data2 = await r.text()
      auths = json.loads(data2)
    auths['created'].pop('ipAddress')
    with open("config.json") as f:
      old = json.load(f)
    
    with open(
      "config.json",
      "w"
    ) as new:
      old['auths'].update(auths)
      json.dump(
        old,
        new,
        indent=2
      )

    logger.info(green('Generated Auths!'))
    return auths

tempc = open_config()
if tempc.get("auths") and tempc['auths'].get("secret"):
  auths = tempc['auths']
else:
  auths = loop.run_until_complete(code_to_auths())

bot = commands.Bot(
  command_prefix="!",
  case_insensitive=True,
  auth=fortnitepy.DeviceAuth(
    device_id=auths['deviceId'],
    account_id=auths['accountId'],
    secret=auths['secret']                                                              
  )
)

@bot.event
async def event_party_invite(invite):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if invite.sender.id in owners:
    try:
      await invite.accept()
    except Exception:
      pass
  else:
    await invite.decline()

server = None

@bot.event
async def event_ready() -> None:
  global server
  config = open_config()
  if config['owner'] == "":
    logger.warning(red('You Haven\'t Filled Out The Config! (Expect Errors To Occur)'))
  user = await bot.fetch_profile(config['owner'])
  if user.id in bot.friends:
    friend = bot.get_friend(user.id)
    try:
      await friend.join_party()
    except:
      await friend.invite()
  else:
    try:
      await bot.unblock_user(user.id)
    except:
      pass
    await bot.add_friend(user.id)
    logger.info(green(f"Added {user.display_name} {red('(ADMIN)')}"))
  await get_items()
  await bot.set_presence(config['status']) 
  clear()
  logger.info(green(f'Launched {bot.user.display_name}'))
  try:
    await PirxcyPinger.post(f"https://{os.environ['REPL_ID']}.id.repl.co")
    logger.info(green('Uploaded URL To PirxcyPinger!'))
  except PirxcyPinger.AlreadyPinging: #if url is already submitted
    logger.warning('Already Pinging URL!')
  except:
    pass
  logger.info('Starting Server')
  log = logging.getLogger('werkzeug')
  log.disabled = True
  coro = app.create_server(
    host=run_ip,
    port=run_port,
    return_asyncio_server=True,
    debug=False,
    access_log=False
  )
  try:
    server = await coro
  except Exception as e:
    logger.error(red(f'Error Starting Server {e}'))

@bot.event
async def event_party_member_join(member):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if member.id in owners:
    logger.info(red(f'{member.display_name} (An Admin) Has Joined!'))
    await member.promote()
    await bot.party.send(config['join_message'])
    await bot.party.send("An Admin of This Bot Has Joined!")
  elif member.display_name in settings['blocked_names'] or member.id in settings['blocked_names']:
    await post_blacklist(id=member.display_name)
    await member.block()
    await member.kick()
  else:
    logger.info(f'{member.display_name} Has Joined!')
    await bot.party.send(f"{config['join_message']}\nMade By Pirxcy")
    
@bot.event
async def event_friend_request(request):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if request.sender.id in owners:
    await request.accept()
    await request.sender.invite()

@bot.event
async def event_friend_add(friend):
  await friend.invite()

@bot.event
async def event_friend_remove(friend):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if friend.id in owners:
    await friend.add_friend()

@bot.event
async def event_friend_message(message):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if message.author.display_name in settings['blocked_names'] or message.author.id in settings['blocked_names']:
    await message.author.block()
    await message.author.kick()
    logger.warning(red(f'Blocked/Kicked {message.author.display_name}'))
  elif any(word.lower() in message.content.lower() for word in settings['blacklist_keywords']):
    await post_blacklist(id=message.author.id)
    await message.author.block()
    logger.warning(red(f'Added {message.author.display_name} to the blacklist!'))
  else:
    if str(message.author.id) in owners:
      logger.info(green(f'[{message.author.display_name} {red("ADMIN")}] {message.content}'))
    else:
      logger.info(green(f'[{message.author.display_name}] {message.content}'))

@bot.event
async def event_party_message(message):
  config = open_config()
  try:
    settings = await get_settings()
    owners = [i for i in settings['whitelist_id']]
  except:
    owners = []
  owners.append(config['owner'])
  if message.author.display_name in settings['blocked_names'] or message.author.id in settings['blocked_names']:
    await message.author.block()
    await message.author.kick()
    logger.warning(red(f'Blocked/Kicked {message.author.display_name}'))
  elif any(word.lower() in message.content.lower() for word in settings['blacklist_keywords']):
    await post_blacklist(id=message.author.display_name)
    await message.author.block()
    await message.author.kick()
    logger.warning(red(f'Added {message.author.display_name} to the blacklist!'))
  else:
    if str(message.author.id) in owners:
      logger.info(green(f'[{message.author.display_name} {red("ADMIN")}] {message.content}'))
    else:
      logger.info(green(f'[{message.author.display_name}] {message.content}'))

@bot.command()
async def hello(ctx):
  await ctx.send('Hello!')

@bot.command()
async def skin(ctx, *, content = None):
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !skin ikonik')    
    elif content.upper().startswith('CID_'):
      await bot.party.me.set_outfit(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('CID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

      if result == []:
        await ctx.send('No Result Found')      

      elif len(result) == 1:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await bot.party.me.set_outfit(asset=result[0]['id'])                    
        skinname = result[0]['name']
        await ctx.send(f"Equiped {skinname}")                
        del result[0]

      else:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await ctx.send(
          f"Result For {content}\n"
          +
          "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
        )
        def check(m): 
          return m.author.id == ctx.author.id
        msg = await bot.wait_for("party_message", check=check)
        await bot.party.me.set_outfit(asset=result[int(msg.content)]['id'])
        skinname = result[int(msg.content)]['name']
        await ctx.send(f'Equiped {skinname}')
        del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

@bot.command()
async def emote(ctx, *, content = None):
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !emote scenario')    
    elif content.upper().startswith('EID_'):
      await bot.party.me.set_emote(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('EID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

      if not result:
        await ctx.send('No Result Found')
        return    

      elif len(result) == 1:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await bot.party.me.set_emote(asset=result[0]['id'])                    
        skinname = result[0]['name']
        await ctx.send(f"Equiped {skinname}")                
        del result[0]
        return

      else:
        result = sorted(result, key=lambda x:x['name'], reverse=False)
        await ctx.send(
          f"Result For {content}\n"
          +
          "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
        )
        def check(msg): 
          return msg.author == ctx.author
        
        msg = await bot.wait_for("party_message", check=check)                  
        await bot.party.me.set_emote(asset=result[int(msg.content)]['id'])
        skinname = result[int(msg.content)]['name']
        await ctx.send(f'Equiped {skinname}')
        del result[int(msg.content)]
        return
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')
  
@bot.command()
async def backpack(ctx, *, content = None):
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !backpack black shield')    
    elif content.upper().startswith('BID_'):
      await bot.party.me.set_backpack(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('BID_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

        if not result:
          await ctx.send('No Result Found')      

        elif len(result) == 1:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await bot.party.me.set_backpack(asset=result[0]['id'])                    
          skinname = result[0]['name']
          await ctx.send(f"Equiped {skinname}")                
          del result[0]

        else:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await ctx.send(
            f"Result For {content}\n"
            +
            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
          )
          def check(msg): 
            return msg.author == ctx.author
          
          msg = await bot.wait_for("party_message", check=check)                  
          await bot.party.me.set_backpack(asset=result[int(msg.content)]['id'])
          skinname = result[int(msg.content)]['name']
          await ctx.send(f'Equiped {skinname}')
          del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

@bot.command()
async def pickaxe(ctx, *, content = None):
  try:
    cosmetics = load_cosmetics()
    if content is None:
      await ctx.send('Try !backpack black shield')    
    elif content.upper().startswith('Pickaxe_'):
      await bot.party.me.set_pickaxe(asset=content)
      await ctx.send(f"Equiped {content}")
    else:
      result = []
      await ctx.send('Searching...')
      for i in cosmetics:
        if content.lower() in i['name'].lower() and i['id'].startswith('Pickaxe_'):
          result.append(
            {
              'name': i['name'],
              'id': i['id']
            }
          )
          if len(result) == 11:
            break

        if not result:
          await ctx.send('No Result Found')      

        elif len(result) == 1:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await bot.party.me.set_pickaxe(asset=result[0]['id'])                    
          skinname = result[0]['name']
          await ctx.send(f"Equiped {skinname}")                
          del result[0]

        else:
          result = sorted(result, key=lambda x:x['name'], reverse=False)
          await ctx.send(
            f"Result For {content}\n"
            +
            "\n".join([f"{num}. {i}" for num, i in enumerate([f['name'] for f in result])]) 
          )
          def check(msg): 
            return msg.author == ctx.author and msg.content
          
          msg = await bot.wait_for("party_message", check=check)                  
          await bot.party.me.set_pickaxe(asset=result[int(msg.content)]['id'])
          skinname = result[int(msg.content)]['name']
          await ctx.send(f'Equiped {skinname}')
          del result[int(msg.content)]
  except Exception as e:
    await ctx.send(f'{traceback.format_exc()}\n{e}')

#most commands below are stolen from xensis all credits to him
#i have modified most of these commands

@bot.command()
async def pinkghoul(ctx):
  await bot.party.me.set_outfit(
    asset='CID_029_Athena_Commando_F_Halloween',
    variants=bot.party.me.create_variants(
      material=3
    )
  )
  await ctx.send('Equiped Pink Ghoul Trooper')

@bot.command()
async def checkeredrenegade(ctx):
  logger.info(f'{ctx.author} Excecuted checkeredrenegade')
  await bot.party.me.set_outfit(
    asset='CID_028_Athena_Commando_F',
    variants=bot.party.me.create_variants(
      material=2
    )
  )
  await ctx.send('Equiped Checkered Renegade Raider')

@bot.command()
async def purpleportal(ctx):
  await bot.party.me.set_backpack(
    asset='BID_105_GhostPortal',
    variants=bot.party.me.create_variants(
      item='AthenaBackpack',
      particle_config='Particle',
      particle=1
    )
  )
  await ctx.send('Equiped Purple Ghost Portal')

@bot.command()
async def purpleskull(ctx):
  logger.info(f'{ctx.author} Excecuted purpleskull')
  await bot.party.me.set_outfit(
    asset='CID_030_Athena_Commando_M_Halloween',
    variants=bot.party.me.create_variants(
      clothing_color=1
    )
  )
  await ctx.send('Equiped Purple Skull Trooper')

@bot.command()
async def goldpeely(ctx):
  await bot.party.me.set_outfit(
    asset='CID_701_Athena_Commando_M_BananaAgent',
    variants=bot.party.me.create_variants(
      progressive=4
    ),
    enlightenment=(
      2, 
      350
    )
  )
  await ctx.send('Equiped Gold Peely')

@bot.command()
async def hatlessrecon(ctx):
  logger.info(f'{ctx.author} Excecuted hatlessrecon')
  await bot.party.me.set_outfit(
    asset='CID_022_Athena_Commando_F',
    variants=bot.party.me.create_variants(
      parts=2
    )
  )
  await ctx.send('Equiped Hatless recon')

@bot.command()
async def hologram(ctx):
  await bot.party.me.set_outfit(
    asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
  )
  await ctx.send('Equiped hologram')

@bot.command()
async def ready(ctx):
  logger.info(f'{ctx.author} Excecuted ready')
  await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
  await ctx.send('Bot is Ready!')

@bot.command()
async def unready(ctx):
  await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
  await ctx.send('Bot is Unready!')

@bot.command()
async def sitin(ctx):
  logger.info(f'{ctx.author} Excecuted sitin')
  await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
  await ctx.send('Sitting in')

@bot.command()
async def sitout(ctx):
  await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
  await ctx.send('Sitting out')

@bot.command()
async def tier(ctx, tier = None):
  if tier is None:
    await ctx.send('Try !tier 1942') 
  else:
    await bot.party.me.set_battlepass_info(
      has_purchased=True,
      level=tier
    )
  await ctx.send(f'Set tier to {tier}')

@bot.command()
async def level(ctx, level = None):
  if level is None:
    await ctx.send(f'Try !level 1942')
  else:
    await bot.party.me.set_banner(season_level=level)
    await ctx.send(f'Set level to {level}')

@bot.command()
@is_admin()
async def verify(
  ctx,
  guess=None
):
  if not guess:
    return await ctx.send("No Code Entered!")
  elif not code:
    return await ctx.send(f"Visit {PirxcyPinger.get_url(platform='replit')}/dash first!")
  elif guess.lower() == code.lower():
    await ctx.send("Welcome Back, SHlT BOUTTA GO DOWN\n Check your web page")





@bot.command()
@is_admin()
async def say(ctx, *, message = None):
  logger.info(f'{ctx.author} Excecuted say')
  if message is not None:
    await bot.party.send(message)
    await ctx.send(f'Message Sent.')
  else:
    await ctx.send(f'Try !say Hi')

@bot.command()
@is_admin()
async def status(ctx, *, status = None):
  if status is None:
    await ctx.send('Try !status 1942')
  else:
    await bot.set_presence(status) 
    await ctx.send(f'Status set')

@bot.command()
@is_admin()
async def leave(ctx):
  await ctx.send('Bye.')
  await bot.party.me.set_emote(asset='EID_Wave')
  await asyncio.sleep(1.5)
  await bot.party.me.leave()

@bot.command()
@is_admin()
async def join(ctx, *, member = None):
  try:
    if member is None:
      user = await bot.fetch_profile(ctx.message.author.id)
      friend = bot.get_friend(user.id)
    elif member is not None:
      user = await bot.fetch_profile(member)
      friend = bot.get_friend(user.id)
      await friend.join_party()
      await ctx.send(f"Joined {friend.display_name}")
  except fortnitepy.Forbidden:
      await ctx.send("Party is Private :(")
  except fortnitepy.PartyError:
      await ctx.send("That user is already here.")
  except fortnitepy.HTTPException:
      await ctx.send("An Unknown Error Occured")
  except AttributeError:
      await ctx.send("I can not join that party. Are you sure I have them friended?")



def run(ip = str, port = int):

  global run_ip
  global run_port
  run_ip = ip
  run_port = port
  bot.run()



#remove this when compiling

run(
  ip="127.0.0.1",
  port=8000
)
