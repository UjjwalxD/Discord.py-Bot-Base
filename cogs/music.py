import discord
from discord.ext import commands 
import wavelink 



#
#  Fill lavalink node at client.py and use version 4 lavalink. (wavelink 3.4)
# basic lavamusic bot in python

class LavaMusic(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._volume = 100 
        self.autoplay = wavelink.AutoPlayMode.partial
        self.source = "ytsearch"
    async def next(self):
        await super().skip(force=True)
    async def remove_player(self):
        self.autoplay = wavelink.AutoPlayMode.partial
        self.queue.clear()
        await self.stop()
        await self.disconnect()
                
        
    
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
################################################################################

    @commands.Cog.listener()
    async def on_wavelink_track_start(self , payload : wavelink.TrackStartEventPayload):
        player : LavaMusic = payload.player
        track = payload.track
        original = payload.original
        
        if hasattr(original , 'requestor'):
            requestor = original.requestor
        else:
            requestor = player.client.user
            
        embed = discord.Embed()
        embed.color = discord.Color.dark_embed()
        embed.title = f"Now Playing: {player.current.title}"
        embed.description = f"- Track: **[{player.current.title}]({player.current.uri})**\n- Artist: **{player.current.author}**"
        embed.set_footer(text=f"Volume: {player.volume}, Requested by {requestor.name}")
        
        try:
            player.msg= await player.home.send(embed=embed)
        except Exception as e:
            await player.home.send(e)
    
    @commands.Cog.Listener()
    async def on_wavelink_track_end(self, payload : wavelink.TrackEndEventPayload):
        player: LavaMusic = ctx.voice_client 
        try:
            await player.msg.delete()
            
        except Exception as e:
            print(e)
            await player.home.send(e)
        


################################################################################
        
    @commands.hybrid_command()
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        if not ctx.guild:return
        player: LavaMusic = ctx.voice_client
        if player and ctx.author.voice.channel:
            if ctx.author.voice.channel.id != player.channel.id:
                return await ctx.send(f'You`re not connected same voice channel as me.')
        if not player:
            try:
                player : LavaMusic = await ctx.author.voice.channel.connect(cls=LavaMusic , self_deaf=True)
            except AttributeError:
                return await ctx.send("Please join a voice channel first before using this command.")
            except discord.ClientException:
                return await ctx.send("I was unable to join this voice channel. Please try again.")
        if not hasattr(player, "home"):
            player.home = ctx.channel
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
            return
        if isinstance(tracks, wavelink.Playlist):
            for track in tracks.tracks:
                track.requestor = ctx.author
            added: int = await player.queue.put_wait(tracks)
            await ctx.reply(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            track.requestor = ctx.author
            await player.queue.put_wait(track)
            await ctx.reply(f"Added **`{track}`** to the queue.")

        if not player.playing:
            await player.play(player.queue.get(), add_history = True)
            
            
    @commands.hybrid_command()
    async def skip(self, ctx):
        player: LavaMusic = ctx.voice_client
        if not player:
            return await ctx.reply('I`m not connected to any voice channel.')
        if player and ctx.author.voice.channel:
            if ctx.author.voice.channel.id != player.channel.id:
                return await ctx.reply(f"You`re not connected as same as me, {player.channel.mention}.")
        if not getattr(ctx.author , 'voice' , 'channel'):
            return await ctx.reply('You need to be in a voice channel to use this command.')
        if not player.playing:
            return await ctx.reply('I`m not playing anything to skip.')
        else:
            await player.next()
            await ctx.reply('Sucessfully skipped your current track.')
    
    @commands.hybrid_command()
    async def volume(self, ctx, volume:int):
        player: LavaMusic = ctx.voice_client
        if not player:
            return await ctx.reply('I`m not connected to any voice channel.')
        if player and ctx.author.voice.channel:
            if ctx.author.voice.channel.id != player.channel.id:
                return await ctx.reply(f"You`re not connected as same as me, {player.channel.mention}.")
        if not getattr(ctx.author , 'voice' , 'channel'):
            return await ctx.reply('You need to be in a voice channel to use this command.')
        if not player.playing:
            return await ctx.reply('I`m not playing anything to skip.')
        else:
            if volume > 300:
                return await ctx.reply('Volume value should be in the range of 300.')
            await player.set_volume(volume)
            await ctx.reply(f'Volume is now: **{volume}**')
    
    @commands.hybrid_command()
    async def stop(self, ctx):
        player: LavaMusic = ctx.voice_client
        if not player:
            return await ctx.reply('I`m not connected to any voice channel.')
        if player and ctx.author.voice.channel:
            if ctx.author.voice.channel.id != player.channel.id:
                return await ctx.reply(f"You`re not connected as same as me, {player.channel.mention}.")
        if not getattr(ctx.author , 'voice' , 'channel'):
            return await ctx.reply('You need to be in a voice channel to use this command.')
        await player.remove_player()
        await ctx.reply('I have stopped the music.')
            
    
                
            


    
        
    
    
        
    
    
async def setup(bot)->None:
    await bot.add_cog(Music(bot))
