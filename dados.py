"""Dados compilados manualmente para o Guia do Imigrante.

Salário mínimo, IDH, índices de custo de vida/segurança/qualidade de vida e
rotas de visto não existem em nenhuma API pública gratuita, por isso ficam aqui.
Todo o resto (indicadores do Banco Mundial, câmbio, clima, resumo do país)
é buscado nas APIs pelo módulo apis.py.

Fontes:
- Salário mínimo: legislação de cada país (ano de referência em "ano_ref").
- IDH: Relatório de Desenvolvimento Humano do PNUD (HDR 2025, dados de 2023).
- Custo de vida, segurança e qualidade de vida: índices aproximados do Numbeo
  (2025). No custo de vida, Nova York = 100.
"""

# Horas trabalhadas por mês, para converter salário por hora em salário mensal
# (40 horas por semana x 52 semanas / 12 meses).
HORAS_POR_MES = 40 * 52 / 12

# O Brasil serve de referência nas comparações.
BRASIL = {
    "iso3": "BRA", "iso2": "br", "nome": "Brasil", "capital": "Brasília",
    "continente": "América do Sul", "idiomas": ["Português"],
    "moeda": {"codigo": "BRL", "nome": "Real brasileiro"},
    "salario_minimo": {"valor": 1621, "periodo": "mes", "ano_ref": 2026},
    "idh": 0.786, "custo_vida": 28, "seguranca": 32, "qualidade_vida": 105,
}

