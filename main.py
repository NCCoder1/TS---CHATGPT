import discord
import openai
import os

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# Set up OpenAI API credentials
openai.api_key = os.environ['OPENAI_API_KEY']

# Define a cache to store previous responses
response_cache = {}

# Define a function to get a ChatGPT response, with caching
def get_response(message):
    if message.content in response_cache:
        return response_cache[message.content]
    else:
        response = openai.Completion.create(
            engine="davinci",
            prompt=message.content,
            max_tokens=50
        )
        response_text = response.choices[0].text
        response_cache[message.content] = response_text
        return response_text

# Define an event listener for when the bot connects to Discord
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Define an event listener for when a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message starts with a mention of the bot
    if client.user.mentioned_in(message) or message.channel.type == discord.ChannelType.private:
        response = get_response(message)
        await message.channel.send(response)

# Start the bot
client.run(os.environ['DISCORD_BOT_TOKEN'])
