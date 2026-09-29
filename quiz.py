"""Quiz "Qual país combina com você?".

Cada resposta vira um peso ou um ajuste na nota dos países. A nota final junta:
- os índices do país (salário, custo de vida, segurança, qualidade de vida),
  normalizados de 0 a 1 e multiplicados pela importância que a pessoa deu;
- ajustes por idioma, região, clima e objetivo da mudança.
"""

# Perguntas do quiz: (chave, pergunta, [(valor, texto da opção), ...])
PERGUNTAS = [
    ("idioma", "Que idioma você fala ou topa aprender?", [
        ("pt", "Só português"),
        ("es", "Espanhol"),
        ("en", "Inglês"),
        ("todos", "Qualquer um, aprendo o que precisar"),
    ]),
    ("regiao", "Onde você se imagina morando?", [
        ("europa", "Europa"),
        ("americas", "Nas Américas, mais perto do Brasil"),
        ("asia", "Ásia, Oriente Médio ou Oceania"),
        ("qualquer", "Tanto faz"),
    ]),
    ("clima", "E o frio?", [
        ("calor", "Prefiro calor, inverno rigoroso não"),
        ("qualquer", "Frio não é problema"),
    ]),
    ("objetivo", "Como você pretende ir?", [
        ("estudo", "Estudando"),
        ("remoto", "Trabalhando remoto para fora (nômade digital)"),
        ("emprego", "Arrumando emprego lá"),
        ("indeciso", "Ainda não sei"),
    ]),
    ("salario", "Quanto pesa ganhar bem, em reais?", "importancia"),
    ("custo", "Quanto pesa ter custo de vida baixo?", "importancia"),
    ("seguranca", "Quanto pesa a segurança?", "importancia"),
    ("qualidade", "Quanto pesa a qualidade de vida em geral?", "importancia"),
]

# Opções das perguntas de importância (valor = peso na nota)
IMPORTANCIA = [("0", "Nada"), ("1", "Pouco"), ("2", "Bastante"), ("3", "Muito")]

# Idiomas de cada opção da primeira pergunta
IDIOMAS = {"pt": {"Português"}, "es": {"Português", "Espanhol"}, "en": {"Português", "Inglês"}}

REGIOES = {
    "europa": {"Europa"},
    "americas": {"América do Norte", "América Latina"},
    "asia": {"Ásia", "Oceania"},
}

# Palavras procuradas nas rotas de visto do país para cada objetivo
PALAVRAS_OBJETIVO = {
    "estudo": ["estudante", "student", "study"],
    "remoto": ["nômade", "nomad", "remote", "remot", "dtv"],
    "emprego": ["trabalh", "work", "skilled", "blue card", "employ", "permit", "specialist",
                "express entry", "employment pass", "s pass", "e-7", "h-1b", "red-white"],
}


def perguntas_formatadas():
    """Lista de perguntas pronta para o template (as de importância recebem as opções)."""
    return [(chave, texto, IMPORTANCIA if opcoes == "importancia" else opcoes)
            for chave, texto, opcoes in PERGUNTAS]


def respostas_validas(args):
    """Lê as respostas da URL. Retorna None se faltar alguma."""
    respostas = {}
    for chave, _, opcoes in perguntas_formatadas():
        valor = args.get(chave)
        if valor not in {v for v, _ in opcoes}:
            return None
        respostas[chave] = valor
    return respostas


def _normalizar(paises, campo, inverter=False):
    """Transforma os valores de um campo em notas de 0 a 1 (1 = melhor)."""
    valores = [p[campo] for p in paises if p[campo] is not None]
    minimo, maximo = min(valores), max(valores)
    notas = {}
    for p in paises:
        v = p[campo]
        if v is None:
            notas[p["iso3"]] = 0.5  # sem dado: fica no meio, sem ganhar nem perder
            continue
        t = (v - minimo) / (maximo - minimo) if maximo > minimo else 0.5
        notas[p["iso3"]] = 1 - t if inverter else t
    return notas


def calcular(respostas, paises):
    """Dá uma nota de 0 a 100 para cada país e devolve os 5 melhores com os motivos.

    `paises` já deve vir com salario_brl calculado (ver resumo_pais em app.py).
    """
    pesos = {
        "salario_brl": int(respostas["salario"]),
        "custo_vida": int(respostas["custo"]),
        "seguranca": int(respostas["seguranca"]),
        "qualidade_vida": int(respostas["qualidade"]),
    }
    notas = {campo: _normalizar(paises, campo, inverter=(campo == "custo_vida")) for campo in pesos}
    soma_pesos = sum(pesos.values()) or 1

    resultado = []
    for p in paises:
        iso = p["iso3"]
        motivos, alertas = [], []

        # Parte principal: média ponderada dos índices
        nota = sum(pesos[c] * notas[c][iso] for c in pesos) / soma_pesos
        if pesos["salario_brl"] and notas["salario_brl"][iso] >= 0.6 and p["salario_brl"]:
            motivos.append("salário mínimo alto em reais")
        if pesos["custo_vida"] and notas["custo_vida"][iso] >= 0.6:
            motivos.append("custo de vida baixo")
        if pesos["seguranca"] and notas["seguranca"][iso] >= 0.6:
            motivos.append("bem seguro")
        if pesos["qualidade_vida"] and notas["qualidade_vida"][iso] >= 0.6:
            motivos.append("ótima qualidade de vida")

        # Idioma: não elimina o país, mas pesa bastante
        if respostas["idioma"] != "todos":
            aceitos = IDIOMAS[respostas["idioma"]]
            if aceitos & set(p["idiomas"]):
                motivos.insert(0, "você já fala o idioma")
            else:
                nota *= 0.6
                alertas.append(f"idioma local: {', '.join(p['idiomas'][:2])}")

        # Região preferida
        if respostas["regiao"] != "qualquer" and p["continente"] not in REGIOES[respostas["regiao"]]:
            nota *= 0.5

        # Clima: usa a latitude da capital como aproximação (acima de 45° os invernos são duros)
        if respostas["clima"] == "calor" and abs(p["coords"][0]) > 45:
            nota *= 0.75
            alertas.append("inverno rigoroso")

        # Objetivo: bônus se alguma rota de visto combina
        if respostas["objetivo"] in PALAVRAS_OBJETIVO:
            texto_vistos = " ".join(p["vistos"]).lower()
            if any(palavra in texto_vistos for palavra in PALAVRAS_OBJETIVO[respostas["objetivo"]]):
                nota = min(1, nota + 0.1)
                rota = next(v for v in p["vistos"]
                            if any(pal in v.lower() for pal in PALAVRAS_OBJETIVO[respostas["objetivo"]]))
                motivos.append(f"tem rota para o seu caso: {rota}")

        resultado.append({"pais": p, "nota": round(nota * 100), "motivos": motivos, "alertas": alertas})

    resultado.sort(key=lambda r: r["nota"], reverse=True)
    return resultado[:5]
