import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
import random
import nacl
import shutil

boobies = ["https://files.yande.re/sample/5a6459719bf0db921ede0d143acd6783/yande.re%20454287%20sample%20darling_in_the_franxx%20horns%20naked%20nipples%20shadowgrave%20wet%20zero_two_%28darling_in_the_franxx%29.jpg"
, "https://i.redd.it/dl38eysjsae21.jpg"
, "https://1.bp.blogspot.com/-yYLpUhOuuXA/W86Ie2HlVXI/AAAAAAAA0M8/5uezeksbEIQ04jHi0m11cctrEGmCQPmIACLcBGAs/w7000/Darling%2Bin%2Bthe%2BFranxx%2B-%2BZero%2BTwo%2BRender%2B9.png"
, "https://i.redd.it/fapsyap3o2o51.jpg"
, "https://i.redd.it/b5trvmmyk8n51.jpg"
]
butt = ["https://files.yande.re/image/877cbe5d78fad92d91c361b15f38dc60/yande.re%20445214%20anus%20ass%20darling_in_the_franxx%20horns%20naked%20penis%20pussy%20rosaline%20uncensored%20zero_two_(darling_in_the_franxx).jpg"
, "https://i.redd.it/2pnf07afo1331.jpg"
, "https://external-preview.redd.it/0xrz-2qzmEbMn98XSLVNArhfHcbS9nWSRmV6b9MaMoA.jpg?auto=webp&s=a2c5d2777c039d0f5c2a907f9c2779d1500578bf"
, "https://pbs.twimg.com/media/EC_5ULSUUAAadpR?format=jpg&name=medium"]
pussys = ["https://cdn.donmai.us/original/d8/16/__zero_two_darling_in_the_franxx_drawn_by_ginhaha__d8167f749f0ef3186ce12a0c2d6f087f.png"
, "https://konachan.com/sample/7ab407f045e64a82006f432af148724e/Konachan.com%20-%20261504%20sample.jpg"
, "https://img2.gelbooru.com/samples/82/a3/sample_82a35e3396eb21849bb6ee7a6b4018c5.jpg"
, "https://cdn.donmai.us/sample/d3/11/__zero_two_darling_in_the_franxx_drawn_by_darkmaya__sample-d3113958950d5137ec51880df9a64956.jpg"
, "https://i.redd.it/fapsyap3o2o51.jpg"]

bot = commands.Bot(command_prefix='02')
client = discord.Client()
bot.remove_command('help')

@bot.command()
async def help(ctx):
    message = ("""
NORMAL :grinning:
    clear <messages[default=5]> = clears 5 or given amount of messages
MUSIC :musical_note:
    join = joins your call
    play <YOUTUBE URL> = plays sound from any youtube video
    leave = leaves call
    play ss = plays the last song that was played
    skip = skips song
    pause = pause song
    resume = resumes song
NSFW :underage:
    boobs = chooses random picture of zero twos boobs
    ass = chooses random picture of zero twos ass
    pussy = chooses random picture of zero twos pussy

    """)
    embed = discord.Embed(title="Help",description=message)
    await ctx.send(embed=embed)
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command(pass_context=True)
async def pussy(ctx):
    await ctx.send(random.choice(pussys))

@bot.command()
async def emoji(ctx):
    await ctx.send(":bread:")

@bot.command()
async def boobs(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send("There are kids here dont do that sh*t")
    else:
        await ctx.send(random.choice(boobies))

@bot.command()
async def ass(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send("There are kids here dont do that sh*t")
    else:
        await ctx.send(random.choice(butt))

@bot.command()
async def stop(ctx):
    await ctx.send("Bot is going down")
    exit()

@bot.event
async def on_ready():
    print(print("Logged in as: " + bot.user.name + "\n"))

@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl', 'p'])
async def play(ctx, url: str):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        if url == "ss":
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.volume = 100
            voice.is_playing()
        else:
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except PermissionError:
                await ctx.send("Wait for the current playing music end or use the 'stop' command")
                return
            await ctx.send("Getting everything ready, playing audio soon(if its a long sogn it might take a second)")
            print("Someone wants to play music let me get that ready for them...")
            voice = get(bot.voice_clients, guild=ctx.guild)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, 'song.mp3')
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.volume = 100
            voice.is_playing()
    else:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            song_there = os.path.isfile("song.mp3")
        if url == "ss":
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.volume = 100
            voice.is_playing()
        else:
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except PermissionError:
                await ctx.send("Wait for the current playing music end or use the 'stop' command")
                return
            await ctx.send("Getting everything ready, playing audio soon(if its a long song it might take a second)")
            print("Someone wants to play music let me get that ready for them...")
            voice = get(bot.voice_clients, guild=ctx.guild)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, 'song.mp3')
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
            voice.volume = 100
            voice.is_playing()

@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")

@bot.command(pass_context=True, aliases=['s', 'fs'])
async def skip(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")
@bot.command(pass_context=True, aliases=['del'])
async def delete(ctx, song="song.mp3"):
    os.remove(song)
    await ctx.send("{} has been deleted and is no longer taking up space!".format(song))

@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")
@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")
@bot.command(pass_context=True, aliases=['e'])
async def everyone(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("@everyone")
    await ctx.channel.purge(limit=1)

bot.run("NzU2Mjc0MzAwNzEzMTczMTEy.X2PdVA.oGLFh6ypcZwsKCqiIw99oXfh4-o")
