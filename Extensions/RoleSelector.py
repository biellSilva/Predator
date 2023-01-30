import discord
import asyncio
import config

from datetime import datetime
from discord.ext import commands


class AlertaView(discord.ui.View):
    @discord.ui.select(
        custom_id='Alertas_selector',
        min_values=0,
        max_values=12,
        placeholder='Selecione cargos que devem ser alterados',
        options=[
            discord.SelectOption(
                label='Ajudante',
                value='ajudante',
                emoji='🆘',
                description='Será pingado ao precisarem de Ajudantes'),
            
            discord.SelectOption(
                label='Reator',
                value='reator',
                emoji=':reator:844951875791093760',
                description='Será pingado em alertas com Reatores'),

            discord.SelectOption(
                label='Catalisador',
                value='catalisador',
                emoji=':catalisador:844951875371401247',
                description='Será pingado em alertas com Catalisadores'),

            discord.SelectOption(
                label='Baro Ki\'Teer',
                value='baro',
                emoji=':BaroBitchPlease:716035316464615455',
                description='Será pingado com a chegada do Baro Ki\'Teer'),

            discord.SelectOption(
                label='Forma',
                value='forma',
                emoji=':Forma:821407092698906656',
                description='Será pingado em alertas com Formas'),

            discord.SelectOption(
                label='Forma Umbra',
                value='umbra',
                emoji=':FormaUmbraiss:679970463153258512',
                description='Será pingado em alertas com Formas Umbra'),

            discord.SelectOption(
                label='Lotus Cósmica',
                value='lotus',
                emoji=':LotusCosmica:835281000694284349',
                description='Será pingado na Lotus Cósmica'),

            discord.SelectOption(
                label='Grão Mestre Ping',
                value='mestre',
                description='Pingado quando um Grão Mestre for usar sua benção'),

            discord.SelectOption(
                label='Sorteios',
                value='sorteio',
                emoji='🎉',
                description='Será pingado quando houver Sorteios'),

            discord.SelectOption(
                label='Eventos Externos',
                value='evento',
                emoji='🎊',
                description='Será pingado quando houver Eventos Externos'),
            
            discord.SelectOption(
                label='Drops Externos',
                value='drops',
                emoji='🎁',
                description='Será pingado quando houver Drops Externos'),

            discord.SelectOption(
                label='Atualizações',
                value='update',
                emoji='🔔',
                description='Será pingado quando houver Atualizações do Warframe')
        ])

    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild = interaction.guild
        user = interaction.user

        await interaction.response.defer(ephemeral=True, thinking=True)

        ajudante = guild.get_role(config.ajudante)
        reator = guild.get_role(config.reator)
        catalisador = guild.get_role(config.catalisador)
        baro = guild.get_role(config.baro)
        forma = guild.get_role(config.forma)
        forma_umbra = guild.get_role(config.forma_umbra)
        lotus = guild.get_role(config.lotus)
        mestre = guild.get_role(config.mestre)
        sorteio = guild.get_role(config.sorteio)
        evento = guild.get_role(config.eventoExt)
        drop = guild.get_role(config.dropExt)
        update = guild.get_role(config.update)

        roles_list = [ajudante, reator, catalisador, baro, forma, forma_umbra, lotus, mestre, sorteio, evento, drop, update]
        values_list = ['ajudante', 'reator', 'catalisador', 'baro', 'forma', 'umbra', 'lotus', 'mestre', 'sorteio', 'evento', 'drops', 'update']
        index_value = 0

        add = '**Adicionado:**'
        mantem = '**Mantido:**'
        removido = '**Removido:**'

        for role in roles_list:
            while index_value < len(roles_list)+1:
                if values_list[index_value] in select.values:
                    if roles_list[index_value] not in user.roles:
                        await user.add_roles(roles_list[index_value])
                        add += f'\n*+ {roles_list[index_value].mention}*'
                    else:
                        await user.remove_roles(roles_list[index_value])
                        removido += f'\n*- {roles_list[index_value].mention}*'
                else:
                    if roles_list[index_value] in user.roles:
                        mantem += f'\n*~ {roles_list[index_value].mention}*'
                index_value += 1
                break

        await interaction.edit_original_response(content=f'{"**Nenhum cargo adicionado**" if len(add)<17 else add}'
                                                         f'\n\n{"**Nenhum cargo removido**" if len(removido)<17 else removido}'
                                                         f'\n\n{"**Nenhum cargo mantido**" if len(mantem)<14 else mantem}')


