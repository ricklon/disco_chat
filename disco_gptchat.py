import os
import discord
from discord.ext import commands
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer


# Set the OpenAI API key using an environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create a variable to hold the Discord bot token
discord_bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Create a variable to hold the Dialogpt auth token
auth_token = os.environ["DIALOGPT_AUTH_TOKEN"]


# The name of the channel that the bot should accept messages from
allowed_channel_name = "chat2gpt"

# Get the list of default intents
intents = discord.Intents.all()

# Add the PrivilegedIntents.MESSAGE_CONTENT intent to the list of intents
#intents.privileged.add(discord.Intents.MESSAGE_CONTENT)

# Create the Discord client with the specified intents
#client = discord.Client(intents=intents)

# Create a Bot instance with the specified command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Set the allowed_channel_id variable to the specified value
allowed_channel_id = 1050950698382151680

# # set up Hugging Face 
tokenizer = AutoTokenizer.from_pretrained("ricklon/DialoGPT-medium-guinan", use_fast=True, use_auth_token=auth_token)
model = AutoModelForCausalLM.from_pretrained("ricklon/DialoGPT-medium-guinan", use_auth_token=auth_token)


# Define the on_ready event handler
@bot.event
async def on_ready():
    # Print the bot's name
    print(f"Logged in as {bot.user.name}")
    # app_info = await bot.get_current_application_info()
    # print(app_info.bot_public)
    # print(app_info.bot_require_code_grant)
    # Print the bot's name to the channel
    channel = bot.get_channel(allowed_channel_id)
    await channel.send(f"Logged in as {bot.user.name}")


# #Higging face Guinan model
# @bot.command()
# async def guinan(ctx, *args):
#     if not args:
#         await ctx.send('Please provide a prompt for the model.')
#         return
    
#     prompt = ' '.join(args)
#     input_ids = tokenizer.encode(prompt, return_tensors='pt')
#     response = model.generate(input_ids)
#     response_text = tokenizer.decode(response[0])
#     await ctx.send(response_text)


@bot.command()
async def dialog(ctx):

    
    # Use the model to generate a response to the user's message
    user_input = ctx.message.content
    response = model.generate(input_ids=tokenizer.encode(user_input), max_length=100, do_sample=True, top_p=1, top_k=50, temperature=0.5)
    response_text = tokenizer.decode(response[0])
    
    await ctx.send(response_text)

# Define the "echo" command using the @bot.command() decorator
@bot.command()
async def echo(ctx, *args):
    # Only process messages that were sent in the allowed channel
    if ctx.channel.id != allowed_channel_id:
        return

    # Send the message content back to the channel
    if not args:
        return
    output = ' '.join(args)
    await ctx.send(output)

@bot.command()
async def hello(ctx):
    name = ctx.message.author.name
    await ctx.send(f'Nice to meet you, {name}!')

@bot.command()
async def ask(ctx, *args):
    # Only process messages that were sent in the allowed channel
    if ctx.channel.id != allowed_channel_id:
        return
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=" ".join(args),
        max_tokens=1024,
        temperature=0.5,
    )

    await ctx.send(response["choices"][0]["text"])


#info command
@bot.command()
async def info(ctx):
    commands = [c.name for c in bot.commands]
    command_list = '\n'.join(commands)
    bot_info = 'This is a simple Discord bot that can do the following things:\n'
    bot_info += '- Say hello to you\n'
    bot_info += '- Echo back the messages you send it\n'
    bot_info += f'\nHere is a list of available commands:\n{command_list}'
    await ctx.send(bot_info)

# Use the Discord bot token variable when starting the bot
bot.run(discord_bot_token)
