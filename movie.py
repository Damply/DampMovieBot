import discord
from imdb import IMDb
import pyperclip
from pyshorteners import Shortener
from discord.ext.commands import Bot
from discord.ext import commands

spider = 'VIDEOSPIDER LINK HERE'

TOKEN = 'DISCORD BOT TOKEN HERE'

ia = IMDb()

shortener = Shortener('Tinyurl')

client = discord.Client()



Ratey = False
Ploty = False
Thumbnaily = False



@client.event
@commands.cooldown(1, 120, commands.BucketType.user)
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
		
	global Ratey
	global Ploty
	global Thumbnaily
	
	# Set thumb to true/false
	if message.content.startswith('$EnableThumb'):
		Thumbnaily = True
		msg = '**Thumbnail enabled**'
		await client.send_message(message.channel, msg)
		
	if message.content.startswith('$DisableThumb'):
		Thumbnaily = False
		msg = '**Thumbnail disabled**'
		await client.send_message(message.channel, msg)

	# Set rate to true/false
	if message.content.startswith('$EnableRate'):
		Ratey = True
		msg = '**Rate enabled**'
		await client.send_message(message.channel, msg)
		
	if message.content.startswith('$DisableRate'):
		Ratey = False
		msg = '**Rate disabled**'
		await client.send_message(message.channel, msg)
	
	# Set plot to true/false
	if message.content.startswith('$EnablePlot'):
		Ploty = True
		msg = '**Plot enabled**'
		await client.send_message(message.channel, msg)
	
	if message.content.startswith('$DisablePlot'):
		Ploty = False
		msg = '**Plot disabled**'
		await client.send_message(message.channel, msg)
		
	
	
	
	
	if message.content.startswith('$debug'):
		msg = '**VARIABLES**'
		await client.send_message(message.channel, msg)
		await client.send_message(message.channel, Ratey)
		await client.send_message(message.channel, Ploty)
		await client.send_message(message.channel, Thumbnaily)

		

	if message.content.startswith('$movie'):
		input = message.content[6:]
		movies = ia.search_movie(input)
		print("Finding",input)
		id = movies[0].movieID
		fplot = ia.get_movie(id)
		rate = ia.get_movie(id, 'vote details')
		movlink = shortener.short(spider + movies[0].movieID)
		plot = fplot['plot'][0]
		rating = rate.get('arithmetic mean')
		thumbnail = ia.get_movie(movies[0].movieID)
		msg = '{0.author.mention}'.format(message)
		boldrate = '**Rating**'
		boldplot = '**About this movie**'
		link = movlink.format(message)
		await client.send_message(message.channel, msg+ link)
		if Ratey is True:
			await client.send_message(message.channel, boldrate)
			await client.send_message(message.channel, rating)
		if Ploty is True:
			await client.send_message(message.channel, boldplot)
			await client.send_message(message.channel, plot)
		if Thumbnaily is True:
			await client.send_message(message.channel, thumbnail['cover url'])
		print("Found",input)
		
	if message.content == '$leave':
		lmsg = 'Goodbye'
		await client.send_message(message.channel, lmsg)
		await client.logout()
		
	if message.content.startswith('$help'):
		msg1 = '**Commands**'
		msg2 = 'To request a movie link use'
		msg3 = ' $movie MOVIENAME'
		msg8 = '$leave'
		msg4 = '**Feature commands**'
		msg5 = '$EnableRate / $DisableRate'
		msg6 = '$EnablePlot / $DisablePlot'
		msg7 = '$EnableThumb / $DisableThumb'
		await client.send_message(message.channel, msg1)
		await client.send_message(message.channel, msg2+msg3)
		await client.send_message(message.channel, msg8)
		await client.send_message(message.channel, msg4)
		await client.send_message(message.channel, msg5)
		await client.send_message(message.channel, msg6)
		await client.send_message(message.channel, msg7)
		
	if message.content.startswith('$game'):
		inputt = message.content[6:]
		msg = 'Setting game to: '
		await client.send_message(message.channel, msg+inputt)
		await client.change_presence(game=discord.Game(name=inputt, type=1))
		
	
	
		


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)