class SquadView(discord.ui.View):
    @discord.ui.select(
        custom_id='Squad_selector',
        min_values=0,
        max_values=18,
        placeholder='Selecione cargos que devem ser alterados',
        options=[
            discord.SelectOption(
                label='Eidolon',
                value='eidolon',
                emoji=':ostron:664486884868882487',
                description='Ping para caçar Eidolon'),

            discord.SelectOption(
                label='Beneficiária',
                value='profit',
                description='Ping para caçar a Beneficiária'),

            discord.SelectOption(
                label='Deriva de Cambion',
                value='deimos',
                description='Ping para a Deriva de Cambion'),

            discord.SelectOption(
                label='Zariman',
                value='anjos',
                description='Ping para farm na Zariman'),

            discord.SelectOption(
                label='Relíquias ',
                value='relic',
                emoji=':reliquia:664486282046472202',
                description='Ping para as Relíquias '),

            discord.SelectOption(
                label='Caminho do Aço',
                value='steel',
                description='Ping para o Caminho do Aço'),

            discord.SelectOption(
                label='Index',
                value='index',
                emoji=':Creditos:596817907984498718',
                description='Ping para farm de Créditos'),

            discord.SelectOption(
                label='Recursos',
                value='recurso',
                emoji=':recurso:664484737951334401',
                description='Ping para farm de Recursos'),
            
            discord.SelectOption(
                label='Arbitragem',
                value='arbitros',
                emoji=':arbiters:664487282635571213',
                description='Ping para a Arbitragem'),

            discord.SelectOption(
                label='Experiencia',
                value='xp',
                emoji=':afinidade:664488114437357574',
                description='Ping para farm de Xp'),

            discord.SelectOption(
                label='Railjack',
                value='railjack',
                emoji=':CephalonCy:664487929724272660',
                description='Ping para a Railjack'),

            discord.SelectOption(
                label='Massacre do Santuário',
                value='santuario',
                description='Ping para o Massacre do Santuário'),

            discord.SelectOption(
                label='Kuva Liches',
                value='lich',
                emoji=':ReliquiaRequiem:687005668325982238',
                description='Ping para caçar Kuva Lich'),
            
            discord.SelectOption(
                label='Irmãs de Parvos',
                value='sisters',
                description='Ping para caçar Corpus Lich'),

            discord.SelectOption(
                label='Kuva',
                value='kuva',
                emoji=':Kuva:689906601619882020',
                description='Ping para farm de Kuva'),

            discord.SelectOption(
                label='Praga Estelar',
                value='praga',
                emoji=':Forma:821407092698906656',
                description='Ping para a Praga Estelar'),

            discord.SelectOption(
                label='Novato',
                value='novato',
                description='Pingado quando querem ajudar novatos'),

            discord.SelectOption(
                label='Caçada de Arconte',
                value='archon',
                emoji='🐍',
                description='Ping para a Caçada de Arconte')])
                
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        user = interaction.user
        guild = interaction.guild

        await interaction.response.defer(ephemeral=True, thinking=True)

        eidolon = guild.get_role(config.eidolon)
        profit = guild.get_role(config.profit)
        relic = guild.get_role(config.relic)
        steel = guild.get_role(config.steel)
        index = guild.get_role(config.index)
        recurso = guild.get_role(config.recurso)
        arbitros = guild.get_role(config.arbitros)
        xp = guild.get_role(config.xp)
        railjack = guild.get_role(config.railjack)
        deimos = guild.get_role(config.deimos)
        santuario = guild.get_role(config.santuario)
        lich = guild.get_role(config.kuvalich)
        sisters = guild.get_role(config.corpuslich)
        kuva = guild.get_role(config.kuva)
        anjos = guild.get_role(config.anjos)
        praga = guild.get_role(config.praga)
        novato = guild.get_role(config.novato)
        archon = guild.get_role(config.archon)

        roles_list = [eidolon, profit, relic, steel, index, recurso, arbitros, xp, railjack, deimos, santuario, lich, sisters, kuva, anjos, praga, novato, archon]
        values_list = ['eidolon', 'profit', 'relic', 'steel', 'index', 'recurso', 'arbitros', 'xp', 'railjack', 'deimos', 'santuario', 'lich', 'sisters', 'kuva', 'anjos', 'praga', 'novato', 'archon']
        index_value = 0

        add = '**Adicionado:**'
        mantem = '**Mantido:**'
        removido = '**Removido:**'

        for role in roles_list:
            while index_value < len(roles_list)+1:
                if values_list[index_value] in select.values:
                    if roles_list[index_value] not in user.roles:
                        await user.add_roles(roles_list[index_value])
                        add += f'\n*+ {roles_list[index_value].mention}*'
                    else:
                        await user.remove_roles(roles_list[index_value])
                        removido += f'\n*- {roles_list[index_value].mention}*'
                else:
                    if roles_list[index_value] in user.roles:
                        mantem += f'\n*~ {roles_list[index_value].mention}*'
                index_value += 1
                break

        await interaction.edit_original_response(content=f'{"**Nenhum cargo adicionado**" if len(add)<17 else add}'
                                                 f'\n\n{"**Nenhum cargo removido**" if len(removido)<17 else removido}'
                                                 f'\n\n{"**Nenhum cargo mantido**" if len(mantem)<14 else mantem}')


