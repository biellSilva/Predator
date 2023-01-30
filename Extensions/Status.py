import discord
import datetime
import config
import discloud
import os
import dotenv
import time

from discord.ext import commands
from discord import app_commands
from typing import Optional

dotenv.load_dotenv(dotenv.find_dotenv())
discloudClient = os.getenv('discloudClient')
Predator_APP = os.getenv('appIdPredator')
client = discloud.Client(discloudClient)


class botStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    status = app_commands.Group(name='status', description='Checa o perfil de algo', guild_only=True)


    @status.command(name='bot')
    async def bot_status(self, interaction: discord.Interaction):
        ''' Checa o status do bot '''

        await interaction.response.defer(ephemeral=True, thinking=True)

        user = interaction.user
        guild = interaction.guild

        lider = guild.get_role(config.Lider)
        dev = guild.get_role(config.mecanico)

        if (lider not in user.roles) and (dev not in user.roles):
            await interaction.edit_original_response(content=f'{user.mention}, você não é um {lider.mention}')
            return

        bot_discloud = await client.app_info(target=Predator_APP)

        guild_info = ''
        i = 1
        for guilds in self.bot.guilds:
            guild_info += f'\n{i}: {guilds.name} - {guilds.member_count} membros'
            i += 1
        
        data = time.mktime(datetime.datetime.strptime(
            str(bot_discloud.start_date), '%d-%m-%Y %H:%M:%S').timetuple())

        data = int(data) - 10800
        
        em = discord.Embed(title='Bot Status',
                           color=config.roxo,
                           description=f'''
                           **Nome:** {self.bot.user}
                           **ID:** {bot_discloud.id}
                           **Status:** {bot_discloud.status}

                           **CPU:** {bot_discloud.cpu}
                           **RAM:** {bot_discloud.memory.using} | {bot_discloud.memory.available}
                           **SSD:** {bot_discloud.ssd}
                           **Ultimo reinicio:** <t:{data}:R>
                           **Network:** Up: {bot_discloud.net_info.upload} | Down: {bot_discloud.net_info.download}
                           **Ping:** {round(self.bot.latency * 1000)}ms

                           **Servidores:** {guild_info}''',
                           timestamp=datetime.datetime.now(config.tz_brazil))
        em.set_footer(text=f'Usado em {guild.name}', icon_url=guild.icon.url)

        await interaction.edit_original_response(embed=em)


async def setup(bot):
    await bot.add_cog(botStatus(bot))
