"""Guia do Imigrante: aplicação web em Flask.

O Flask recebe a visita, consulta as APIs externas (módulo apis.py), faz as
contas e devolve a página HTML pronta, montada com os templates da pasta
templates/. O mapa é gerado em Python com a biblioteca folium.

Para rodar localmente:  python app.py   e abrir http://localhost:5000
"""

import unicodedata
from datetime import datetime

import folium
from flask import Flask, abort, render_template, request

import apis
import quiz
from dados import BRASIL, CONTINENTES, HORAS_POR_MES, INDICADORES_BM, PAISES, buscar_pais

app = Flask(__name__)

SIMBOLOS = {"EUR": "€", "USD": "US$", "GBP": "£", "CAD": "C$", "AUD": "A$",
            "NZD": "NZ$", "JPY": "¥", "BRL": "R$", "CHF": "CHF", "KRW": "₩",
            "ILS": "₪", "THB": "฿", "PLN": "zł", "MXN": "MX$", "SGD": "S$"}
# Moedas em que não se usam centavos no dia a dia
SEM_CENTAVOS = {"JPY", "KRW", "CLP", "PYG", "COP", "CRC", "HUF", "ISK", "AOA", "CVE", "ARS"}

# Colunas que podem ordenar a tabela / colorir o mapa
METRICAS = {
    "salario_brl": "Salário mínimo",
    "poder_compra": "Poder de compra",
    "custo_vida": "Custo de vida (mais barato)",
    "seguranca": "Segurança",
    "qualidade_vida": "Qualidade de vida",
    "idh": "IDH",
}
# Nesses indicadores, quanto menor, melhor
MENOR_E_MELHOR = {"custo_vida"}


# ---------- Formatação no padrão brasileiro (usada nos templates) ----------

@app.template_filter("numero")
def fmt_numero(valor, casas=0):
    """1234.5 -> '1.234,5'. Valores ausentes viram um traço."""
    if valor is None:
        return "–"
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


@app.template_filter("reais")
def fmt_reais(valor):
    return "–" if valor is None else "R$ " + fmt_numero(valor)


@app.template_filter("moeda")
def fmt_moeda(valor, codigo, casas=2):
    """Valor com o símbolo da moeda. Moedas como iene e won ficam sem centavos."""
    if valor is None:
        return "–"
    if codigo in SEM_CENTAVOS:
        casas = 0
    return f"{SIMBOLOS.get(codigo, codigo)} {fmt_numero(valor, casas)}"


@app.template_filter("populacao")
def fmt_populacao(valor):
    if valor is None:
        return "–"
    return fmt_numero(valor / 1e6, 1) + " mi" if valor >= 1e6 else fmt_numero(valor)


# ---------- Cálculos ----------

def salario_mensal_local(pais):
    """Salário mínimo por mês na moeda do país (converte quem paga por hora)."""
    s = pais["salario_minimo"]
    if s["valor"] is None:
        return None
    return s["valor"] * HORAS_POR_MES if s["periodo"] == "hora" else s["valor"]


def para_reais(valor, moeda, taxas):
    """Converte para reais. A API informa quanto 1 real vale em cada moeda, por isso dividimos."""
    if valor is None or taxas is None:
        return None
    if moeda == "BRL":
        return valor
    taxa = taxas.get(moeda)
    return valor / taxa if taxa else None


def poder_de_compra(salario_brl, custo_vida):
    """Quanto o mínimo local rende comparado ao brasileiro.

    (salário em R$ / custo de vida do país) dividido pela mesma conta feita para o Brasil.
    2,0 significa que o salário mínimo local compra o dobro do brasileiro.
    """
    if salario_brl is None:
        return None
    brasil = BRASIL["salario_minimo"]["valor"] / BRASIL["custo_vida"]
    return (salario_brl / custo_vida) / brasil


def resumo_pais(pais, taxas):
    """Junta os dados do país com os valores calculados a partir do câmbio."""
    mensal = salario_mensal_local(pais)
    salario_brl = para_reais(mensal, pais["moeda"]["codigo"], taxas)
    return {
        **pais,
        "salario_mensal": mensal,
        "salario_brl": salario_brl,
        "poder_compra": poder_de_compra(salario_brl, pais["custo_vida"]),
        # True quando o país não tem mínimo em lei e usamos um piso de referência
        "referencia": pais["salario_minimo"].get("referencia", False),
    }


def ordenar(linhas, ordem):
    """Ordena pela métrica escolhida; países sem valor vão para o fim."""
    if ordem == "nome":
        return sorted(linhas, key=lambda p: p["nome"])
    com_valor = [p for p in linhas if p[ordem] is not None]
    sem_valor = [p for p in linhas if p[ordem] is None]
    com_valor.sort(key=lambda p: p[ordem], reverse=ordem not in MENOR_E_MELHOR)
    return com_valor + sem_valor


