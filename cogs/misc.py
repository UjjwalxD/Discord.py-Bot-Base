import discord 
from discord.ext import commands 


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot =bot
    
    
    @commands.hybrid_command(name="ping", description="ping")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        await ctx.send(round(self.bot.latency*1000))        
        
async def setup(bot)->None:
    await bot.add_cog(Misc(bot))