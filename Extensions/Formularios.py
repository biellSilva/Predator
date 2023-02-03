import discord
import datetime
import config
import random

from discord.ext import commands, tasks
from discord import app_commands, Interaction


class Exame(discord.ui.Modal, title='Exame Cósmico'):
    warframe = discord.ui.TextInput(label='Warframe', required=True, placeholder='Nome#000')
    cargo = discord.ui.TextInput(label='Cargo de Interesse', required=True, placeholder='Decorador / Recrutador / Moderador')
    extra = discord.ui.TextInput(label='Extras', style=discord.TextStyle.paragraph, required=False, placeholder='Ajudarei a staff com o que puder')

    async def on_submit(self, interaction: Interaction):
        guild = interaction.guild
        author = interaction.user
        formChannel = guild.get_channel(config.exame_cosmico)
        cargo = next((cargo for cargo in author.roles if 'tenno de' in cargo.name.lower()), None)

        if cargo == None:
            await interaction.response.send_message(f'Você não é um membro da União Cósmica', ephemeral=True)
            return

        em = discord.Embed(title='Exame Cósmico',
                           color=config.roxo,
                           description= f'**Warframe:** {self.warframe}\n'
                                        f'**Discord:** {author.mention}\n'
                                        f'**Discord ID:** {author.id}\n'
                                        f'**Clã:** {cargo.mention}\n'
                                        f'**Cargo de Interesse:** {self.cargo}\n'
                                        f'**Extra:** {self.extra}',
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))
        
        em.set_author(name=author, url=author.display_avatar.url)
        em.set_thumbnail(url=author.display_avatar.url)
        em.set_footer(text=guild.name, icon_url=guild.icon.url)

        await formChannel.send(embed=em)
        await interaction.response.send_message(f'Registro enviado', embed=em, ephemeral=True)


class Denuncia(discord.ui.Modal, title='Registro de Denúncia'):
    warframe = discord.ui.TextInput(label='Warframe', required=False, placeholder='Nome#000')
    discord_name = discord.ui.TextInput(label='Discord', required=False, placeholder='Nome#000')
    razao = discord.ui.TextInput(label='Motivo da denúncia', style=discord.TextStyle.paragraph, required=True, placeholder='Xingamentos')

    async def on_submit(self, interaction: Interaction):
        guild = interaction.guild
        formChannel = guild.get_channel(config.formularios)

        em = discord.Embed(title='Registro de Denúncia',
                           color=config.roxo,
                           description=f'**Warframe:** {self.warframe}\n'
                                       f'**Discord:** {self.discord_name}\n'
                                       f'**Razão:** {self.razao}',
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))

        em.set_thumbnail(url=guild.icon)
        em.set_footer(text=guild.name, icon_url=guild.icon.url)

        await formChannel.send(embed=em)
        await interaction.response.send_message(f'Registro enviado para a moderação', embed=em, ephemeral=True)


class Criador(discord.ui.Modal, title='Criador de Conteúdo'):
    warframe = discord.ui.TextInput(label='Warframe', required=True, placeholder='Nome#000')
    youtube = discord.ui.TextInput(label='Youtube', required=False, placeholder='https://youtube.com/user')
    twitch = discord.ui.TextInput(label='Twitch', required=False, placeholder='https://twitch.tv/user')
    razao = discord.ui.TextInput(label='Informações Extras', style=discord.TextStyle.paragraph, required=False, placeholder='Stream de Warframe 8 horas por dia')

    async def on_submit(self, interaction: Interaction):
        guild = interaction.guild
        author = interaction.user
        formChannel = guild.get_channel(config.formularios)

        em = discord.Embed(title='Criador de Conteúdo',
                           color=config.roxo,
                           description=f'**Warframe:** {self.warframe}\n'
                           f'**Twitch:** {self.twitch}\n'
                           f'**Youtube:** {self.youtube}'
                           f'**Extras:** {self.razao}\n\n'
                           f'{author.mention} - {author.id}',
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))

        em.set_thumbnail(url=author.display_avatar.url)
        em.set_footer(text=guild.name, icon_url=guild.icon)

        await formChannel.send(embed=em)
        await interaction.response.send_message(f'Registro enviado para a moderação', embed=em, ephemeral=True)


@app_commands.guild_only()
class Formularios(commands.GroupCog, name='forms'):
    '''Comando dos Formulários'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        self.anuncio.start()

    def cog_unload(self):
        self.anuncio.stop()

    @tasks.loop(hours=1)
    async def anuncio(self):
        await self.bot.wait_until_ready()

        if datetime.datetime.now(tz=config.tz_brazil).hour not in (2, 8, 14, 20):
            return

        guild = self.bot.get_guild(config.uniao)
        warframe_chat = guild.get_channel(config.warframe_chat)

        txt_1 = ('Interessado em Ajudar a Aliança? Estamos procurando por jogadores que desejam contribuir para a comununidade, jogadores que possam participar efetivamente na aliança e ajudar outros jogadores.\n'
                'Faça o Exame Cósmico -> </forms exame:1042305650472005716>')

        txt_2 = ('Aos membros da União Cósmica com objetivo de colaborar com o desenvolvimento dos clãs e da aliança de diversas formas.\n'
                 'Clique aqui -> </forms exame:1042305650472005716>')

        em = discord.Embed(color=config.cinza,
                           description=random.choice([txt_1, txt_2]),
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))
        em.set_footer(text=guild.name, icon_url=guild.icon.url)

        await warframe_chat.send(embed=em)
    

    @app_commands.command(name='denuncia')
    async def report(self, interaction: discord.Interaction):
        '''Pode denúnciar um membro do Warframe ou Discord'''
        await interaction.response.send_modal(Denuncia(timeout=600))

    @app_commands.command(name='criador')
    async def criador(self, interaction: discord.Interaction):
        '''Faz um pedido pelos cargos de Streamer e/ou Youtuber'''
        await interaction.response.send_modal(Criador(timeout=600))

    @app_commands.command(name='exame')
    async def exame(self, interaction: discord.Interaction):
        '''Exame Cósmico para se tornar um staff'''
        await interaction.response.send_modal(Exame(timeout=600))


async def setup(bot):
    await bot.add_cog(Formularios(bot))