class DiarioView(discord.ui.View):
    @discord.ui.select(
        custom_id='diario_selector',
        min_values=0,
        max_values=6,
        placeholder='Selecione cargos que devem ser alterados',
        options=[
            discord.SelectOption(
                label='Cetus Dia',
                value='dia',
                emoji='☀️',
                description='Ping quando amanhecer em Cetus'),

            discord.SelectOption(
                label='Cetus Noite',
                value='noite',
                emoji='🌑',
                description='Ping quando anoitecer em Cetus'),

            discord.SelectOption(
                label='Deimos Vome',
                value='vome',
                emoji='🔵',
                description='Ping quando Vome reina no Necralisk'),

            discord.SelectOption(
                label='Deimos Fass',
                value='fass',
                emoji='🔴',
                description='Ping quando Fass reina no Necralisk'),

            discord.SelectOption(
                label='Fortuna Frio',
                value='frio',
                emoji='❄️',
                description='Ping quando Fortuna se torna Fria'),

            discord.SelectOption(
                label='Fortuna Morno',
                value='morno',
                emoji='🔥',
                description='Ping quando Fortuna se torna Morna'),
        ])
    
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        user = interaction.user
        guild = interaction.guild

        await interaction.response.defer(ephemeral=True, thinking=True)
        
        dia = guild.get_role(config.dia)
        noite = guild.get_role(config.noite)
        vome = guild.get_role(config.vome)
        fass = guild.get_role(config.fass)
        frio = guild.get_role(config.frio)
        morno = guild.get_role(config.morno)

        roles_list = [dia, noite, vome, fass, frio, morno]
        values_list = ['dia', 'noite', 'vome', 'fass', 'frio', 'morno']
        index_value = 0

        add = '**Adicionado:**'
        mantem = '**Mantido:**'
        removido = '**Removido:**'

        for role in roles_list:
            while index_value < len(roles_list)+1:
                if values_list[index_value] in select.values:
                    if roles_list[index_value] not in user.roles:
                        await user.add_roles(roles_list[index_value])
                        add += f'\n*+ {roles_list[index_value].mention}*'
                    else:
                        await user.remove_roles(roles_list[index_value])
                        removido += f'\n*- {roles_list[index_value].mention}*'
                else:
                    if roles_list[index_value] in user.roles:
                        mantem += f'\n*~ {roles_list[index_value].mention}*'
                index_value += 1
                break

        await interaction.edit_original_response(content=f'{"**Nenhum cargo adicionado**" if len(add)<17 else add}'
                                                 f'\n\n{"**Nenhum cargo removido**" if len(removido)<17 else removido}'
                                                 f'\n\n{"**Nenhum cargo mantido**" if len(mantem)<14 else mantem}')


