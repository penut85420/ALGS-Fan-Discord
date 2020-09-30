import os
import sys
import random
os.environ['LOGURU_AUTOINIT'] = 'False'
import discord
from loguru import logger
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from twsc_calendar import TWSCCalendar
from liquipedia import search_next

activity = discord.Activity(
    name='輸入 @藍兔小粉絲',
    type=discord.ActivityType.playing
)

bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    case_insensitive=True,
    activity=activity
)

activity = discord.Activity(
    name='輸入 @藍兔小粉絲',
    type=discord.ActivityType.playing
)

bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    case_insensitive=True,
    activity=activity
)

tc = TWSCCalendar()
samatch_str = json.load(open('./samatch.json', 'r', encoding='UTF-8'))

def log(msg):
    logger.info(msg)

async def get_channel(chid):
    for ch in bot.get_all_channels():
        if ch.id == chid:
            await ch.send('Restarting done.')
            break

@bot.event
async def on_ready():
    log(f'{bot.user} Ready!')
    if os.path.exists('flag'):
        chid = int(open('flag', 'r').read())
        await get_channel(chid)
        os.remove('flag')

@bot.event
async def on_message(ctx):
    msg = ctx.content.replace('\n', ' ')

    if ctx.content.startswith('!'):
        log(f'{ctx.author}: {msg}')

    if ctx.author == bot.user:
        log(f'{ctx.author}: {msg}')

    if bot.user in ctx.mentions:
        await ctx.channel.send(
            '`!近期比賽` 可以列出最近的星海比賽\n'
            '`!近期可報名` 可以列出最近可以報名的星海比賽\n\n'
            '其他指令請參考 https://git.io/JJuba'
        )

    await commands.Bot.on_message(bot, ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    log(str(error).replace('\n', ' | '))

@bot.command(name='近期比賽')
async def cmd_recent(ctx):
    await ctx.channel.send(
        '【近期賽事資訊】\n\n'
        f'{tc.get_recent_events()}\n\n'
        'TWSC 星海賽事行事曆\n'
        '<http://bit.ly/TWSCSC2CAL>\n'
        'ALGS 藍兔電子競技工作室 Twitch\n'
        'https://www.twitch.tv/algs_sc2\n'
        'AfreecaTV 艾菲卡 GSL 中文台\n'
        '<http://play.afreecatv.com/gsltw>\n'
        'AfreecaTV 艾菲卡臺灣星海中文轉播台\n'
        '<http://play.afreecatv.com/aftwsc2>\n'
    )

@bot.command(name='近期可報名')
async def cmd_recent_sign(ctx):
    await ctx.channel.send(
        '【近期可報名賽事】\n\n'
        f'{tc.get_recent_sign()}\n\n'
        '若需要協助請洽 https://discord.gg/SwX9KMj'
    )

@bot.command(name='星海比賽', aliases=['比賽', 'b', 'bracket', '賽程', '賽程表'])
async def cmd_calendar(ctx):
    await ctx.channel.send(tc.get_next_event())

@bot.command(name='下一場比賽', aliases=['nt'])
async def cmd_next(ctx):
    await ctx.channel.send(tc.get_next_event(next_only=True))

@bot.command(name='報名')
async def cmd_sign(ctx):
    await ctx.channel.send(tc.get_next_sign())

@bot.command(name='samatch')
async def samatch(ctx):
    await ctx.send(samatch_str['samatch'])

@bot.command(name='pov')
async def pov(ctx):
    await ctx.send(samatch_str['pov'])

@bot.command(name='哈囉', aliases=['hello'])
async def cmd_testing(ctx):
    await ctx.channel.send(f'{ctx.author.mention} 你好啊!')

@bot.command(name='藍兔', aliases=['algs'])
async def cmd_algs(ctx):
    await ctx.channel.send('藍兔電子競技工作室臉書粉絲團\nhttps://www.facebook.com/ALGSSC2/')

@bot.command(name='星途', aliases=['pos'])
async def pos(ctx):
    await ctx.channel.send('星途(Path of Star) - 臺灣《星海爭霸II》募資邀請賽\nhttps://www.zeczec.com/projects/pathofstar')

@bot.command(name='召喚')
async def cmd_summon(ctx, *arg):
    player = ' '.join(arg).strip()
    if player == '':
        await ctx.channel.send('指令格式：`!召喚 [選手名稱]`')
        return

    result = search_next(player)
    if result is not None:
        await ctx.channel.send(result)
    else:
        await ctx.channel.send(f'沒有找到 {player} 最近的比賽 QQ')

@bot.command(name='nice')
async def cmd_nice(ctx):
    nice_name = [
        '死亡鳳凰艦隊提督',
        '抓放軍團最高統帥',
        '冰雪風暴靜滯領主',
        '亞細亞洲璀銀神帝',
        '極限大師廿八星宿',
        '四大毒奶堅持天尊'
    ]
    msg = ' <:nice:736140894927061023> '.join(nice_name) + ' <:nice:736140894927061023>'

    next_match = search_next('nice')
    if next_match is not None:
        msg = f'{msg}\n{next_match}'

    await ctx.channel.send(msg)

@bot.command(name='has')
async def cmd_has(ctx):
    msg = 'Has 臉書粉絲團\nhttps://www.facebook.com/SC2Has-273980189818092/'
    next_match = search_next('has')
    if next_match is not None:
        msg = f'{msg}\n{next_match}'

    await ctx.channel.send(msg)

@bot.command(name='hui')
async def cmd_hui(ctx):
    await ctx.channel.send('輝哥臉書粉絲團\nhttps://www.facebook.com/hui379/')

@bot.command(name='sobad')
async def cmd_sobad(ctx):
    await ctx.channel.send('師哥臉書粉絲團\nhttps://www.facebook.com/rushsobad')

@bot.command(name='az', aliases=['azure'])
async def cmd_az(ctx):
    await ctx.channel.send('AZ 大大的臉書粉絲團\nhttps://www.facebook.com/AzureForSC2/')

@bot.command(name='rex')
async def cmd_rex(ctx):
    msg = 'Rex 小雷雷臉書粉絲團\nhttps://www.facebook.com/RexStorMWTF'
    next_match = search_next('rex')
    if next_match is not None:
        msg = f'{msg}\n{next_match}'

    await ctx.channel.send(msg)

@bot.command(name='阿吉')
async def cmd_ahchi(ctx):
    await ctx.channel.send('恭迎吉孤觀音⎝༼ ◕д ◕ ༽⎠ 渡世靈顯四方⎝༼ ◕д ◕ ༽⎠')

@bot.command(name='top')
async def cmd_top(ctx):
    await ctx.channel.send('吃我的大火球～～～')

@bot.command(name='堅持')
async def cmd_persist(ctx):
    await ctx.channel.send('你在堅持啥啊')

@bot.command(name='提告', aliases=['sue'])
async def cmd_sue(ctx):
    await ctx.channel.send('Nice：「不排除提告」（設計對白）')

@bot.command(name='錯覺', aliases=['illusion'])
async def cmd_illusion(ctx):
    await ctx.channel.send('你從什麼時候開始產生了你這盤能贏的錯覺？')

@bot.command(name='藉口', aliases=['excuse'])
async def cmd_excuse(ctx):
    await ctx.channel.send('成功的人找方法，失敗的人找藉口。')

def check_auth(ctx):
    if ctx.guild.id != int(os.getenv('AUTH_GUILD')):
        return False

    if ctx.author.id != int(os.getenv('AUTH_USER')):
        return False

    return True

@bot.command(name='bye')
@commands.check(check_auth)
async def cmd_bye(ctx):
    await ctx.channel.send('Bye!')
    await bot.logout()
    await bot.close()

@bot.command(name='r')
@commands.check(check_auth)
async def cmd_bye(ctx):
    await ctx.channel.send('Restarting...')
    open('flag', 'w').write(f'{ctx.channel.id}')
    await bot.logout()
    await bot.close()

def set_logger():
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | '
        '<lvl>{level: ^9}</lvl> | '
        '{message}'
    )
    logger.add(sys.stderr, level='INFO', format=log_format)
    logger.add(
        f'./logs/algs.log',
        rotation='7 day',
        retention='30 days',
        level='INFO',
        encoding='UTF-8',
        format=log_format
    )

if __name__ == '__main__':
    set_logger()
    bot.run(os.getenv('TOKEN'))
