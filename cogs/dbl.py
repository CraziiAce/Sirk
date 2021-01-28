import discord, json
from discord.ext import commands, tasks

File = "tools/config.json"
with open(File) as f:
    data = json.load(f)
space = data['SPACE']

class dbl(commands.Cog):
    '''Discord Bot Lists Commands/Tasks'''
    def __init__(self, bot):
        self.bot = bot
        self.space.start()
        
    @tasks.loop(minutes=30.0)
    async def space(self):
        '''
        BOTLIST.SPACE
        https://botlist.space
        '''
        url = "https://api.botlist.space/v1/bots/751447995270168586"
        headers = {"Authorization": space, "Content-Type": 'application/json'}
        try:
            r = await self.bot.session.post(url, headers=headers, data=json.dumps({'server_count': len(self.bot.guilds)}))
            result = json.loads(await r.text())
            message = result['message']
            c = self.bot.get_channel(803413039256043590)
            await c.send(f"__**BotList.Space**__ - {message} **({len(self.bot.guilds)})**")
        except:
            pass
        
def setup(bot):
    bot.add_cog(dbl(bot))