def sem_acento(texto):
    """Minúsculas e sem acentos, para a busca achar "japao" em "Japão"."""
    normal = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in normal if unicodedata.category(c) != "Mn")


def texto_cambio(taxas, atualizado_em):
    if not taxas:
        return None
    data = datetime.fromtimestamp(atualizado_em).strftime("%d/%m/%Y")
    partes = [f"1 {m} = {fmt_moeda(1 / taxas[m], 'BRL')}" for m in ("EUR", "USD", "GBP", "CAD")]
    return f"Câmbio de {data}: " + " · ".join(partes)


# ---------- Páginas ----------

@app.route("/")
def inicio():
    taxas, atualizado_em = apis.cotacoes()

    # Filtros e ordenação chegam pela URL, ex.: /?continente=Europa&ordem=seguranca
    continente = request.args.get("continente", "")
    busca = request.args.get("busca", "").strip()
    ordem = request.args.get("ordem", "salario_brl")
    if ordem not in METRICAS and ordem != "nome":
        ordem = "salario_brl"
    metrica = request.args.get("metrica", "salario_brl")
    if metrica not in METRICAS:
        metrica = "salario_brl"

    linhas = [resumo_pais(p, taxas) for p in PAISES]
    linhas = [p for p in linhas
              if (not continente or p["continente"] == continente)
              and sem_acento(busca) in sem_acento(p["nome"])]

    return render_template(
        "index.html",
        linhas=ordenar(linhas, ordem),
        brasil=resumo_pais(BRASIL, taxas),
        continentes=CONTINENTES, continente=continente, busca=busca, ordem=ordem,
        metricas=METRICAS, metrica=metrica,
        cambio=texto_cambio(taxas, atualizado_em),
        edicao=f"Edição de {mes_atual()} · {len(PAISES)} países", total=len(PAISES),
    )


@app.route("/mapa")
def mapa():
    """Mapa gerado com folium (Leaflet + OpenStreetMap). A página inicial o exibe num iframe."""
    taxas, _ = apis.cotacoes()
    metrica = request.args.get("metrica", "salario_brl")
    if metrica not in METRICAS:
        metrica = "salario_brl"

    paises = [resumo_pais(p, taxas) for p in PAISES]
    valores = [p[metrica] for p in paises if p[metrica] is not None]
    minimo, maximo = min(valores, default=0), max(valores, default=1)

    m = folium.Map(location=[20, 30], zoom_start=2, min_zoom=1, max_zoom=8,
                   tiles="OpenStreetMap", scrollWheelZoom=False)

    for p in paises:
        valor = p[metrica]
        if valor is None:
            cor = "#ffffff"  # sem dado (a Itália não tem salário mínimo nacional)
        else:
            t = 0.5 if maximo == minimo else (valor - minimo) / (maximo - minimo)
            if metrica in MENOR_E_MELHOR:
                t = 1 - t
            cor = cor_escala(t)

        popup = (f"<b style='font-size:15px'>{p['nome']}</b><br>"
                 f"mínimo {fmt_reais(p['salario_brl'])}{'*' if p['referencia'] else ''}<br>"
                 f"custo de vida {p['custo_vida']} · segurança {p['seguranca']}<br>"
                 f"<a href='/pais/{p['iso3']}' target='_top'>Abrir ficha</a>")
        folium.CircleMarker(
            location=p["coords"], radius=9, weight=1.5, color="#1c1b19",
            fill=True, fill_color=cor, fill_opacity=1,
            tooltip=p["nome"], popup=folium.Popup(popup, max_width=240),
        ).add_to(m)

    # Enquadra o mapa para caber todos os países, dos EUA à Nova Zelândia
    m.fit_bounds([[-42, -80], [55, 176]])
    return m.get_root().render()


def cor_escala(t):
    """Um só tom de azul: claro (pior, t=0) até escuro (melhor, t=1)."""
    return f"hsl(213, 48%, {86 - t * 62:.0f}%)"


