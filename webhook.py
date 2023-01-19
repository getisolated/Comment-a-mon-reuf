import discord
from discord import Webhook
import requests
from PIL import Image
import os
import json
import random

# Creating intents for the bot
intents = discord.Intents.default()
intents.members = True

# Initializing the bot
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Find the webhook by its id
    webhooks = await message.channel.webhooks()
    # Add the webhook ID here ---------------------v
    webhook = next((x for x in webhooks if x.id == 1065757061285171361 ), None)

    # Open the json file with the replies
    with open("replies.json", "r") as f:
        replies_data = json.load(f)
        replies = replies_data["replies"]

    # Check if the message mentions someone
    if message.mentions:
            for member in message.mentions:
                # Download the avatar of the mentioned user if it doesn't exist
                avatar_file = f"{member.id}.jpg"
                if not os.path.exists(avatar_file):
                    avatar_url = member.avatar
                    avatar_data = requests.get(avatar_url)
                    if avatar_data.status_code != 200:
                        continue
                    # Saves the avatar in a file with the id of the tagged user as a name
                    with open(avatar_file, "wb") as f:
                        f.write(avatar_data.content)
                        # Converts image to JPEG
                        im = Image.open(avatar_file)
                        im = im.convert("RGB")
                        im.save(f"{member.id}.jpg", "JPEG")
                # Opens and reads the avatar by the id of the tagged user
                with open(avatar_file, "rb") as f:
                    avatar_b64 = f.read()
                    # Change the webhook's image and name
                    members = message.guild.members
                    serverMemberTagged = next(m for m in members if m.id == member.id)
                    serverMemberAuthor = next(m for m in members if m.id == message.author.id)

                    # Assign the designation of the tagged user (if it's a name or a nick)
                    if member.nick:
                        taggedDesignation = serverMemberTagged.nick
                    else:
                        taggedDesignation = serverMemberTagged.name

                    # Assign the designation of the author (if it's a name or a nick)
                    if message.author.nick:
                        authorDesignation = serverMemberAuthor.nick
                    else:
                        authorDesignation = serverMemberAuthor.name

                    # Changes the webhook to the appareance of the tagged user
                    await webhook.edit(name=serverMemberAuthor, avatar=avatar_b64)
                    # Chooses random message from the JSON Replies
                    randomReply = random.choice(replies)
                    # Assign the variables of the JSON to the variables
                    message = randomReply.format(author = authorDesignation, tagged = taggedDesignation)
                    # Sends the message with the webhook
                    await webhook.send(message)

# Connect to the bot
client.run('MTA2NTQ0MDcyOTk1NjEwNjI0MQ.GGGvh5.46bLslK1MA8Ea9vJYNn7rzOhSinaBqS6lrNVrI')
