import discord
import random
import pytz
import re
import config

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Optional


tz_brazil = pytz.timezone('America/Sao_Paulo')


@app_commands.guild_only()
class rpgCommands(commands.GroupCog, name='rpg'):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='dado', with_app_command=True)
    @app_commands.describe(dados='Informe quantos dados e quantos lados. ex.: 4d6')
    async def dado(self, ctx: Context, dados: str):

        '''Tente a sorte nos dados'''

        guild = ctx.guild
        dados = dados.lower()

        if ctx.channel.id != config.comandos:
            comandos = guild.get_channel(config.comandos)
            await ctx.reply(f'Apenas em {comandos.mention}', ephemeral=True)
            return

        em = discord.Embed(title='Dados', color=config.roxo, description=dados)

        msg = await ctx.reply(embed=em)

        if ('d' not in dados) or (len(dados) < 3):
            em.color = config.vermelho
            em.description = f'Error:\nEsperado: ex.: 4d6\nRecebido: {dados}'
            await msg.edit(embed=em)
            return

        x = re.split(r'[d|+|*|/|-]', dados)

        q_dados = int(x[0])
        q_lados = int(x[1])

        em.title = f'Dados - {dados}'

        if 0 < q_dados > 20:
            em.color = config.vermelho
            em.description = 'Error:\nLimite  de dados: 1 ~ 20'
            await msg.edit(embed=em)
            return

        if 2 < q_lados > 100:
            em.color = config.vermelho
            em.description = 'Error:\nLimite  de lados: 2 ~ 100'
            await msg.edit(embed=em)
            return

        if q_lados > 2:
            soma = soma_dados(q_dados, q_lados)

            em.color = config.roxo
            em.description = f'{q_dados} {"dado" if q_dados == 1 else "dados"} de {q_lados} lados:\n{soma[0]}'

            if '+' in dados:
                fim = int(soma[1]) + int(x[2])
                em.description += f'= {soma[1]} + {x[2]} = {fim}'

            elif '-' in dados:
                fim = int(soma[1]) - int(x[2])
                em.description += f'= {soma[1]} - {x[2]} = {fim}'

            elif '*' in dados:
                fim = int(soma[1]) * int(x[2])
                em.description += f'= {soma[1]} * {x[2]} = {fim}'

            elif '/' in dados:
                fim = int(soma[1]) / int(x[2])
                em.description += f'= {soma[1]} / {x[2]} = {fim}'

            else:
                em.description += f'= {soma[1]}'

            await msg.edit(embed=em)

    @dado.error
    async def dado_error(self, ctx: Context, err):
        if isinstance (err, commands.errors.MissingRequiredArgument):
            em = discord.Embed(
                title='Dados',
                color=config.vermelho,
                description=f'Error:\nEsperado: ex.: p!dado 4d6\nRecebido: p!dado')
            await ctx.reply(embed=em)
            return


def soma_dados(dados, lados):
    soma = 0
    texto = ''
    lista = []

    for y in range(dados):
        dado = random.randint(1, lados)
        texto += f'{dado} + '
        soma += dado
        lista.append(dado)
    end_text = f'{texto[:-2]}'

    return end_text, soma, lista


async def setup(bot):
    await bot.add_cog(rpgCommands(bot))
