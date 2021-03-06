import discord
from captcha.image import ImageCaptcha
import random
import asyncio
import datetime
import time
import os

client = discord.Client()
gaming = '채원 인증'

@client.event
async def on_ready():
    print("인증 봇이 정상적으로 실행되었습니다.")
    game = discord.Game(gaming)
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith("채원 인증"):    # 채원 인증
        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author. id) + ".png"
        Captcha_img.write(a, name)

        await message.channel.send(f"""{message.author.mention} 아래 숫자를 15초 내에 입력해주세요. """)
        await message.channel.send(file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=15, check=check) # 제한시간 15초
        except:
            await message.channel.purge(limit=3)
            chrhkEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            chrhkEmbed.add_field(name='닉네임', value=message.author, inline=False)
            chrhkEmbed.add_field(name='이유', value='시간초과', inline=False)
            await message.channel.send(embed=chrhkEmbed)
            print(f'{message.author} 님이 시간초과로 인해 인증을 실패함.')
            return

        if msg.content == a:
            role = discord.utils.get(message.guild.roles, name="인증")   #역활
            await message.channel.purge(limit=4)
            tjdrhdEmbed = discord.Embed(title='인증성공', color=0x04FF00)
            tjdrhdEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tjdrhdEmbed.add_field(name='5초후 인증역할이 부여됩니다.', value='** **', inline=False)
            tjdrhdEmbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=tjdrhdEmbed)
            time.sleep(5)
            await message.author.add_roles(role)
        else:
            await message.channel.purge(limit=4)
            tlfvoEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            tlfvoEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tlfvoEmbed.add_field(name='이유', value='잘못된 숫자', inline=False)
            await message.channel.send(embed=tlfvoEmbed)
            print(f'{message.author} 님이 잘못된 숫자로 인해 인증을 실패함.')

@client.event
async def on_message(message):
    if message.guild is None:
        if message.author.bot:
            return
        else:
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=message.created_at)
            embed.add_field(name='전송자', value=message.author, inline=False)
            embed.add_field(name='내용', value=message.content, inline=False)
            embed.set_footer(text=f'!디엠 <@{message.author.id}> [할말] 을 통해 답장을 보내주세요!')
            await client.get_channel(819556608022413362).send(f"`{message.author.name}({message.author.id})`", embed=embed)

    if message.content.startswith('!디엠'):
        if message.author.guild_permissions.manage_messages:
            msg = message.content[26:]
            await message.mentions[0].send(f"{msg}")
            await message.channel.send(f'`{message.mentions[0]}`에게 DM을 보냈습니다')
        else:
            return
        
access_token = os.environ["BOT_TOKEN"]     
client.run(access_token)


