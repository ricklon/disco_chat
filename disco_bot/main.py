import os
import asyncio
import logging
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import click
from dotenv import load_dotenv
import json

import openai
from ai import AI


# Load the environment variables from the .env file
load_dotenv()

# Set the OpenAI API key using an environment variable
openai_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Create a dictionary to hold the AI instances
ais = {
    "Davinci": AI("Davinci", "text-davinci-003", openai_api_key, "Hello, I'm Davinci. How can I assist you today?"),
    "Curie": AI("Curie", "text-curie-001", openai_api_key, "Hi there, I'm Curie. How can I help you?"),
}

# Set the maximum number of AIs
MAX_AIS = int(os.environ.get("MAX_AIS", 10))


# Create the Discord bot
bot = commands.Bot(command_prefix='!')


@bot.command(name='listais', help='List available AIs')
async def list_ais(ctx):
    await ctx.send("Available AIs: " + ", ".join(ais.keys()))


@bot.command(name='newai', help='Create a new AI')
@has_permissions(administrator=True)
async def new_ai(ctx, name: str, model: str, prompt: str = None):
    if len(ais) >= MAX_AIS:
        await ctx.send(f"Error: maximum number of AIs ({MAX_AIS}) has been reached.")
        return
    ai = AI(name, model, openai_api_key, prompt)
    ais[name] = ai
    await ctx.send(f"Created AI '{name}' with model '{model}'.")


@bot.command(name='getprompt', help='Get the prompt for an AI')
async def get_prompt(ctx, name: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    prompt = ai.get_prompt()
    await ctx.send(f"Prompt for AI '{name}':\n```{prompt}```")


@bot.command(name='setprompt', help='Set the prompt for an AI')
@has_permissions(administrator=True)
async def set_prompt(ctx, name: str, prompt: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    ai.set_prompt(prompt)
    await ctx.send(f"Prompt for AI '{name}' has been set.")


@bot.command(name='savehistory', help='Save conversation history for an AI')
async def save_history(ctx, name: str, file_name: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    ai.save_conversation_history(file_name)
    await ctx.send(f"Conversation history for AI '{name}' has been saved to file '{file_name}'.")


@bot.command(name='deactivate', help='Deactivate an AI')
@has_permissions(administrator=True)
async def deactivate(ctx, name: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    ai.deactivate()
    await ctx.send(f"AI '{name}' has been deactivated.")


@bot.command(name='activate', help='Activate an AI')
@has_permissions(administrator=True)
async def activate(ctx, name: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    ai.activate()
    await ctx.send(f"AI '{name}' has been activated.")


@bot.command(name='removeai', help='Remove an AI')
@has_permissions(administrator=True)
async def remove_ai(ctx, name: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    del ais[name]
    await ctx.send(f"AI '{name}' has been removed.")


@bot.command(name='chat', help='Chat with an AI')
async def chat(ctx, name: str, message: str):
    ai = ais.get(name)
    if ai is None:
        await ctx.send(f"Error: AI '{name}' not found.")
        return
    response = ai.get_response(message)
    await ctx.send(response)


if __name__ == '__main__':
    bot.run(os.environ['DISCORD_BOT_TOKEN'])
