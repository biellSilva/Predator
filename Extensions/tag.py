import discord
import os
import json
import config
import datetime

from discord.ext import commands
from discord import app_commands


class Registro(discord.ui.Modal, title='Build Add'):
    nome = discord.ui.TextInput(label='Nome da Build', placeholder='Wisp Eidolon')
    categoria = discord.ui.TextInput(label='Categoria', placeholder='Warframe / Primaria / Secundaria / Meele / Pet / Necramech / Railjack')
    content = discord.ui.TextInput(label='Build', style=discord.TextStyle.paragraph, placeholder='Texto explicando sua build, pode conter links do discord', max_length=10000)

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        dev_embed = guild.get_channel(config.test_dev_embed)
        reg = guild.get_channel(config.registro_de_punicao)
        em = discord.Embed(title='Registro de Punição',
                           color=config.roxo,
                           description=f'**Warframe:** {self.warframe}\n'
                                       f'**Discord:** {self.discord_id}\n'
                                       f'**Local:** {self.local}\n'
                                       f'**Punição:** {self.punicao}\n'
                                       f'**Razão:** {self.razao}\n',
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))

        em.set_thumbnail(url=guild.icon)
        em.set_footer(
            text=f'Registrado por {user}', icon_url=user.display_avatar.url)

        await reg.send(embed=em)
        await interaction.response.send_message(f'Registro enviado', embed=em, ephemeral=True)


class TagCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        if not os.path.exists('./json/tag.json'):
            with open('./json/tag.json', 'w') as f:
                json.dump({}, f, indent=4)


    @commands.hybrid_group(name='tag')
    async def tag(self, ctx: commands.Context, pesquisa: str):
        '''Sistema de Tags'''

        print('Tag: ', ctx.author.display_name, ctx.channel.name)

        tag = await get_tag_data()

        for tag_name in tag:
            if tag_name == pesquisa.lower():
                await ctx.send(tag[tag_name]['tag_message'])


    @tag.command(name='add')
    async def tag_add(self, ctx: commands.Context, nome: str, *, texto: str):
        '''Adiciona Tag'''

        print('Tag add: ', ctx.author.display_name, ctx.channel.name)

        tag = await get_tag_data()
        
        em = discord.Embed()
        
        if nome.lower() not in tag:
            '''Tag Name não existe'''
            tag[nome.lower()] = {}
            tag[nome.lower()]['tag_author'] = ctx.author.id
            tag[nome.lower()]['tag_message'] = texto

            with open('./json/tag.json', 'w') as f:
                json.dump(tag, f, indent=4)

            
                
                


    @tag.command(name='del')
    async def tag_del(self, ctx: commands.Context, id: int):
        '''Apaga Tag'''
        print('Tag del: ', ctx.author.display_name, ctx.channel.name)

    @tag.command(name='edit')
    async def tag_edit(self, ctx: commands.Context, id: int):
        '''Edit Tag'''
        print('Tag edit: ', ctx.author.display_name, ctx.channel.name)

    @tag.command(name='find')
    async def tag_find(self, ctx: commands.Context, pesquisa: int):
        '''Find Tag'''
        print('Tag find: ', ctx.author.display_name, ctx.channel.name)
        

async def create_tag_json(tag_name: str):

    ''' Entra no wish alerta do mudae '''

    tag = await get_tag_data()

    if tag_name in tag:
        return False

    else:
        tag[tag_name] = {}
        tag[tag_name]['tag_author'] = None
        tag[tag_name]['tag_message'] = None

    with open('./json/tag.json', 'w') as f:
        json.dump(tag, f, indent=4)
        return True


async def get_tag_data():

    ''' Lê todo o arquivo mudae wish json '''

    with open('./json/tag.json', 'r') as f:
        tag = json.load(f)
    return tag


async def setup(bot):
    await bot.add_cog(TagCommand(bot))
