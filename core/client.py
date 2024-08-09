import discord , os , random , jishaku , requests
import wavelink
from wavelink import NodeReadyEventPayload
from utility.logger import logger
from discord.ext import commands , tasks 
from dotenv import load_dotenv 
from utility.database import database
load_dotenv()





class Client(commands.AutoShardedBot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),       intents=intents,        help_command=None)
        self.owner_ids = []
        self.session = requests.Session() # You can use session without importing it again n again.
    
    async def on_ready(self) -> None:
        logger(f"[Ready] Logged in as : {self.user.name}","green")
    
    
    
    @tasks.loop(minutes=1.1)
    async def statuses(self) -> None:
        xd = ["Made By Ujjwal", "github/UjjwalxD", "discord.gg/winklemusic"]
        await self.change_presence(activity=discord.Game(random.choice(xd)))   
        
        
        
    
    async def on_wavelink_node_ready(self, payload: NodeReadyEventPayload) -> None:
        print("Wavelink Node connected: %r | Resumed: %s", payload.node, payload.resumed)

    
    @statuses.before_loop
    async def before_statuses_task(self) -> None:
        await self.wait_until_ready()
    
    async def setup_hook(self)->None:
        nodes = [wavelink.Node(uri="http://lavalink01.techbyte.host:2005/", password="NAIGLAVA-dash.techbyte.host")]
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)
        database()
        self.statuses.start()
        await self.load_extension('jishaku')
        await self.tree.sync()
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py'):
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger(f'[Loaded] `{filename}`', "blue")
            except Exception as e:
                logger(e, "blue")
    
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)
        
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed()
            embed.color = discord.Color.red()
            embed.description = f"Calm down!, use this again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}"
            await ctx.send(embed=embed, delete_after=6)       




client = Client()
client.run(os.getenv("TOKEN"))



########################
# for help dm me on discord or join server https://discord.gg/winklemusic
