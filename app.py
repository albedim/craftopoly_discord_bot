import os

import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

from labels.labels import *
from utils.utils import BASE_URL

load_dotenv()

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='start')
async def start(ctx):
    await ctx.send(start_message(ctx.author.name))


@bot.command(name='connect')
async def connect(ctx, code):
    user_id = str(ctx.author.id)
    getUser = requests.put(f"{BASE_URL}/users/discord/connect", json={
        'discord_user_id': user_id,
        'code': code
    })
    if getUser.status_code == 404:
        await ctx.send(user_code_not_found())
    elif getUser.status_code == 409:
        await ctx.send(user_already_connected())
    elif getUser.status_code != 200:
        await ctx.send(error())
    elif getUser.status_code == 200:
        await ctx.send(connect_message_success(getUser.json()['param']))


@bot.command(name='ticket')
async def ticket(ctx, *args):
    user_id = str(ctx.author.id)
    isConnected = requests.get(f"{BASE_URL}/users/discord/{user_id}").status_code != 404
    print(isConnected)
    if isConnected:
        if len(args) > 0:
            if args[0] == 'create':
                if len(args) > 1:
                    createTicket = requests.post(f"{BASE_URL}/tickets/?platform=discord", json={
                        'message': " ".join(args[1:])
                    }, headers={"Authorization": "Bearer " + user_id})
                    if createTicket.status_code == 404:
                        await ctx.send(user_code_not_found())
                    elif createTicket.status_code == 409:
                        await ctx.send(ticket_already_open())
                    elif createTicket.status_code != 200:
                        await ctx.send(error())
                    elif createTicket.status_code == 200:
                        await ctx.send(ticket_successfully_created())
                else:
                    await ctx.send(wrong_command_use())
            elif args[0] == 'close':
                if len(args) == 2:
                    ticket_id = args[1]
                    closeTicket = requests.put(f"{BASE_URL}/tickets/{ticket_id}?platform=discord",
                                               headers={"Authorization": "Bearer " + user_id})
                    if closeTicket.status_code == 403:
                        await ctx.send(no_enough_permissions())
                    elif closeTicket.status_code == 404:
                        await ctx.send(ticket_not_found())
                    elif closeTicket.status_code == 409:
                        await ctx.send(ticket_already_closed())
                    elif closeTicket.status_code != 200:
                        await ctx.send(error())
                    elif closeTicket.status_code == 200:
                        await ctx.send(ticket_successfully_closed())
                else:
                    await ctx.send(wrong_command_use())
            elif args[0] == 'info':
                if len(args) == 2 or len(args) == 3:
                    ticket_id = args[1]
                    page = args[2] if len(args) == 3 else "1"
                    # Code to get ticket information
                    ticket = requests.get(f"{BASE_URL}/tickets/{ticket_id}?page={page}&platform=discord",
                                          headers={"Authorization": "Bearer " + user_id})
                    if ticket.status_code == 403:
                        await ctx.send(no_enough_permissions())
                    elif ticket.status_code == 404:
                        await ctx.send(ticket_not_found())
                    elif ticket.status_code == 409:
                        await ctx.send(ticket_already_closed())
                    elif ticket.status_code != 200:
                        await ctx.send(error())
                    elif ticket.status_code == 200:
                        await ctx.send(ticket_info(page, ticket.json()['param']))
                else:
                    await ctx.send(wrong_command_use())
            elif args[0] == 'comment':
                if len(args) > 2:
                    ticket_id = args[1]
                    comment_text = " ".join(args[2:])
                    # Code to add a comment to a ticket
                    ticket = requests.post(f"{BASE_URL}/tickets/messages?platform=discord", json={
                        'message': comment_text,
                        'ticket_id': int(ticket_id)
                    }, headers={"Authorization": "Bearer " + user_id})
                    if ticket.status_code == 403:
                        await ctx.send(no_enough_permissions())
                    elif ticket.status_code == 404:
                        await ctx.send(ticket_not_found())
                    elif ticket.status_code == 422:
                        await ctx.send(ticket_closed())
                    elif ticket.status_code != 200:
                        await ctx.send(error())
                    elif ticket.status_code == 200:
                        await ctx.send(ticket_successfully_commented())
                else:
                    await ctx.send(wrong_command_use())
            elif args[0] == 'all':
                if len(args) == 1 or len(args) == 2:
                    page = args[1] if len(args) == 2 else "1"
                    # Code to list all tickets
                    tickets = requests.get(f"{BASE_URL}/tickets/?page={page}&platform=discord",
                                           headers={"Authorization": "Bearer " + user_id})
                    if tickets.status_code == 403:
                        await ctx.send(no_enough_permissions())
                    elif tickets.status_code == 404:
                        await ctx.send(ticket_not_found())
                    elif tickets.status_code != 200:
                        await ctx.send(error())
                    elif tickets.status_code == 200:
                        await ctx.send(ticket_list_info(page, tickets.json()['param']))
                else:
                    await ctx.send(wrong_command_use())
            elif args[0] == 'list':
                username = requests.get(f"{BASE_URL}/users/discord/{user_id}").json()['param']['username']
                if len(args) == 1 or len(args) == 2:
                    page = args[1] if len(args) == 2 else "1"
                    # Code to list tickets for a specific user
                    tickets = requests.get(f"{BASE_URL}/tickets/user/{username}?page={page}")
                    if tickets.status_code == 403:
                        await ctx.send(no_enough_permissions())
                    elif tickets.status_code == 404:
                        await ctx.send(ticket_not_found())
                    elif tickets.status_code != 200:
                        await ctx.send(error())
                    elif tickets.status_code == 200:
                        await ctx.send(ticket_list_info(page, tickets.json()['param']))
                else:
                    await ctx.send(wrong_command_use())
        else:
            await ctx.send(help_message())
    else:
        await ctx.send(not_connected())

if __name__ == '__main__':
    bot.run(TOKEN)
