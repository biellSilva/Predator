import discord
import datetime
import asyncio
import random
import os
import requests
import config

from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from typing import Optional
from bs4 import BeautifulSoup


images = os.path.join(os.getcwd(), "./imagens/wiki")


def arquivoWiki():
    return os.path.join(images, random.choice(os.listdir(images)))


@app_commands.guild_only()
class openCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='avatar')
    @app_commands.describe(member='Selecione um membro')
    async def avatar(self, interaction: discord.Interaction, member: Optional[discord.Member]):

        ''' Envia o avatar/icone de um membro '''

        user = interaction.user

        if member == None:

            em = discord.Embed(
                title=f'Avatar de {user.display_name}', color=config.roxo)
            em.set_image(url=user.display_avatar)
            em.set_footer(text=f'Autor: {user}')
            em.timestamp = datetime.datetime.now(tz=config.tz_brazil)
            await interaction.response.send_message(embed=em, ephemeral=True)

        else:
            em = discord.Embed(
                title=f'Avatar de {member.display_name}', color=config.roxo)
            em.set_image(url=member.display_avatar)
            em.set_footer(text=f'Autor: {user}')
            em.timestamp = datetime.datetime.now(tz=config.tz_brazil)
            await interaction.response.send_message(embed=em, ephemeral=True)

    @app_commands.command(name='banir')
    @app_commands.describe(member='Selecione um membro', reason='Sem uma razão informada, escolherei uma aleatoria será escolhida')
    async def ban(self, interaction: discord.Interaction,  member: discord.Member, reason: Optional[str]):

        ''' Bane o membro '''

        user = interaction.user
        guild = interaction.guild

        if member.id == 597036489074802698:
            await interaction.response.send_message('Não posso me banir, ficou maluco? Quem vai perturbar os outros no meu lugar, você?')
            return

        if member.id == 657297392860790794:
            await interaction.response.send_message('Não posso banir meu irmão, ele é meu trouxa de teste')
            await asyncio.sleep(0.5)
            await interaction.followup.send('digo, boneco de teste <:Kekw:722633936106291200>')
            return

        if member == user:
            await interaction.response.send_message('Olha, existe um número que você deve ligar quando se sentir triste, não posso lhe banir <:Pow:632993254891192410>')
            return

        if reason == None:
            reasonList = ['Por ser corno', 'Gado demais', 'Jogador de warframe', 'Wisp lover', 'Grendel lover', 'Mas pq não?', 'Minha mãe mandou', 'Usuário de Inaros',
                          'Não gostou da guerra', 'To ficando sem ideias', 'Deu vontade', 'Ele mereceu', 'Duvidou da beleza do haisen', 'Não gostavamos dele',
                          'Teve a brilhante ideia de falar mal da entidade', 'Procurou por isso', 'Aah, o heid que pediu', 'Deve ter xingado a staff', 'Não sei, não me contaram o motivo',
                          'Esse não volta mais', 'Sinceramente? até que gostei', 'Não sei, talvez foi problema na cpu', 'Colocou feijão por baixo do arroz', 'Colocou ketchup na pizza',
                          'Entrou na defesa usando slow Nova', 'Jogou de Inaros', 'Mencionou o Conclave', 'Usa magnético na Astilla', 'Pegou build no Overframe', 'Postou build de Youtuber',
                          'Negou a Segunda Guerra', 'Não louvou nosso Lorde e Salvador\n||não me pergunte quem é, não faço ideia||', 'Escuta Pablo pela manhã', 'Ousou comprar platina',
                          'Colocou açucar no café', 'Perguntou se tinha Adoçante', 'Escondeu o controle da TV', 'Esqueceu de alimentar o Kubrow', 'Joga League of Legends', 'Falou de Futebol',
                          'Não fez carinho no Kavat', 'Reclamou de uma drop rate "baixa" mas na verdade era 10%', 'Postou o proibidíssimo gif do Elon Musk', 'Sugeriu emote que não era de Warframe', 'Pintou as paredes do Andromeda de verde', 'Pixou o dojo do Lyra com "Aquila esteve aqui"', 'Colocou adesivos de "Vote no Orion" nas janelas do Aquila',
                          'Tentou convencer um Moderador do Orion para se juntar ao Andromeda', 'Esse mono Inaros pisou na merda do meu pé!', 'Achou a Copa do mundo boa. Não me importa qual foi', 'Removeu o 2 da Wisp', 'Gloom na Nova speed', 'Trocou o 2 da Saryn', 'Tirou o 3 do Nezha']

            em = discord.Embed(title='Registro de Punição',
                               color=config.roxo,
                               description=f'{user.display_name} baniu {member.mention} do servidor!\n'
                               f'Razão: {random.choice(reasonList)}')
            em.set_thumbnail(
                url='https://cdn.discordapp.com/emojis/716678272338886716.webp')
            em.set_footer(
                text=f'Registrado por {guild}', icon_url=f'{guild.icon}')
            em.timestamp = datetime.datetime.now(tz=config.tz_brazil)

            await interaction.response.send_message(embed=em)

        else:
            em = discord.Embed(title='Registro de Punição',
                               color=config.roxo,
                               description=f'{user.display_name} baniu {member.mention} do servidor!\n'
                               f'Razão: {reason}')

            em.set_thumbnail(
                url='https://cdn.discordapp.com/emojis/716678272338886716.webp')
            em.set_footer(
                text=f'Registrado em {guild}', icon_url=f'{guild.icon}')
            em.timestamp = datetime.datetime.now(tz=config.tz_brazil)

            await interaction.response.send_message(embed=em)

    @commands.hybrid_command(name='wikia', with_app_command=True)
    async def wikia(self, ctx):

        ''' Envia uma imagem aleatoria relacionada a wiki'''

        if ctx.message.reference:
            msg = ctx.channel.get_partial_message(
                ctx.message.reference.message_id)
            await msg.reply(file=discord.File(arquivoWiki()))
            return

        await ctx.send(file=discord.File(arquivoWiki()))

    @commands.hybrid_command(name='wiki', with_app_command=True)
    @app_commands.describe(pesquisa='O que deseja pesquisar?')
    async def wiki(self, ctx: Context, *, pesquisa: str = None):

        '''   Pesquisa algo em warframe.fandom.com    '''

        guild = ctx.guild

        if pesquisa == None:
            await ctx.reply('Informe o que devo pesquisar')
            return

        if ctx.message.reference:
            msg = ctx.channel.get_partial_message(ctx.message.reference.message_id)
            msg1 = await msg.reply('me dá um segundinho...')
            msg = ctx.channel.get_partial_message(msg1.id)
        else:
            msg = await ctx.send('me dá um segundinho...')

        em = discord.Embed(title=f'{pesquisa}', 
                           color=config.roxo,
                           description='',
                           timestamp=datetime.datetime.now(tz=config.tz_brazil))
        em.set_footer(text=guild.name, icon_url=guild.icon)

        pesquisa.replace(' ', '+')

        res = requests.get(f'https://warframe.fandom.com/wiki/Special:Search?query={pesquisa}&scope=internal&navigationSearch=true')
        soup = BeautifulSoup(res.text, 'html.parser')

        search = soup.select('.unified-search__result__title')

        search_index = 0 
        for search_index in range(5):
            if search_index == len(search): 
                break

            title = search[search_index].get('data-title')
            link = search[search_index].get('href')
            em.description += f'[{title}]({link})\n'
            search_index += 1

        try:
            photo_res = requests.get(search[0].get('href'))
            photo_soup = BeautifulSoup(photo_res.text, 'html.parser')
            a = photo_soup.find('a', class_='image image-thumbnail', href=True)
            em.set_thumbnail(url=str(a['href']))

        except:
            pass

        await msg.edit(content='', embed=em)
        return


    @app_commands.command(name='ola')
    async def ola(self, interaction: discord.Interaction):

        '''     Olá!     '''

        biell = await self.bot.fetch_user(420634633793699851)
        entidade = await self.bot.fetch_user(1002306871132168192)

        await interaction.response.send_message(f'Olá {interaction.user.display_name}!'
                                                f'\nFui criado com o objetivo de auxiliar a **{interaction.guild.name}** enquanto restauramos a {entidade.mention}'
                                                f'\n\nDesenvolvido por {biell.mention}, qualquer problema ou duvida quem me envolva pergunte a ele.', ephemeral=True)
        return


async def setup(bot):
    await bot.add_cog(openCommands(bot))
