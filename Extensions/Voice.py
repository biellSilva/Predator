import discord
import datetime
import pytz
import json
import config

from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from typing import Optional, Union
from discord.utils import get

tz_brazil = pytz.timezone('America/Sao_Paulo')


@app_commands.guild_only()
class Voice(commands.GroupCog, name='voice'):

    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='criar')
    @app_commands.describe(privacidade='Deseja uma sala Pública ou Privada?')
    @app_commands.choices(privacidade=[
        Choice(name='Pública', value=0),
        Choice(name='Privada', value=1)
    ])
    async def voice(self, interaction: discord.Interaction, privacidade: int):

        '''Crie sua sala de voz Pública ou Privada'''

        guild = interaction.guild
        user = interaction.user

        categoria = get(guild.categories, id=config.voice_categoria)
        voice_comandos = guild.get_channel(config.voice_comandos)
        member = guild.get_role(config.membro)
        visit = guild.get_role(config.visitante)

        await open_account(user)
        users = await get_data()
        sala = users[str(user.id)]['sala']

        if sala != 0:
            sala = guild.get_channel(sala)
            em = discord.Embed(color=config.roxo,
                               description=f'{user.mention}, você já possui uma sala: {sala.mention}\n'
                               f'Use `/voice config` caso queira alterá-la')
            em.set_footer(
                text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
            em.timestamp = datetime.datetime.now(tz=tz_brazil)
            await interaction.response.send_message(embed=em, ephemeral=True)

        else:
            if privacidade == 1:
                voip = await guild.create_voice_channel(f'Sala Privada [{user}]', category=categoria)

                perms = voip.overwrites_for(user)
                perms.move_members = True
                perms.view_channel = True
                perms.manage_channels = True
                perms.mute_members = True
                perms.deafen_members = True

                await voip.set_permissions(user, overwrite=perms)

                em = discord.Embed(color=config.roxo,
                                   description=f'{user.display_name}, seu canal de voz foi criado na configuração privada\n'
                                   'É permitido que altere o nome da sala para algo que goste, mas o que está entre `[]` não deve ser alterado\n'
                                   f'{voip.mention}')
                em.set_footer(
                    text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
                em.timestamp = datetime.datetime.now(tz=tz_brazil)

                users = await get_data()
                users[str(user.id)]['sala'] = voip.id
                users[str(user.id)]['privado'] = 1
                with open('./json/salas.json', 'w') as f:
                    json.dump(users, f, indent=4)

                await interaction.response.send_message(embed=em, ephemeral=True)

            else:
                voip = await guild.create_voice_channel(f'Sala Pública [{user}]', category=categoria)

                perms = voip.overwrites_for(user)
                perms.move_members = True
                perms.view_channel = True
                perms.manage_channels = True
                perms.mute_members = True
                perms.deafen_members = True

                permsMember = voip.overwrites_for(member)
                permsMember.view_channel = True

                permsVisit = voip.overwrites_for(visit)
                permsVisit.view_channel = True

                await voip.set_permissions(user, overwrite=perms)
                await voip.set_permissions(member, overwrite=permsMember)
                await voip.set_permissions(visit, overwrite=permsVisit)

                em = discord.Embed(color=config.roxo,
                                   description=f'{user.mention}, seu canal de voz foi criado na configuração pública\n'
                                   'Ao sair da sala ela será apagada\n'
                                   f'{voip.mention}')
                em.set_footer(
                    text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
                em.timestamp = datetime.datetime.now(tz=tz_brazil)

                users = await get_data()
                users[str(user.id)]['sala'] = voip.id
                users[str(user.id)]['privado'] = 0
                with open('./json/salas.json', 'w') as f:
                    json.dump(users, f, indent=4)

                await interaction.response.defer(embed=em, ephemeral=True)
                await voice_comandos.send(embed=em)

    @app_commands.command(name='config')
    @app_commands.describe(tipo='Adicionar/Remover o acesso livre do membro. Deletar: Apaga sua sala de voz', membro='Adicionar/Remover um membro ou cargo')
    @app_commands.choices(tipo=[
        Choice(name='Adicionar membro', value='add'),
        Choice(name='Remover membro', value='rem'),
        Choice(name='Deletar', value='del')
    ])
    async def voice_add(self, interaction: discord.Interaction, tipo: str, membro: Optional[Union[discord.User, discord.Role]]):

        '''Configure sua sala de voz'''

        guild = interaction.guild
        user = interaction.user
        users = await get_data()
        sala = users[str(user.id)]['sala']
        sala = guild.get_channel(sala)

        if 'add' in tipo:
            if membro != None:
                perms = sala.overwrites_for(membro)
                perms.view_channel = True
                await sala.set_permissions(membro, overwrite=perms)

                em = discord.Embed(
                    color=config.roxo, description=f'{membro.mention} foi adicionado a seu canal: {sala.mention}')
                em.set_footer(
                    text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
                em.timestamp = datetime.datetime.now(tz=tz_brazil)
                await interaction.response.send_message(embed=em, ephemeral=True)

            else:
                await interaction.response.send_message(f'{user.display_name}, você esqueceu de informar o membro', ephemeral=True)

        if 'rem' in tipo:
            if membro != None:
                perms = sala.overwrites_for(membro)
                perms.view_channel = False
                await sala.set_permissions(membro, overwrite=perms)

                em = discord.Embed(
                    color=config.roxo, description=f'{membro.display_name} foi removido de seu canal: {sala.mention}')
                em.set_footer(
                    text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
                em.timestamp = datetime.datetime.now(tz=tz_brazil)
                await interaction.response.send_message(embed=em, ephemeral=True)

            else:
                await interaction.response.send_message(f'{user.display_name}, você esqueceu de informar o membro', ephemeral=True)

        if 'del' in tipo:
            em = discord.Embed(color=config.roxo,
                               description=f'{user.display_name}, sua sala foi deletada como pediu.\n{sala.mention}')
            em.set_footer(text=f'Registrado em {guild}',
                          icon_url=f'{guild.icon}')
            em.timestamp = datetime.datetime.now(tz=tz_brazil)

            users = await get_data()
            sala_id = users[str(user.id)]['sala']

            sala = guild.get_channel(sala_id)
            await sala.delete(reason=f'{user} voice privado')

            users[str(user.id)]['sala'] = 0
            users[str(user.id)]['privado'] = 0
            with open('./json/salas.json', 'w') as f:
                json.dump(users, f, indent=4)

            await interaction.response.send_message(embed=em, ephemeral=True)

    @app_commands.command(name='staff')
    @app_commands.describe(membro='Remove a sala do membro')
    @app_commands.checks.has_role(config.Lorde)
    async def staff_remove(self, interaction: discord.Interaction, membro: discord.Member):

        '''Reseta o ID de voice privado'''

        guild = interaction.guild

        em = discord.Embed(color=config.roxo,
                           description=f'{membro.display_name}, teve seu id de sala resetado')
        em.set_footer(text=f'Registrado em {guild}',
                      icon_url=f'{guild.icon}')
        em.timestamp = datetime.datetime.now(tz=tz_brazil)

        users = await get_data()
        users[str(membro.id)]['privado'] = 0
        users[str(membro.id)]['sala'] = 0
        with open('./json/salas.json', 'w') as f:
            json.dump(users, f, indent=4)

        await interaction.response.send_message(embed=em, ephemeral=True)

    @staff_remove.error
    async def staff_remove_error(self, interaction: discord.Interaction, err):
        if isinstance(err, app_commands.MissingRole):
            lorde = interaction.guild.get_role(config.Lorde)
            await interaction.response.send_message(f'Você não é um {lorde.mention}', ephemeral=True)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = self.bot.get_guild(config.uniao)

        try:
            users = await get_data()
            sala = users[str(member.id)]['sala']
            privado = users[str(member.id)]['privado']

            if privado == 1:
                return

            if member.id == users[str(member.id)]['id']:
                if after.channel is None or (before.channel is not None and after.channel is not None):
                    if before.channel.id == sala:
                        canal = guild.get_channel(sala)
                        voice_comandos = guild.get_channel(config.voice_comandos)

                        em = discord.Embed(color=config.roxo, description=f'{member.mention}, seu canal de voz público foi deletado pois você o deixou')
                        em.set_footer(text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
                        em.timestamp = datetime.datetime.now(tz=tz_brazil)

                        await voice_comandos.send(embed=em)
                        await canal.delete()

                        sala = users[str(member.id)]['sala'] = 0
                        with open('./json/salas.json', 'w') as f:
                            json.dump(users, f, indent=4)
        except KeyError:
            return


async def open_account(user):

    users = await get_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]['nome'] = str(user.name)
        users[str(user.id)]['id'] = user.id
        users[str(user.id)]['privado'] = 0
        users[str(user.id)]['sala'] = 0

    with open('./json/salas.json', 'w') as f:
        json.dump(users, f, indent=4)
        return True


async def get_data():
    with open('./json/salas.json', 'r') as f:
        users = json.load(f)
    return(users)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