PAISES = [
    {
        "iso3": "PRT", "iso2": "pt", "nome": "Portugal", "continente": "Europa",
        "capital": "Lisboa", "coords": (38.7223, -9.1393), "wiki": "Portugal",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Português"],
        "salario_minimo": {"valor": 920, "periodo": "mes", "ano_ref": 2026,
                           "obs": "Pago em 14 parcelas por ano (inclui 13º e subsídio de férias)."},
        "idh": 0.890, "custo_vida": 44, "seguranca": 70, "qualidade_vida": 165,
        "vistos": ["Visto D7 (renda passiva)", "Visto D8 (nômade digital)",
                   "Visto para procura de trabalho", "Acordo de mobilidade CPLP"],
        "resumo": "Mesmo idioma, clima ameno e grande comunidade brasileira.",
    },
    {
        "iso3": "ESP", "iso2": "es", "nome": "Espanha", "continente": "Europa",
        "capital": "Madri", "coords": (40.4168, -3.7038), "wiki": "Espanha",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Espanhol", "Catalão", "Galego", "Basco"],
        "salario_minimo": {"valor": 1184, "periodo": "mes", "ano_ref": 2025,
                           "obs": "Pago em 14 parcelas por ano."},
        "idh": 0.918, "custo_vida": 48, "seguranca": 64, "qualidade_vida": 170,
        "vistos": ["Visto de nômade digital", "Arraigo (regularização por residência)",
                   "Visto de estudante", "Nacionalidade pela Lei da Memória Democrática"],
        "resumo": "Qualidade de vida alta, idioma próximo e custo moderado.",
    },
    {
        "iso3": "IRL", "iso2": "ie", "nome": "Irlanda", "continente": "Europa",
        "capital": "Dublin", "coords": (53.3498, -6.2603), "wiki": "Irlanda",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Inglês", "Irlandês"],
        "salario_minimo": {"valor": 14.15, "periodo": "hora", "ano_ref": 2026},
        "idh": 0.949, "custo_vida": 70, "seguranca": 56, "qualidade_vida": 160,
        "vistos": ["Critical Skills Employment Permit", "General Employment Permit",
                   "Stamp 2 (estudante, pode trabalhar 20 h por semana)"],
        "resumo": "Polo de tecnologia na Europa; o intercâmbio de inglês costuma ser a porta de entrada.",
    },
    {
        "iso3": "DEU", "iso2": "de", "nome": "Alemanha", "continente": "Europa",
        "capital": "Berlim", "coords": (52.52, 13.405), "wiki": "Alemanha",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Alemão"],
        "salario_minimo": {"valor": 13.90, "periodo": "hora", "ano_ref": 2026},
        "idh": 0.959, "custo_vida": 63, "seguranca": 61, "qualidade_vida": 185,
        "vistos": ["Blue Card UE", "Chancenkarte (Cartão de Oportunidade)",
                   "Visto para formação profissional (Ausbildung)"],
        "resumo": "Maior economia da Europa, com falta de mão de obra qualificada.",
    },
    {
        "iso3": "NLD", "iso2": "nl", "nome": "Países Baixos", "continente": "Europa",
        "capital": "Amsterdã", "coords": (52.3676, 4.9041), "wiki": "Países_Baixos",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Neerlandês"],
        "salario_minimo": {"valor": 14.06, "periodo": "hora", "ano_ref": 2025},
        "idh": 0.955, "custo_vida": 66, "seguranca": 71, "qualidade_vida": 200,
        "vistos": ["Highly Skilled Migrant", "Orientation Year (recém-formados)", "Blue Card UE"],
        "resumo": "Inglês muito difundido e uma das melhores qualidades de vida do mundo.",
    },
    {
        "iso3": "GBR", "iso2": "gb", "nome": "Reino Unido", "continente": "Europa",
        "capital": "Londres", "coords": (51.5074, -0.1278), "wiki": "Reino_Unido",
        "moeda": {"codigo": "GBP", "nome": "Libra esterlina"},
        "idiomas": ["Inglês"],
        "salario_minimo": {"valor": 12.71, "periodo": "hora", "ano_ref": 2026,
                           "obs": "National Living Wage (21 anos ou mais)."},
        "idh": 0.946, "custo_vida": 64, "seguranca": 52, "qualidade_vida": 168,
        "vistos": ["Skilled Worker visa", "Global Talent visa", "Graduate visa"],
        "resumo": "Mercado financeiro e acadêmico forte; quase sempre exige patrocínio do empregador.",
    },
    {
        "iso3": "ITA", "iso2": "it", "nome": "Itália", "continente": "Europa",
        "capital": "Roma", "coords": (41.9028, 12.4964), "wiki": "Itália",
        "moeda": {"codigo": "EUR", "nome": "Euro"},
        "idiomas": ["Italiano"],
        "salario_minimo": {"valor": 1300, "periodo": "mes", "ano_ref": 2025, "referencia": True,
                           "obs": "Não há salário mínimo nacional. Valor aproximado dos pisos das convenções coletivas (comércio e serviços)."},
        "idh": 0.915, "custo_vida": 55, "seguranca": 55, "qualidade_vida": 150,
        "vistos": ["Cidadania por descendência (regras restringidas em 2025)",
                   "Visto de trabalho (Decreto Flussi)", "Visto de nômade digital"],
        "resumo": "Muitos brasileiros têm direito à cidadania, que abre as portas da União Europeia.",
    },
    {
        "iso3": "CAN", "iso2": "ca", "nome": "Canadá", "continente": "América do Norte",
        "capital": "Ottawa", "coords": (45.4215, -75.6972), "wiki": "Canadá",
        "moeda": {"codigo": "CAD", "nome": "Dólar canadense"},
        "idiomas": ["Inglês", "Francês"],
        "salario_minimo": {"valor": 17.75, "periodo": "hora", "ano_ref": 2025,
                           "obs": "Mínimo federal; cada província define o seu."},
        "idh": 0.939, "custo_vida": 64, "seguranca": 58, "qualidade_vida": 170,
        "vistos": ["Express Entry", "Provincial Nominee Program (PNP)",
                   "Study Permit + PGWP (permissão de trabalho pós-estudo)"],
        "resumo": "Imigração por pontos bem estruturada, com caminho claro para a residência permanente.",
    },
    {
        "iso3": "USA", "iso2": "us", "nome": "Estados Unidos", "continente": "América do Norte",
        "capital": "Washington, D.C.", "coords": (38.9072, -77.0369), "wiki": "Estados_Unidos",
        "moeda": {"codigo": "USD", "nome": "Dólar americano"},
        "idiomas": ["Inglês"],
        "salario_minimo": {"valor": 7.25, "periodo": "hora", "ano_ref": 2025,
                           "obs": "Mínimo federal; muitos estados pagam bem mais."},
        "idh": 0.938, "custo_vida": 70, "seguranca": 50, "qualidade_vida": 178,
        "vistos": ["H-1B (trabalho especializado)", "EB-2 NIW (green card por mérito)", "F-1 (estudante)"],
        "resumo": "Os maiores salários em tecnologia, mas o visto é disputado.",
    },
    {
        "iso3": "AUS", "iso2": "au", "nome": "Austrália", "continente": "Oceania",
        "capital": "Camberra", "coords": (-35.2809, 149.13), "wiki": "Austrália",
        "moeda": {"codigo": "AUD", "nome": "Dólar australiano"},
        "idiomas": ["Inglês"],
        "salario_minimo": {"valor": 24.95, "periodo": "hora", "ano_ref": 2025},
        "idh": 0.958, "custo_vida": 68, "seguranca": 57, "qualidade_vida": 190,
        "vistos": ["Skilled Independent (subclasse 189)", "Skills in Demand (patrocinado)",
                   "Student visa (subclasse 500)"],
        "resumo": "Um dos maiores salários mínimos do mundo, e estudantes podem trabalhar.",
    },
    {
        "iso3": "NZL", "iso2": "nz", "nome": "Nova Zelândia", "continente": "Oceania",
        "capital": "Wellington", "coords": (-41.2865, 174.7762), "wiki": "Nova_Zelândia",
        "moeda": {"codigo": "NZD", "nome": "Dólar neozelandês"},
        "idiomas": ["Inglês", "Maori"],
        "salario_minimo": {"valor": 23.50, "periodo": "hora", "ano_ref": 2025},
        "idh": 0.938, "custo_vida": 63, "seguranca": 58, "qualidade_vida": 175,
        "vistos": ["Skilled Migrant Category", "Accredited Employer Work Visa", "Student visa"],
        "resumo": "Natureza, tranquilidade e equilíbrio entre trabalho e vida pessoal.",
    },
    {
        "iso3": "JPN", "iso2": "jp", "nome": "Japão", "continente": "Ásia",
        "capital": "Tóquio", "coords": (35.6762, 139.6503), "wiki": "Japão",
        "moeda": {"codigo": "JPY", "nome": "Iene"},
        "idiomas": ["Japonês"],
        "salario_minimo": {"valor": 1121, "periodo": "hora", "ano_ref": 2025,
                           "obs": "Média nacional ponderada; varia por província."},
        "idh": 0.925, "custo_vida": 43, "seguranca": 77, "qualidade_vida": 170,
        "vistos": ["Visto de descendente (nikkei)", "Engineer / Specialist in Humanities",
                   "Specified Skilled Worker (SSW)"],
        "resumo": "Muito seguro e mais barato do que parece; o idioma é o grande desafio.",
    },
]