class PlataformaView(discord.ui.View):
    @discord.ui.select(
        custom_id='plataforma_selector',
        min_values=0,
        max_values=3,
        placeholder='Selecione cargos que devem ser alterados',
        options=[
            discord.SelectOption(
                label='Pc',
                value='pc',
                emoji='💻',
                description='Joga pelo Pc/Notebook'),

            discord.SelectOption(
                label='Console',
                value='console',
                emoji='🎮',
                description='Joga pelo Console'),

            discord.SelectOption(
                label='Mobile',
                value='mobile',
                emoji='📱',
                description='Joga pelo Mobile')])

    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild = interaction.guild
        user = interaction.user

        await interaction.response.defer(ephemeral=True, thinking=True)

        pc = guild.get_role(config.pc)
        console = guild.get_role(config.console)
        mobile = guild.get_role(config.mobile)

        roles_list = [pc, console, mobile]
        values_list = ['pc', 'console', 'mobile']
        index_value = 0

        add = '**Adicionado:**'
        mantem = '**Mantido:**'
        removido = '**Removido:**'

        for role in roles_list:
            while index_value < len(roles_list)+1:
                if values_list[index_value] in select.values:
                    if roles_list[index_value] not in user.roles:
                        await user.add_roles(roles_list[index_value])
                        add += f'\n*+ {roles_list[index_value].mention}*'
                    else:
                        await user.remove_roles(roles_list[index_value])
                        removido += f'\n*- {roles_list[index_value].mention}*'
                else:
                    if roles_list[index_value] in user.roles:
                        mantem += f'\n*~ {roles_list[index_value].mention}*'
                index_value += 1
                break

        await interaction.edit_original_response(content=f'{"**Nenhum cargo adicionado**" if len(add)<17 else add}'
                                                 f'\n\n{"**Nenhum cargo removido**" if len(removido)<17 else removido}'
                                                 f'\n\n{"**Nenhum cargo mantido**" if len(mantem)<14 else mantem}')


