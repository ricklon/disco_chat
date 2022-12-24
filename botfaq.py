import os
import asyncio
import logging
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import faqorm 
import setupdb



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
    await setupdb.create_database()
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
async def exit(ctx):
    """Shut down the bot."""
    # Check if the user has the "administrator" permission
    if ctx.author.guild_permissions.administrator:
        await ctx.send('Shutting down...')
        await bot.logout()
    else:
        await ctx.send('You do not have permission to shut down the bot.')



@bot.command()
async def add_faq(ctx, channel: discord.TextChannel = None):
    """Add a new FAQ entry."""
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel
    print(f"Adding FAQ for channel: {ctx.channel.name}, id: {channel.id}, msg.id: {ctx.message.id}")
    # Set the channel_id to the channel's ID
    channel_id = channel.id


    # Prompt the user for the question
    await ctx.send('What is the question you would like to add to the FAQ?')
    question_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    question = question_response.content

    # Prompt the user for the answer
    await ctx.send('What is the answer to the question?')
    answer_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    answer = answer_response.content

    # Add the FAQ entry
    await faqorm.add_faq(channel_id, ctx.message.id, question, answer)
    await ctx.send('FAQ added successfully!')


@bot.command()
async def list_faqs(ctx,  channel: discord.TextChannel = None):
    """List all FAQ entries for a particular channel."""
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel
    print(f"Adding FAQ for channel: {ctx.channel.name}, id: {channel.id}, msg.id: {ctx.message.id}")
    # Set the channel_id to the channel's ID
    channel_id = channel.id

    faqs = await faqorm.list_faqs(str(channel_id))
    if not faqs:
        await ctx.send('There are no FAQs for this channel.')
    else:
        for faq in faqs:
            await ctx.send(f'{faq.question}: {faq.answer}')

@bot.command()
async def update_faq(ctx, faq_id: int, question: str, answer: str):
    """Update the question and answer for a particular FAQ entry."""
    await faqorm.update_faq(faq_id, question, answer)
    await ctx.send('FAQ updated successfully!')

@bot.command()
async def delete_faq(ctx, faq_id: int):
    """Delete a particular FAQ entry."""
    await faqorm.delete_faq(faq_id)
    await ctx.send('FAQ deleted successfully!')

@bot.command()
async def get_faq(ctx, faq_id: int):
    """Retrieve a particular FAQ entry."""
    faq = await faqorm.get_faq(faq_id)
    if faq:
        await ctx.send(f'{faq.question}: {faq.answer}')
    else:
        await ctx.send('FAQ not found.')

@bot.command()
async def like_faq(ctx, message_id: int):
    """Increment the number of likes for an FAQ entry."""
    await faqorm.like_faq(message_id)
    await ctx.send('FAQ liked!')


@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is a thumbs up or thumbs down
    if str(reaction.emoji) == '👍':
        # Increment the reaction count for the FAQ entry asynchronously
        session = faqorm.Session()
        await faqorm.like_faq(session, str(reaction.message.id))
    elif str(reaction.emoji) == '👎':
        # Decrement the reaction count for the FAQ entry asynchronously
        session = faqorm.Session()
        await faqorm.dislike_faq(session, str(reaction.message.id))

@bot.event
async def on_reaction_remove(reaction, user):
    # Check if the reaction is a thumbs up or thumbs down
    if str(reaction.emoji) == '👍':
        # Decrement the reaction count for the FAQ entry asynchronously
        session = faqorm.Session()
        await faqorm.dislike_faq(session, str(reaction.message.id))
    elif str(reaction.emoji) == '👎':
        # Increment the reaction count for the FAQ entry asynchronously
        session = faqorm.Session()
        await faqorm.like_faq(session, str(reaction.message.id))

asyncio.run(setupdb.create_database())
# Use the Discord bot token variable when starting the bot
bot.run(discord_bot_token)
