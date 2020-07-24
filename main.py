import os
import sys
import random
os.environ['LOGURU_AUTOINIT'] = 'False'
from loguru import logger
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from twsc_calendar import TWSCCalendar

bot = commands.Bot(command_prefix='!', help_command=None, case_insensitive=True)
tc = TWSCCalendar()

def log(msg):
    logger.info(msg)

@bot.event
async def on_ready():
    log(f'{bot.user} Ready!')

@bot.event
async def on_message(ctx):
    if ctx.content.startswith('!'):
        log(f'{ctx.author}: {ctx.content}')
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

@bot.command(name='星海比賽', aliases=['比賽', 'b', 'bracket', '賽程', '賽程表'])
async def cmd_calendar(ctx):
    await ctx.channel.send(tc.get_next_event())

@bot.command(name='下一場比賽', aliases=['nt'])
async def cmd_next(ctx):
    await ctx.channel.send(tc.get_next_event(next_only=True))

@bot.command(name='報名')
async def cmd_sign(ctx):
    await ctx.channel.send(tc.get_next_sign())

@bot.command(name='哈囉', aliases=['hello'])
async def cmd_testing(ctx):
    await ctx.channel.send(f'{ctx.author.mention} 你好啊!')

@bot.command(name='藍兔', aliases=['algs'])
async def cmd_algs(ctx):
    await ctx.channel.send('藍兔電子競技工作室臉書粉絲團\nhttps://www.facebook.com/ALGSSC2/')

@bot.command(name='星途', aliases=['pos'])
async def pos(ctx):
    await ctx.channel.send('星途(Path of Star) - 臺灣《星海爭霸II》募資邀請賽\nhttps://www.zeczec.com/projects/pathofstar')

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
    await ctx.channel.send(' <:nice:736140894927061023> '.join(nice_name) + ' <:nice:736140894927061023>')

@bot.command(name='az', aliases=['azure'])
async def cmd_az(ctx):
    await ctx.channel.send('AZ 大大的臉書粉絲團\nhttps://www.facebook.com/AzureForSC2/')

@bot.command(name='rex')
async def cmd_rex(ctx):
    await ctx.channel.send('Rex 小雷雷臉書粉絲團\nhttps://www.facebook.com/RexStorMWTF')

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