# ---------- Países adicionados na segunda versão ----------
# Para não repetir as mesmas chaves 35 vezes, estes países são montados pelas
# funções abaixo, que geram exatamente o mesmo formato da lista acima.

def _pais(iso3, iso2, nome, continente, capital, coords, wiki, moeda, nome_moeda, idiomas,
          salario, idh, custo_vida, seguranca, qualidade_vida, vistos, resumo):
    return {
        "iso3": iso3, "iso2": iso2, "nome": nome, "continente": continente,
        "capital": capital, "coords": coords, "wiki": wiki,
        "moeda": {"codigo": moeda, "nome": nome_moeda}, "idiomas": idiomas,
        "salario_minimo": salario, "idh": idh, "custo_vida": custo_vida,
        "seguranca": seguranca, "qualidade_vida": qualidade_vida,
        "vistos": vistos, "resumo": resumo,
    }


def _mes(valor, ano, obs=None):
    """Salário mínimo definido por mês."""
    return {"valor": valor, "periodo": "mes", "ano_ref": ano, "obs": obs}


def _hora(valor, ano, obs=None):
    """Salário mínimo definido por hora."""
    return {"valor": valor, "periodo": "hora", "ano_ref": ano, "obs": obs}


def _referencia(valor, periodo, ano, obs):
    """Piso de referência para países SEM salário mínimo em lei.

    O valor aproxima o que convenções coletivas ou regras locais garantem para o
    trabalho de menor salário. No site ele aparece com asterisco (*).
    """
    return {"valor": valor, "periodo": periodo, "ano_ref": ano, "obs": obs, "referencia": True}


CONVENCOES = "Não há salário mínimo nacional. Valor aproximado dos pisos das convenções coletivas"

