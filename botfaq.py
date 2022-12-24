import os
import asyncio
import logging
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import faq

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

@bot.command()
async def hello(ctx):
    name = ctx.message.author.name
    await ctx.send(f'Nice to meet you, {name}!')


@bot.command()
@has_permissions(manage_messages=True)
async def add_faq(ctx, channel: discord.TextChannel = None):
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel

    # Send a message to the channel to prompt the user for the question
    await ctx.send('Please type the question for the FAQ:')

    # Wait for the user's response
    question_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == channel)
    question = question_message.content

    # Send a message to the channel to prompt the user for the answer
    await ctx.send('Please type the answer for the FAQ:')

    # Wait for the user's response
    answer_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == channel)
    answer = answer_message.content

    # Create a session object
    session = faq.Session()

    # Add the FAQ entry asynchronously
    await faq.add_faq(session, str(channel.id), question, answer)

    # Send a message to the channel to confirm that the FAQ has been added
    await ctx.send(f'Successfully added the FAQ: "{question}"')



@bot.command()
async def list_faqs(ctx, channel: discord.TextChannel = None):
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel
    # Create a session object
    session = faq.Session()
    # Retrieve a list of all the FAQ entries for the specified channel
    faqs_list = await faq.list_faqs(session, str(channel.id))
    # Iterate through the list of FAQs and send a message for each one
    for faq_item in faqs_list:
        await ctx.send(f'{faq_item.question} - {faq_item.answer}')


@bot.command()
async def update_faq(ctx, faq_id: int, question: str, answer: str):
    # Create a session object
    session = faq.Session()

    # Update the FAQ entry asynchronously
    await faq.update_faq(session, faq_id, question, answer)

    # Notify the user that the FAQ entry has been updated
    await ctx.send(f'Successfully updated the FAQ with ID {faq_id}')

@bot.command()
async def delete_faq(ctx, faq_id: int):
    # Create a session object
    session = faq.Session()

    # Delete the FAQ entry asynchronously
    await faq.delete_faq(session, faq_id)

    # Notify the user that the FAQ entry has been deleted
    await ctx.send(f'Successfully deleted the FAQ with ID {faq_id}')

@bot.command()
async def get_faq(ctx, faq_id: int):
    # Create a session object
    session = faq.Session()

    # Retrieve the FAQ entry asynchronously
    faq_entry = await faq.get_faq(session, faq_id)

    if faq_entry is not None:
        # Format the FAQ entry and send it to the user
        message = f'ID: {faq_entry.id}\nQuestion: {faq_entry.question}\nAnswer: {faq_entry.answer}'
        await ctx.send(message)
    else:
        # Notify the user that the FAQ entry was not found
        await ctx.send(f'Could not find an FAQ with ID {faq_id}')







@bot.command()
async def like_faq(ctx, message: discord.Message):
    # Create a session object
    session = faq.Session()

    # Increment the reaction count for the FAQ entry asynchronously
    await faq.like_faq(session, str(message.id))

    # Notify the user that the reaction count has been updated
    await ctx.send('Successfully liked the FAQ')

@bot.command()
async def dislike_faq(ctx, message: discord.Message):
    # Create a session object
    session = faq.Session()

    # Decrement the reaction count for the FAQ entry asynchronously
    await faq.dislike_faq(session, str(message.id))

    # Notify the user that the reaction count has been updated
    await ctx.send('Successfully disliked the FAQ')


@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is a thumbs up or thumbs down
    if str(reaction.emoji) == '👍':
        # Increment the reaction count for the FAQ entry asynchronously
        session = faq.Session()
        await faq.like_faq(session, str(reaction.message.id))
    elif str(reaction.emoji) == '👎':
        # Decrement the reaction count for the FAQ entry asynchronously
        session = faq.Session()
        await faq.dislike_faq(session, str(reaction.message.id))

@bot.event
async def on_reaction_remove(reaction, user):
    # Check if the reaction is a thumbs up or thumbs down
    if str(reaction.emoji) == '👍':
        # Decrement the reaction count for the FAQ entry asynchronously
        session = faq.Session()
        await faq.dislike_faq(session, str(reaction.message.id))
    elif str(reaction.emoji) == '👎':
        # Increment the reaction count for the FAQ entry asynchronously
        session = faq.Session()
        await faq.like_faq(session, str(reaction.message.id))

# Use the Discord bot token variable when starting the bot
bot.run(discord_bot_token)
