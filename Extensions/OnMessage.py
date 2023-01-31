import random
import discord
import discord.utils
import os
import pytz
import config

from datetime import datetime
from discord.ext import commands


cd_mapping = commands.CooldownMapping.from_cooldown(
    1, 150, commands.BucketType.channel)

images = os.path.join(os.getcwd(), "./imagens/nada")


def arquivoNada():
    return os.path.join(images, random.choice(os.listdir(images)))


tz_brazil = pytz.timezone('America/Sao_Paulo')

nico = ['nix', 'nico', 'nicolas', 'nero', 'nicolau']
pia = ['pia', 'piá']
apolo = ['apolo', 'xapolo', 'apolo10', 'xapolo10']

roxo = 0x690FC3


class onMessage(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        msg0 = message.content.lower()
        msg = msg0.split()

        guild = message.guild

        if message.author.bot:
            return

        if msg:

            for apolo10 in apolo:
                if apolo10 in msg:
                    await message.add_reaction("<:DeletSteve:756658553804161075>")

            if '<@296031411532726274>' in msg:
                await message.add_reaction("<:DeletSteve:756658553804161075>")

            #####################

            if 'frost' in msg:
                await message.add_reaction("<:frost:842098733726040155>")

            if '<@272111002110263308>' in msg:
                await message.add_reaction("<:frost:842098733726040155>")

            #####################

            if "teixera" in msg:
                await message.add_reaction("<:Teixeira:759925616887463976>")

            if '<@467662803394887680>' in msg:
                await message.add_reaction("<:Teixeira:759925616887463976>")

            ####################

            if "entidade" in msg:
                await message.add_reaction("<:EntidadeBan:716678272338886716>")

            if '<@1002306871132168192>' in msg:
                await message.add_reaction("<:EntidadeBan:716678272338886716>")

            ####################
            for lider in pia:
                if lider in msg:
                    await message.add_reaction("<:Suspeito:657016538653655071>")

            if '<@711004246535045161>' in msg:
                await message.add_reaction("<:Suspeito:657016538653655071>")

            ####################

            if "heid" in msg:
                await message.add_reaction("<:AnnoyedPigeon:756658547374424164>")

            if '<@902647469840687184>' in msg:
                await message.add_reaction("<:AnnoyedPigeon:756658547374424164>")

            ####################

            for nix in nico:
                if nix in msg:
                    await message.add_reaction("<:ehe:724081286993543228>")

            if "<@794578925807992832>" in msg:
                await message.add_reaction("<:ehe:724081286993543228>")

        if message.channel.id == config.warframe_chat or message.channel.id == config.teste_dev:

            nada = ['nada para fazer', 'nada pa fazer', 'nada pra fazer', 'nd pra fazer', 'nada no jogo para fazer', 'nd p fz', 'nd p fzr', 'conteudo do warframe',
                    'conteudo no warframe', 'no content']

            for nadareply in nada:
                if nadareply in message.content.lower():

                    bucket = cd_mapping.get_bucket(message)
                    retry_after = bucket.update_rate_limit()

                    if retry_after:
                        await message.reply(f'calma, sem pressa que ainda falta ``{round(retry_after)}s``')
                        break

                    else:
                        await message.reply(file=discord.File(arquivoNada()))
                        break
            return

        if message.channel.id == config.sugest:
            sugest = guild.get_channel(config.sugest)
            em = discord.Embed(title="Sugestão",
                               color=roxo,
                               description=f"Sugestão de {message.author.mention}:\n"
                                           f"||autor: {message.author} - {message.author.id}||\n\n"
                                           f"{message.content}",
                                           timestamp=datetime.now(tz=tz_brazil))
            em.set_footer(text="Reaja com base na sua decisão", icon_url=guild.icon)
            msg_1 = await sugest.send(embed=em)
            await msg_1.add_reaction("👍")
            await msg_1.add_reaction("👎")
            await message.delete()
            return

        if message.channel.id == config.sugest_nomes:
            sugest = guild.get_channel(config.sugest_nomes)
            em = discord.Embed(title="Sugestão para nomeação da aliança e clãs",
                               color=roxo,
                               description=f"Sugestão de {message.author.mention}:\n"
                                           f"||autor: {message.author} - {message.author.id}||\n\n"
                                           f"{message.content}",
                                           timestamp=datetime.now(tz=tz_brazil))
            em.set_footer(text="Reaja com base na sua decisão",
                          icon_url=guild.icon)
            msg_1 = await sugest.send(embed=em)
            await msg_1.add_reaction("👍")
            await msg_1.add_reaction("👎")
            await message.delete()
            return


async def setup(bot):
    await bot.add_cog(onMessage(bot))
