import discord
from discord import Webhook
import requests
from PIL import Image
import os
import json
import random

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Choose the webhook
    webhooks = await message.channel.webhooks()
    webhook = next((x for x in webhooks if x.id == 1065757061285171361 ), None)

    with open("replies.json", "r") as f:
        replies_data = json.load(f)
        replies = replies_data["replies"]

    if message.mentions:
            for member in message.mentions:
                # Envoyer un message dans le canal où le message a été envoyé
                avatar_file = f"{member.id}.jpg"
                if not os.path.exists(avatar_file):
                    # avatar_url = "https://cdn.discordapp.com/avatars/555361128688123908/9b6f03f256b9fb26e5b1da8ca837bc0d.webp?size=128"
                    avatar_url = member.avatar
                    avatar_data = requests.get(avatar_url)
                    if avatar_data.status_code != 200:
                        continue
                    with open(avatar_file, "wb") as f:
                        f.write(avatar_data.content)
                        #Conversion de l'image en format JPEG
                        im = Image.open(avatar_file)
                        im = im.convert("RGB")
                        im.save(f"{member.id}.jpg", "JPEG")
                with open(avatar_file, "rb") as f:
                    avatar_b64 = f.read()
                    # Change the webhook's image and name
                    members = message.guild.members
                    serverMemberTagged = next(m for m in members if m.id == member.id)
                    serverMemberAuthor = next(m for m in members if m.id == message.author.id)
                    if member.nick:
                        usedName = serverMemberTagged.nick
                    else:
                        usedName = serverMemberTagged.name
                    await webhook.edit(name=usedName, avatar=avatar_b64)
                    # Send a message with the webhook
                    randomReply = random.choice(replies)
                    await webhook.send(randomReply)

client.run('MTA2NTQ0MDcyOTk1NjEwNjI0MQ.GPoNrC.Xarp1udyzrU1877Zxi_AeFwawJJf6PpYlYMMDs')