class MemberView(discord.ui.View):
    @discord.ui.select(
        custom_id='member_selector',
        max_values=1,
        placeholder='Selecione seu cargo',
        options=[
            discord.SelectOption(
                label='Os Tenno de Andromeda',
                value='tan',
                emoji=':Andromeda:615250826474291211',
                description='Membro do Andromeda'),

            discord.SelectOption(
                label='Os Tenno de Aquila',
                value='ta',
                emoji=':Aquila:615250826289741834',
                description='Membro do Aquila'),
            
            discord.SelectOption(
                label='Os Tenno de Lyra',
                value='tl',
                emoji=':Lyra:615250826260381735',
                description='Membro do Lyra'),

            discord.SelectOption(
                label='Os Tenno de Orion',
                value='to',
                emoji=':Orion:615250826872619196',
                description='Membro do Orion'),
            
            discord.SelectOption(
                label='Visitante',
                value='visit',
                emoji='👥',
                description='Visitando a Aliança'),

            discord.SelectOption(
                label='Quero Participar',
                value='parti',
                emoji='🤝',
                description='Deseja participar da Aliança')])

    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild = interaction.guild
        member = interaction.user

        await interaction.response.defer(ephemeral=True, thinking=True)

        tan = guild.get_role(config.andromeda)
        ta = guild.get_role(config.aquila)
        tl = guild.get_role(config.lyra)
        to = guild.get_role(config.orion)

        visitante = guild.get_role(config.visitante)
        participar = guild.get_role(config.participar)
        membro = guild.get_role(config.membro)

        recrutador = guild.get_role(config.Recrutador)

        channelRec = guild.get_channel(config.recrutamento)

        add = '\n**Adicionado:**'
        removido = '\n**Removido:**'
        mantem = '\n**Mantido:**'

        if "tan" in select.values:
            if tan not in member.roles:
                await member.add_roles(tan)
                await member.add_roles(membro)
                add += f'\n*+ {tan.mention}*'
        else:
            if tan in member.roles:
                await member.remove_roles(tan)
                removido += f'\n*- {tan.mention}*'

        if "ta" in select.values:
            if ta not in member.roles:
                await member.add_roles(ta)
                add += f'\n*+ {ta.mention}*'
        else:
            if ta in member.roles:
                await member.remove_roles(ta)
                removido += f'\n*- {ta.mention}*'

        if "tl" in select.values:
            if tl not in member.roles:
                await member.add_roles(tl)
                await member.add_roles(membro)
                add += f'\n*+ {tl.mention}*'
        else:
            if tl in member.roles:
                await member.remove_roles(tl)
                removido += f'\n*- {tl.mention}*'

        if "to" in select.values:
            if to not in member.roles:
                await member.add_roles(to)
                await member.add_roles(membro)
                add += f'\n*+ {to.mention}*'
        else:
            if to in member.roles:
                await member.remove_roles(to)
                removido += f'\n*- {to.mention}*'

        if "visit" in select.values:
            if visitante not in member.roles:
                await member.add_roles(visitante)
                await member.remove_roles(membro)
                add += f'\n*+ {visitante.mention}*'
        else:
            if visitante in member.roles:
                await member.remove_roles(visitante)
                removido += f'\n*- {visitante.mention}*'

        if "parti" in select.values:
            if participar not in member.roles:
                await member.add_roles(participar)
                await member.remove_roles(membro)
                add += f'\n*+ {participar.mention}*'

                embedRec = discord.Embed(title="Recrutamento",
                                         color=config.roxo,
                                         description=f"Olá {member.mention}, para um atendimento rapido informe seu nick no Warframe e um dos clãs abaixo para notificarmos um recrutador\n\n"
                                         f"<:Andromeda:615250826474291211> - {tan.mention}\n"
                                         f"<:Aquila:615250826289741834> - {ta.mention}\n"
                                         f"<:Lyra:615250826260381735> - {tl.mention}\n"
                                         f"<:Orion:615250826872619196> - {to.mention}\n\n"
                                         f"||{member} - {member.id}||")
                embedRec.timestamp = datetime.now(tz=config.tz_brazil)
                embedRec.set_footer(text=f"Bem vindo a {guild}", icon_url=guild.icon.url)
                embedRec.set_thumbnail(url=member.display_avatar.url)

                await asyncio.sleep(1)
                await channelRec.send(f"{member.mention} {recrutador.mention}")
                await channelRec.send(embed=embedRec)

        else:
            if participar in member.roles:
                await member.remove_roles(participar)
                removido += f'\n*- {participar.mention}*'

        await interaction.edit_original_response(content=f'{"**Nenhum cargo adicionado**" if len(add)<17 else add}\n{"**Nenhum cargo removido**" if len(removido)<17 else removido}')


