#gerekli modüller
import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import youtube_dl
import datetime

YOUR_TOKEN=''

__version__ = '1.0.0'

# botun prefix'i
bot = commands.Bot(command_prefix='!')


# bot çalıştığında bot hakkında bilgiler verecek
@bot.event
async def on_ready():
    print('Bot Online!!')
    print(f'Bot-Adi: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    print(f'Discord Versiyonu: {discord.__version__}')
    print(f'Bot Versiyonu: {__version__}')
    print('------')

# botun server ile client arasındaki gecikmesini döndürür
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Gecikme: {0}ms'.format(round(bot.latency, 1)))

# random sayı gerektiği zaman kendisine verilen range ve 0 arasında bir sayı döndürecek
@bot.command()
async def rastgele(ctx, arg):
    sayi = random.randint(0,int(arg))
    await ctx.send(f"İşte senin için bir sayı : {sayi}")

# komut test fonksiyonu
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# istenilen kadar mesaj silme
@bot.event
async def on_message(message):
    if message.content.startswith('!sil'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit = count)
                    await message.channel.send('{} mesaj silindi 👌'.format(len(deleted)-1))
            else:
                deleted = await message.channel.purge(limit = 10)
                await message.channel.send('{} mesaj silindi 👌'.format(10))
    await bot.process_commands(message)

#handling kısmı
@bot.event
async def on_error(event, *args, **kwargs):
    if bot.dev:
        traceback.print_exc()
    else:
        embed = discord.Embed(title=':x: Event Hatası', colour=0xe74c3c)
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        try:
            await bot.AppInfo.owner.send(embed=embed)
        except:
            pass

bot.run(YOUR_TOKEN)