import pdb
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
            await ctx.send(f'id: {faq.id}, channel: {bot.get_channel(int(faq.channel_id))}, msg_id: {faq.message_id}, {faq.question}: {faq.answer}')

@bot.command()
async def update_faq(ctx, faq_id: int = None):
    # If no faq_id is provided, prompt the user for the faq_id
    if faq_id is None:
        await ctx.send('Please enter the ID of the FAQ you want to update:')
        faq_id_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        try:
            faq_id = int(faq_id_message.content)
        except ValueError:
            await ctx.send('Invalid FAQ ID. Please enter a valid ID.')
            return

    # Get the faq for the given faq_id
    faq = await faqorm.get_faq(faq_id)
    if faq is None:
        await ctx.send(f'No FAQ found with ID {faq_id}')
        return

    # Display the current question and answer to the user in an embed
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=faq.question)
    embed.add_field(name='Answer', value=faq.answer)
    await ctx.send(embed=embed)

    # Prompt the user for the new question
    await ctx.send('What is the new question?')
    question_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    question = question_response.content
    
    # Prompt the user for the new answer
    await ctx.send('What is the new answer?')
    answer_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    answer = answer_response.content

    # Display the new question and answer to the user in an embed
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=question)
    embed.add_field(name='Answer', value=answer)
    await ctx.send(embed=embed)

    # Prompt the user to confirm the update
    await ctx.send('Are you sure you want to update this FAQ? (y/n)')
    confirmation_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    if confirmation_response.content.lower() != 'y':
        await ctx.send('FAQ update cancelled.')
        return

    # Update the FAQ entry
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