PAISES += [
    # Europa
    _pais("FRA", "fr", "França", "Europa", "Paris", (48.8566, 2.3522), "França", "EUR", "Euro", ["Francês"],
          _hora(11.88, 2025, "SMIC."), 0.920, 60, 54, 165,
          ["Passeport Talent", "Visto de estudante (VLS-TS)", "Visto de trabalho assalariado"],
          "Ensino superior público barato e forte proteção ao trabalhador."),
    _pais("BEL", "be", "Bélgica", "Europa", "Bruxelas", (50.8503, 4.3517), "Bélgica", "EUR", "Euro",
          ["Neerlandês", "Francês", "Alemão"],
          _mes(2070, 2025), 0.951, 62, 53, 165,
          ["Single Permit", "Blue Card UE", "Visto de estudante"],
          "Sede das instituições europeias, com salários altos e três idiomas oficiais."),
    _pais("LUX", "lu", "Luxemburgo", "Europa", "Luxemburgo", (49.6116, 6.1319), "Luxemburgo", "EUR", "Euro",
          ["Luxemburguês", "Francês", "Alemão"],
          _mes(2704, 2025, "Valor para trabalhador não qualificado."), 0.922, 72, 66, 190,
          ["Blue Card UE", "Autorização para trabalhador assalariado", "Visto de estudante"],
          "O maior salário mínimo da Europa e uma grande comunidade de língua portuguesa."),
    _pais("CHE", "ch", "Suíça", "Europa", "Berna", (46.948, 7.4474), "Suíça", "CHF", "Franco suíço",
          ["Alemão", "Francês", "Italiano", "Romanche"],
          _referencia(24.32, "hora", 2025, "Não há salário mínimo nacional. Valor do mínimo do cantão de Genebra."),
          0.970, 110, 74, 195,
          ["Autorização B por contrato de trabalho (cotas para não europeus)", "Visto de estudante"],
          "Salários altíssimos, mas também o custo de vida mais caro da lista."),
    _pais("AUT", "at", "Áustria", "Europa", "Viena", (48.2082, 16.3738), "Áustria", "EUR", "Euro", ["Alemão"],
          _referencia(2000, "mes", 2025, CONVENCOES + " (pago em 14 parcelas)."), 0.930, 62, 72, 185,
          ["Red-White-Red Card", "Blue Card UE", "Visto de estudante"],
          "Viena aparece sempre entre as cidades com melhor qualidade de vida do mundo."),
    _pais("SWE", "se", "Suécia", "Europa", "Estocolmo", (59.3293, 18.0686), "Suécia", "SEK", "Coroa sueca", ["Sueco"],
          _referencia(25000, "mes", 2025, CONVENCOES + "."), 0.959, 60, 53, 180,
          ["Permissão de trabalho", "Blue Card UE", "Visto de estudante"],
          "Estado de bem-estar social forte e muitas empresas de tecnologia."),
    _pais("NOR", "no", "Noruega", "Europa", "Oslo", (59.9139, 10.7522), "Noruega", "NOK", "Coroa norueguesa", ["Norueguês"],
          _referencia(220, "hora", 2025, CONVENCOES + " (limpeza, construção e hotelaria)."), 0.970, 76, 66, 185,
          ["Permissão para trabalhador qualificado", "Visto de estudante"],
          "Um dos países mais ricos do mundo, com salários altos e custo de vida à altura."),
    _pais("DNK", "dk", "Dinamarca", "Europa", "Copenhague", (55.6761, 12.5683), "Dinamarca", "DKK", "Coroa dinamarquesa",
          ["Dinamarquês"],
          _referencia(135, "hora", 2025, CONVENCOES + "."), 0.962, 72, 74, 195,
          ["Pay Limit Scheme", "Positive List (profissões em falta)", "Fast-track"],
          "Equilíbrio entre trabalho e vida pessoal levado a sério."),
    _pais("FIN", "fi", "Finlândia", "Europa", "Helsinque", (60.1699, 24.9384), "Finlândia", "EUR", "Euro",
          ["Finlandês", "Sueco"],
          _referencia(1900, "mes", 2025, CONVENCOES + "."), 0.948, 64, 75, 190,
          ["Specialist permit", "Permissão para trabalhador", "Visto de estudante"],
          "Eleita várias vezes o país mais feliz do mundo; o inverno é longo."),
    _pais("ISL", "is", "Islândia", "Europa", "Reykjavík", (64.1466, -21.9426), "Islândia", "ISK", "Coroa islandesa",
          ["Islandês"],
          _referencia(425000, "mes", 2024, CONVENCOES + "."), 0.972, 88, 76, 180,
          ["Permissão para especialista", "Permissão para profissão em falta"],
          "Muito segura e com salários altos, mas pequena e cara."),
    _pais("POL", "pl", "Polônia", "Europa", "Varsóvia", (52.2297, 21.0122), "Polônia", "PLN", "Złoty", ["Polonês"],
          _mes(4666, 2025), 0.906, 42, 71, 150,
          ["Permissão de trabalho (tipo A)", "Blue Card UE", "Visto de estudante"],
          "Economia que mais cresce na UE, com custo de vida baixo."),
    _pais("CZE", "cz", "República Tcheca", "Europa", "Praga", (50.0755, 14.4378), "República_Checa", "CZK", "Coroa tcheca",
          ["Tcheco"],
          _mes(20800, 2025), 0.915, 45, 74, 160,
          ["Employee Card", "Blue Card UE", "Visto de estudante"],
          "Praga é segura, barata para a Europa e cheia de vagas em TI."),
    _pais("GRC", "gr", "Grécia", "Europa", "Atenas", (37.9838, 23.7275), "Grécia", "EUR", "Euro", ["Grego"],
          _mes(880, 2025, "Pago em 14 parcelas por ano."), 0.908, 50, 55, 130,
          ["Golden Visa (investimento)", "Visto de nômade digital", "Blue Card UE"],
          "Clima mediterrâneo e custo baixo; salários ainda modestos."),
    _pais("MLT", "mt", "Malta", "Europa", "Valletta", (35.8989, 14.5146), "Malta", "EUR", "Euro", ["Maltês", "Inglês"],
          _mes(961, 2025), 0.924, 58, 57, 140,
          ["Nomad Residence Permit", "Single Permit", "Key Employee Initiative"],
          "Inglês como língua oficial, destino popular para intercâmbio."),
    _pais("HRV", "hr", "Croácia", "Europa", "Zagreb", (45.815, 15.9819), "Croácia", "EUR", "Euro", ["Croata"],
          _mes(970, 2025), 0.889, 48, 74, 150,
          ["Visto de nômade digital", "Permissão de trabalho e residência"],
          "Litoral bonito, segura e com custo de vida moderado."),
    _pais("HUN", "hu", "Hungria", "Europa", "Budapeste", (47.4979, 19.0402), "Hungria", "HUF", "Florim húngaro", ["Húngaro"],
          _mes(290800, 2025), 0.870, 42, 68, 140,
          ["White Card (nômade digital)", "Guest Worker Permit", "Blue Card UE"],
          "Budapeste é uma das capitais mais baratas da UE."),
    _pais("EST", "ee", "Estônia", "Europa", "Tallinn", (59.437, 24.7536), "Estônia", "EUR", "Euro", ["Estoniano"],
          _mes(886, 2025), 0.905, 52, 76, 170,
          ["Digital Nomad Visa", "Startup Visa", "e-Residency (não dá direito a morar)"],
          "O país mais digital da Europa, muito procurado por quem abre startup."),
    _pais("CYP", "cy", "Chipre", "Europa", "Nicósia", (35.1856, 33.3823), "Chipre", "EUR", "Euro", ["Grego", "Turco"],
          _mes(1000, 2025), 0.913, 55, 67, 155,
          ["Visto de nômade digital", "Blue Card UE", "Permissão para profissional altamente qualificado"],
          "Sol o ano inteiro, inglês muito usado e impostos baixos."),

    # América Latina e México
    _pais("CHL", "cl", "Chile", "América Latina", "Santiago", (-33.4489, -70.6693), "Chile", "CLP", "Peso chileno",
          ["Espanhol"],
          _mes(529000, 2025), 0.878, 42, 40, 115,
          ["Residência temporária", "Acordo de Residência do Mercosul"],
          "Economia estável e o maior IDH da América do Sul."),
    _pais("URY", "uy", "Uruguai", "América Latina", "Montevidéu", (-34.9011, -56.1645), "Uruguai", "UYU", "Peso uruguaio",
          ["Espanhol"],
          _mes(23604, 2025), 0.862, 50, 46, 120,
          ["Residência pelo Mercosul", "Residência permanente"],
          "Vizinho tranquilo, com burocracia simples para brasileiros."),
    _pais("ARG", "ar", "Argentina", "América Latina", "Buenos Aires", (-34.6037, -58.3816), "Argentina", "ARS",
          "Peso argentino", ["Espanhol"],
          _mes(322000, 2025, "Reajustado com frequência por causa da inflação."), 0.865, 40, 37, 105,
          ["Residência pelo Mercosul", "Visto de nômade digital"],
          "Universidade pública gratuita e vida cultural intensa; economia instável."),
    _pais("PRY", "py", "Paraguai", "América Latina", "Assunção", (-25.2637, -57.5759), "Paraguai", "PYG", "Guarani",
          ["Espanhol", "Guarani"],
          _mes(2899048, 2025), 0.756, 30, 50, 110,
          ["Residência pelo Mercosul", "Residência permanente"],
          "Custo de vida baixo e impostos entre os menores do continente."),
    _pais("PAN", "pa", "Panamá", "América Latina", "Cidade do Panamá", (8.9824, -79.5199), "Panamá", "USD",
          "Dólar americano (e balboa)", ["Espanhol"],
          _mes(636, 2025, "Varia por região e setor; valor aproximado."), 0.839, 45, 50, 120,
          ["Friendly Nations Visa", "Visto Pensionado (aposentados)"],
          "Economia dolarizada e centro logístico das Américas."),
    _pais("CRI", "cr", "Costa Rica", "América Latina", "San José", (9.9281, -84.0907), "Costa_Rica", "CRC",
          "Colón costa-riquenho", ["Espanhol"],
          _mes(365015, 2025, "Valor para trabalhador não qualificado."), 0.833, 48, 45, 120,
          ["Visto de nômade digital", "Rentista", "Pensionado"],
          "Natureza preservada, sem exército e com boa saúde pública."),
    _pais("COL", "co", "Colômbia", "América Latina", "Bogotá", (4.711, -74.0721), "Colômbia", "COP", "Peso colombiano",
          ["Espanhol"],
          _mes(1423500, 2025), 0.788, 28, 38, 100,
          ["Visto V de nômade digital", "Visto M de trabalho", "Residência pelo Mercosul"],
          "Custo de vida muito baixo; Medellín virou polo de nômades digitais."),
    _pais("MEX", "mx", "México", "América do Norte", "Cidade do México", (19.4326, -99.1332), "México", "MXN",
          "Peso mexicano", ["Espanhol"],
          _mes(8480, 2025, "MXN 278,80 por dia; mais alto na fronteira norte."), 0.789, 38, 46, 110,
          ["Residência temporária por solvência econômica", "Visto de trabalho"],
          "Grande mercado, vizinho dos EUA e muito procurado por nômades digitais."),

    # Ásia e Oriente Médio
    _pais("ARE", "ae", "Emirados Árabes Unidos", "Ásia", "Abu Dhabi", (24.4539, 54.3773), "Emirados_Árabes_Unidos",
          "AED", "Dirham", ["Árabe", "Inglês"],
          _referencia(1500, "mes", 2025, "Não há salário mínimo. Valor aproximado pago em funções de entrada; vagas qualificadas pagam bem mais."),
          0.940, 55, 84, 165,
          ["Golden Visa", "Green Visa", "Visto de trabalho patrocinado", "Remote Work Visa"],
          "Sem imposto de renda e muito seguro; Dubai concentra as vagas."),
    _pais("SGP", "sg", "Singapura", "Ásia", "Singapura", (1.3521, 103.8198), "Singapura", "SGD", "Dólar de Singapura",
          ["Inglês", "Malaio", "Mandarim", "Tâmil"],
          _referencia(1800, "mes", 2025, "Não há salário mínimo nacional. Valor do Local Qualifying Salary, o mínimo que a empresa precisa pagar a locais para poder contratar estrangeiros."),
          0.946, 85, 77, 165,
          ["Employment Pass", "S Pass", "ONE Pass (talentos)"],
          "Centro financeiro da Ásia, em inglês, mas com aluguel caríssimo."),
    _pais("KOR", "kr", "Coreia do Sul", "Ásia", "Seul", (37.5665, 126.978), "Coreia_do_Sul", "KRW", "Won", ["Coreano"],
          _hora(10030, 2025), 0.937, 58, 74, 140,
          ["E-7 (profissional)", "D-10 (procura de emprego)", "D-2 (estudante)"],
          "Tecnologia de ponta e cidades seguras; a jornada de trabalho é longa."),
    _pais("ISR", "il", "Israel", "Ásia", "Jerusalém", (31.7683, 35.2137), "Israel", "ILS", "Novo shekel",
          ["Hebraico", "Árabe"],
          _mes(6248, 2025), 0.919, 70, 67, 150,
          ["Lei do Retorno (descendentes de judeus)", "Visto B/1 de trabalho para especialistas"],
          "Ecossistema de startups forte; a situação de segurança varia muito."),
    _pais("QAT", "qa", "Catar", "Ásia", "Doha", (25.2854, 51.531), "Catar", "QAR", "Rial catariano", ["Árabe"],
          _mes(1800, 2025, "QAR 1.000 de salário + 800 de auxílio moradia e alimentação."), 0.886, 55, 85, 170,
          ["Visto de trabalho patrocinado pelo empregador"],
          "Sem imposto de renda e muito seguro; a imigração depende do empregador."),
    _pais("THA", "th", "Tailândia", "Ásia", "Bangkok", (13.7563, 100.5018), "Tailândia", "THB", "Baht", ["Tailandês"],
          _mes(10400, 2025, "THB 400 por dia em Bangkok, 26 dias por mês."), 0.798, 35, 61, 105,
          ["Destination Thailand Visa (DTV)", "Long-Term Resident (LTR)", "Non-Immigrant B"],
          "Barato e acolhedor para nômades digitais; salários locais baixos."),

    # África
    _pais("ZAF", "za", "África do Sul", "África", "Pretória", (-25.7479, 28.2293), "África_do_Sul", "ZAR", "Rand",
          ["Inglês", "Zulu", "Africâner", "e outros"],
          _hora(28.79, 2025), 0.741, 38, 25, 130,
          ["Critical Skills Work Visa", "General Work Visa", "Remote Work Visa"],
          "Economia mais diversificada da África; a violência urbana é alta."),
    _pais("AGO", "ao", "Angola", "África", "Luanda", (-8.839, 13.2894), "Angola", "AOA", "Kwanza", ["Português"],
          _mes(70000, 2024, "Valor para grandes empresas."), 0.616, 40, 35, 70,
          ["Visto de trabalho", "Visto de fixação de residência"],
          "Fala português e tem demanda em petróleo e construção; Luanda é cara."),
    _pais("CPV", "cv", "Cabo Verde", "África", "Praia", (14.933, -23.5133), "Cabo_Verde", "CVE", "Escudo cabo-verdiano",
          ["Português", "Crioulo"],
          _mes(15000, 2023), 0.668, 38, 55, 90,
          ["Remote Working Cabo Verde", "Autorização de residência"],
          "Arquipélago lusófono, tranquilo e com programa para trabalho remoto."),
]