class CargosSelector(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.member_view = MemberView(timeout=None)
        self.plataforma_view = PlataformaView(timeout=None)
        self.diario_view = DiarioView(timeout=None)
        self.squad_view = SquadView(timeout=None)
        self.alerta_view = AlertaView(timeout=None)

    async def cog_load(self):
        self.bot.add_view(self.member_view)
        self.bot.add_view(self.plataforma_view)
        self.bot.add_view(self.diario_view)
        self.bot.add_view(self.squad_view)
        self.bot.add_view(self.alerta_view)

    @commands.command(name='viewT')
    @commands.is_owner()
    async def membros_view(self, ctx: commands.Context):
        ''' Inicia os seletores de cargos '''

        bem_vindo_canal = ctx.guild.get_channel(config.bem_vindo)

        warframe_chat = ctx.guild.get_channel(config.warframe_chat)
        off_topic = ctx.guild.get_channel(config.off_topic)
        cargo_reaçao = ctx.guild.get_channel(config.cargo_reacao)
        cargo_conquista = ctx.guild.get_channel(config.cargo_conquista)

        bem_vindo = discord.Embed(color=config.roxo,
                                  title=f'Bem vindo a {ctx.guild.name}',
                                  description='''
                                  Temos como objetivo reunir jogadores em uma comunidade forte e ativa no Universo Warframe. 
                                  Fique à vontade para navegar pelos canais de voz e texto. 
                                  Abaixo, você encontrará as informações necessárias para usar o Discord. 
                                  ''')
        bem_vindo.set_thumbnail(url=ctx.guild.icon.url)
        
        memberEmbed = discord.Embed(color=config.roxo,
                                    description='''
                                        Você está em um dos quatro Clãs da União, quer participar ou só veio visitar?
                                        Para saber em qual clã está basta conferir seu perfil no jogo
                                        <:Andromeda:615250826474291211> <:Aquila:615250826289741834> <:Lyra:615250826260381735> <:Orion:615250826872619196> 👥 🤝''')

        plataformaEmbed = discord.Embed(color=config.roxo,
                                        description='Utiliza qual plataforma para jogar? 💻 🎮 📱')
        
        mais_texto = discord.Embed(color=config.roxo,
                                  description=f'''
                                    Você pode usar o canal {warframe_chat.mention} para conversar sobre os mais diversos assuntos relacionados ao Warframe. 
                                    Caso tenha algum assunto que não seja relacionado ao Warframe, publique-o no canal {off_topic.mention}
                                    Dica: Facilita a comunicação se seu nome aqui no Discord for igual ao seu nome no Jogo. 

                                    Você pode receber alertas sobre as atividades do jogo indo ao canal {cargo_reaçao.mention}.
                                    Também, buscar conquistas exclusivas de nosso servidor, os requisitos estão no canal {cargo_conquista.mention}. 
                                    ''')
        
        await bem_vindo_canal.send(embed=bem_vindo)
        await bem_vindo_canal.send(embed=memberEmbed, view=MemberView())
        await bem_vindo_canal.send(embed=plataformaEmbed, view=PlataformaView())
        await bem_vindo_canal.send(embed=mais_texto)


        diarioEmbed = discord.Embed(color=config.roxo,
                                    description='Selecione os ping de horarios que deseja: ☀️ 🌑 ❄️ 🔥')

        squadEmbed = discord.Embed(color=config.roxo,
                                   description='Selecione os ping de esquadrões que deseja: <:reliquia:664486282046472202> <:Creditos:596817907984498718> <:recurso:664484737951334401> <:Forma:821407092698906656>')

        alertaEmbed = discord.Embed(color=config.roxo,
                                   description='Selecione os ping de alertas que deseja: <:reator:844951875791093760> <:catalisador:844951875371401247> <:BaroBitchPlease:716035316464615455> <:FormaUmbraiss:679970463153258512>')

        await cargo_reaçao.send(embed=diarioEmbed, view=DiarioView())
        await cargo_reaçao.send(embed=squadEmbed, view=SquadView())
        await cargo_reaçao.send(embed=alertaEmbed, view=AlertaView())
        
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(CargosSelector(bot))