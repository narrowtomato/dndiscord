# This is the bot's token, configured in your Discord developer account
TOKEN = ''

# This is the channel where you want bot commands to be recognized
BOT_CHANNEL = ''

import discord
import random
import json

# This is the path to the JSON file containing the spells.  You may need to change this to the absolute path
# This file can be found here: https://github.com/mattearly/DnD_5e_Perfect_Spells
SPELLS_FILENAME = "allSpells.json"

# Open the file and load spells into dictionary
try:
    with open(SPELLS_FILENAME, 'r') as file:
        spells = json.load(file)
except FileNotFoundError as e:
    print(f"File {SPELLS_FILENAME} not found")
    exit()

# Create Discord client
client = discord.Client()

# Verify Login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Listen for messages
@client.event
async def on_message(message):
    # Break message into components
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    # Ignore messages from self
    if message.author == client.user:
        return

    # Messages in the bot channel
    if message.channel.name == BOT_CHANNEL:

        # Show spells with !spell
        if user_message.lower().split(' ')[0] == '!spell':
            spell_found = False
            for spell in spells["allSpells"]:
                if spell["name"].lower() == " ".join(user_message.lower().split(' ')[1:]):
                    # This builds the message and splits it into chunks of 2000 characters to match the Discord max
                    msg = ""
                    for k, v in spell.items():
                        msg += f"**{k}**: {v}\n"
                    num_msgs = (len(msg) // 2000) + 1
                    for i in range(1, num_msgs + 1):
                        await message.channel.send(msg[((i - 1) * 2000):(i * 2000)])
                    spell_found = True
            if not spell_found:
                await message.channel.send("Spell not found.")

        # Roll dice with !roll
        if user_message.lower().split(' ')[0] == '!roll':
            try:
                # Get roll components
                selected_roll = user_message.lower().split(' ')[1]
                num_dice = user_message.lower().split(' ')[1].split('d')[0]
                type_dice = user_message.lower().split(' ')[1].split('d')[1]
                total_roll = 0

                # Loop through, calculate the roll and build the message
                msg = f"**{username}** rolled **{selected_roll}**: "
                for i in range(int(num_dice)):
                    roll = random.randint(1, int(type_dice))
                    total_roll += roll
                    msg += f"+ {str(roll)} "
                msg += f"= **{total_roll}**"

            # If roll could not be calculated from input
            except:
                msg = "Could not calculate that roll"

            # Send the message 
            await message.channel.send(msg)
            

client.run(TOKEN)