# Indicadores buscados na API do Banco Mundial.
# "melhor" diz se o valor mais alto ou o mais baixo é o melhor (usado no comparador).
INDICADORES_BM = {
    "pib":        {"codigo": "NY.GDP.PCAP.CD", "nome": "PIB per capita", "unidade": "US$", "melhor": "alto"},
    "vida":       {"codigo": "SP.DYN.LE00.IN", "nome": "Expectativa de vida", "unidade": "anos", "melhor": "alto"},
    "homicidios": {"codigo": "VC.IHR.PSRC.P5", "nome": "Homicídios por 100 mil hab.", "unidade": "", "melhor": "baixo"},
    "desemprego": {"codigo": "SL.UEM.TOTL.ZS", "nome": "Desemprego", "unidade": "%", "melhor": "baixo"},
    "inflacao":   {"codigo": "FP.CPI.TOTL.ZG", "nome": "Inflação anual", "unidade": "%", "melhor": "baixo"},
    "populacao":  {"codigo": "SP.POP.TOTL", "nome": "População", "unidade": "", "melhor": None},
}

CONTINENTES = ["Europa", "América do Norte", "América Latina", "Ásia", "Oceania", "África"]


def buscar_pais(iso3):
    """Devolve o país com o código ISO informado (ou o Brasil), ou None."""
    if iso3 == "BRA":
        return BRASIL
    return next((p for p in PAISES if p["iso3"] == iso3), None)
