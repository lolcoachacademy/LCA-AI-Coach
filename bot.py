import discord
import requests
import os

# Load environment variables from Render
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    if message.content.startswith("!ask"):
        question = message.content[5:].strip()  # Remove "!ask " from the message

        if not question:
            await message.channel.send("Please ask a question after '!ask'.")
            return

        # Send message to n8n webhook
        payload = {"content": question, "user": str(message.author), "channel_id": str(message.channel.id)}
        response = requests.post(WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            await message.channel.send("Processing your question..