@app.route("/pais/<iso3>")
def pais(iso3):
    dados_pais = buscar_pais(iso3.upper())
    if dados_pais is None or dados_pais is BRASIL:
        abort(404)

    taxas, _ = apis.cotacoes()
    bm, _ = apis.indicadores_banco_mundial([p["iso3"] for p in PAISES] + ["BRA"])
    p = resumo_pais(dados_pais, taxas)
    codigo = p["moeda"]["codigo"]
    taxa = taxas.get(codigo) if taxas else None

    # Conversor: o valor em reais vem do formulário (?valor=3000)
    try:
        valor = float(request.args.get("valor", 3000))
    except ValueError:
        valor = 3000
    convertido = valor * taxa if taxa else None
    pct_minimo = convertido / p["salario_mensal"] * 100 if convertido and p["salario_mensal"] else None

    clima = apis.clima_agora(*p["coords"])
    if clima:
        clima["descricao"] = apis.descrever_tempo(clima["codigo"])

    return render_template(
        "pais.html", p=p, brasil=BRASIL, horas_mes=HORAS_POR_MES,
        taxa=taxa, valor=valor, convertido=convertido, pct_minimo=pct_minimo,
        bm=bm.get(p["iso3"], {}), bm_brasil=bm.get("BRA", {}), indicadores=INDICADORES_BM,
        clima=clima, wiki=apis.resumo_wikipedia(p["wiki"]),
    )


@app.route("/comparar")
def comparar():
    taxas, _ = apis.cotacoes()
    bm, _ = apis.indicadores_banco_mundial([p["iso3"] for p in PAISES] + ["BRA"])
    opcoes = PAISES + [BRASIL]

    a = resumo_pais(buscar_pais(request.args.get("a", "PRT")) or PAISES[0], taxas)
    b = resumo_pais(buscar_pais(request.args.get("b", "CAN")) or buscar_pais("CAN"), taxas)
    bm_a, bm_b = bm.get(a["iso3"], {}), bm.get(b["iso3"], {})

    # Cada linha: (nome, valor A, valor B, texto A, texto B, qual é melhor)
    linhas = [
        ("Salário mínimo (R$/mês)", a["salario_brl"], b["salario_brl"], fmt_reais, "alto"),
        ("Poder de compra (Brasil = 1)", a["poder_compra"], b["poder_compra"], lambda v: fmt_numero(v, 2), "alto"),
        ("Custo de vida", a["custo_vida"], b["custo_vida"], fmt_numero, "baixo"),
        ("Segurança", a["seguranca"], b["seguranca"], fmt_numero, "alto"),
        ("Qualidade de vida", a["qualidade_vida"], b["qualidade_vida"], fmt_numero, "alto"),
        ("IDH", a["idh"], b["idh"], lambda v: fmt_numero(v, 3), "alto"),
    ]
    for chave, ind in INDICADORES_BM.items():
        unidade = f" ({ind['unidade']})" if ind["unidade"] else ""
        if chave == "populacao":
            fmt = fmt_populacao
        else:
            fmt = (lambda casas: lambda v: fmt_numero(v, casas))(0 if chave == "pib" else 1)
        linhas.append((ind["nome"] + unidade,
                       bm_a.get(chave, {}).get("valor"), bm_b.get(chave, {}).get("valor"),
                       fmt, ind["melhor"]))

    tabela = []
    for nome, va, vb, fmt, melhor in linhas:
        vence_a = vence_b = False
        if melhor and va is not None and vb is not None and va != vb:
            a_melhor = va > vb if melhor == "alto" else va < vb
            vence_a, vence_b = a_melhor, not a_melhor
        tabela.append({"nome": nome, "a": fmt(va), "b": fmt(vb), "vence_a": vence_a, "vence_b": vence_b})

    # As duas primeiras linhas dependem do salário: marca com * o piso de referência
    for linha in tabela[:2]:
        if a["referencia"]:
            linha["a"] += "*"
        if b["referencia"]:
            linha["b"] += "*"

    return render_template("comparar.html", a=a, b=b, opcoes=opcoes, tabela=tabela)


@app.route("/quiz")
def pagina_quiz():
    """Mostra as perguntas; quando todas vêm respondidas na URL, mostra também o resultado."""
    respostas = quiz.respostas_validas(request.args)
    resultado = None
    if respostas:
        taxas, _ = apis.cotacoes()
        resultado = quiz.calcular(respostas, [resumo_pais(p, taxas) for p in PAISES])
    return render_template("quiz.html", perguntas=quiz.perguntas_formatadas(),
                           respostas=respostas or request.args, resultado=resultado,
                           faltou=bool(request.args) and not respostas)


@app.route("/fontes")
def fontes():
    # Consulta as APIs para mostrar se estão respondendo agora
    taxas, _ = apis.cotacoes()
    _, bm_ok = apis.indicadores_banco_mundial([p["iso3"] for p in PAISES] + ["BRA"])
    status = {"Banco Mundial": bm_ok, "Câmbio": taxas is not None}
    return render_template("fontes.html", status=status)


@app.errorhandler(404)
def nao_encontrado(_):
    return render_template("404.html"), 404


def mes_atual():
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
             "agosto", "setembro", "outubro", "novembro", "dezembro"]
    hoje = datetime.now()
    return f"{meses[hoje.month - 1]} de {hoje.year}"


if __name__ == "__main__":
    app.run(debug=True)
