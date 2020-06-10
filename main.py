#gerekli modüller
import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import youtube_dl
import datetime
import platform

YOUR_TOKEN='INSERT_HERE_YOUR_TOKEN'

__version__ = '1.0.0'

# botun komut algılayıcısı
bot = commands.Bot(command_prefix='!')

#  region region komutlar
# botun server ile client arasındaki gecikmesini döndürür
@bot.command()
async def ping(ctx):
    print("- Ping istendi.")
    await ctx.send('Pong! Gecikme: {0}ms'.format(round(bot.latency, 1)))

@bot.command()
async def github(ctx):
    print("- GitHub linki istendi.")
    await ctx.send('Botun GitHub linki: https://github.com/GoktugYalcin/discord_bot')

@bot.command()
async def spotify(ctx):
    print("- Aktivite istendi.")
    userx = ctx.message.author
    for act in userx.activities:
        if act.name=="Spotify":
            await ctx.send(f"{userx.name}, şu an ***{act.name}*** üzerinden, **{act.title}** dinliyor. :musical_note:")
        elif act.name != "Spotify":
            await ctx.send(f"{userx.name}, şu an bir şarkı dinlemiyor.")

@bot.command()
async def sil(ctx, sayi=10):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
        count = int(sayi) + 1
        deleted = await ctx.message.channel.purge(limit = count)
        print(f"- {len(deleted)-1} mesaj silindi.")
        await ctx.send('{} mesaj silindi 👌'.format(len(deleted)-1))

@bot.command()
async def bilgi(ctx):
    print("- Bilgi istendi.")
    await ctx.send(f'Bot-Adi: {bot.user.name} 💡\nBot-ID: {bot.user.id} 🧭\nDiscord Versiyonu: {discord.__version__} 🛹\nBot Versiyonu: {__version__} 🎮\n')

# random sayı gerektiği zaman kendisine verilen range ve 0 arasında bir sayı döndürecek
@bot.command()
async def rastgele(ctx, arg=10):
    print("- Rastgele sayı istendi.")
    sayi = random.randint(0,int(arg))
    await ctx.send(f"İşte senin için bir sayı : {sayi}")

# komut test fonksiyonu
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
#  endregion

#  region region event_listeners
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
# katılan kullanicinin dogrulamasi
@bot.event
async def on_member_join(member):
    print(f"- {member.mention} sunucuya katıldı.")
    channel = bot.get_channel(717402901017788417)
    users = bot.users
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucuya katıldı 🤙 Üye sayısı: {lst}')

# giden kullanicinin dogrulamasi
@bot.event
async def on_member_remove(member):
    print(f"- {member.mention} sunucuyu terketti.")
    channel = bot.get_channel('YOUR_CHANNEL_ID')
    users = bot.users
    guild = member.guild
    lst = len(list(guild.members))

    await channel.send(f'{member.mention} sunucudan ayrıldı 👋 Üye sayısı: {lst+2}')


#handling kısmı
@bot.event
async def on_error(event, *args, **kwargs):
    print("- Fonksiyon hata verdi.")
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

# bot çalıştığında bot hakkında bilgiler verecek
@bot.event
async def on_ready():
    sistem = platform.system()
    print('------------------------------------')
    print('|          Bot Online!!             |')
    print(f'|Bot-Adi: {bot.user.name}          |')
    print(f'|Bot-ID: {bot.user.id}         |')
    print(f'|Discord Versiyonu: {discord.__version__}           |')
    print(f'|Bot Versiyonu: {__version__}               |')
    print(f"|Çalışılan İşletim Sistemi: {sistem} |")
    print('------------------------------------\n\n\nLog başlangıcı:\n')
#  endregion

bot.run(YOUR_TOKEN)