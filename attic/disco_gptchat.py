import os
import asyncio
import logging
import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import bindparam

import openai
from transformers import AutoModelForCausalLM, AutoTokenizer

# Connect to the database
engine = create_async_engine("sqlite+aiosqlite:///mydatabase.db")

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
        engine="text-davinci-003",
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

@bot.command(name='add_faq', help='Adds a new question and answer to the faqs table')
async def add_faq(ctx):
    # Prompt the user to enter a question
    await ctx.send('Enter the question:')

    # Wait for the user's response
    question_message = await bot.wait_for('message', check=lambda message: message.author == ctx.message.author)
    question = question_message.content

    # Prompt the user to enter an answer
    await ctx.send('Enter the answer:')

    # Wait for the user's response
    answer_message = await bot.wait_for('message', check=lambda message: message.author == ctx.message.author)
    answer = answer_message.content

    async with engine.connect() as conn:
        # Insert the question and answer into the faqs table
        insert_stmt = text("INSERT INTO faqs (question, answer) VALUES (:question, :answer)")
        await conn.execute(insert_stmt, {'question': question, 'answer': answer})
        await conn.commit()
        await ctx.send(f'Successfully added the following question and answer to the faqs table: {question} - {answer}')


@bot.command(name='search_faq', help='Searches the faqs table for a matching question and returns the answer')
async def search_faq(ctx, question: str = None):
    if not question:
        # Prompt the user to enter a search term
        await ctx.send('Enter a search term:')

        # Wait for the user's response
        search_term_message = await bot.wait_for('message', check=lambda message: message.author == ctx.message.author)
        question = search_term_message.content

    async with engine.connect() as conn:
        # Fetch the answer for the given question
        result = await conn.execute(text("SELECT answer FROM faqs WHERE question LIKE :question"), {'question': f'%{question}%'})
        row = result.fetchone()
        if row:
            answer = row['answer']
            await ctx.send(f'The answer to the question "{question}" is: {answer}')
        else:
            await ctx.send(f'No matching question was found in the faqs table')




@bot.command(name='show_questions', help='Displays all the questions in the faqs table')
async def show_questions(ctx):
    async with engine.connect() as conn:
        # Fetch all the questions from the faqs table
        result = await conn.execute(text("SELECT question FROM faqs"))
        rows = result.fetchall()
        
         # Log the rows to a file
        logging.info(rows)

        # Construct a message with all the questions
        message = 'All the questions in the faqs table:\n'
        for row in rows:
            message += row['question'] + '\n'

        # Send the message to the Discord channel
        await ctx.send(message)

# Use the Discord bot token variable when starting the bot
bot.run(discord_bot_token)
