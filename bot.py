import os
import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        # await message.author.send(response) if is_private and message.channel != 'bot-alert' else await message.channel.send(response)
        if response is not None and is_private:
            await message.author.send(response)
        elif response is not None:
            await message.channel.send(response)
        else:
            pass

    except Exception as e:
        print(e)


# Bot function
def run_discord_bot():
    TOKEN = 'MTE4NDYxODY3NDkzMDMzOTg0MA.GeIl5V._24P5tYpRiLY8UN8mH5p_xWdtKfLGkeu4uxc1U'
    # TOKEN = os.environ["TOKEN"]
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_connect():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !status"))

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        # If message uses '?' at the beginning the bot will respond privately
        if len(user_message) > 0:
            if user_message[0] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
