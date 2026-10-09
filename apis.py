"""Comunicação com as APIs externas (os servidores que o site consome).

- Banco Mundial ........ indicadores socioeconômicos de cada país
- ExchangeRate-API ..... cotação das moedas em reais
- Open-Meteo ........... tempo agora na capital
- Wikipedia ............ resumo do país em português

Nenhuma delas exige chave. As respostas ficam guardadas em memória por um
tempo (cache) para o site não repetir a mesma consulta a cada visita.
"""

import time

import requests

from dados import INDICADORES_BM

URL_BANCO_MUNDIAL = "https://api.worldbank.org/v2"
URL_CAMBIO = "https://open.er-api.com/v6/latest/BRL"
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
URL_WIKIPEDIA = "https://pt.wikipedia.org/api/rest_v1/page/summary/"

# A Wikipedia pede que todo cliente se identifique
CABECALHOS = {"User-Agent": "GuiaDoImigrante/1.0 (trabalho academico)"}
TEMPO_LIMITE = 10  # segundos de espera por resposta

# Cache em memória: chave -> (momento em que foi salvo, valor)
_cache = {}


def _com_cache(chave, validade, funcao):
    """Devolve o valor guardado se ainda for válido; senão chama a função e guarda.

    Se a API estiver fora do ar e existir um valor antigo guardado, devolve o
    antigo em vez de falhar: é melhor mostrar o câmbio de uma hora atrás do que nada.
    """
    agora = time.time()
    if chave in _cache and agora - _cache[chave][0] < validade:
        return _cache[chave][1]
    try:
        valor = funcao()
    except (requests.RequestException, KeyError, ValueError):
        if chave in _cache:
            return _cache[chave][1]
        raise
    _cache[chave] = (agora, valor)
    return valor


def _get_json(url, params=None):
    """GET que devolve o JSON da resposta ou lança erro se o status não for 2xx."""
    resposta = requests.get(url, params=params, headers=CABECALHOS, timeout=TEMPO_LIMITE)
    resposta.raise_for_status()
    return resposta.json()


# ---------- Banco Mundial ----------

def _buscar_indicador(codigos_paises, codigo_indicador):
    """Valor mais recente de um indicador para vários países.

    mrnev=1 pede o último valor que não está vazio. A resposta tem o formato
    [metadados, [ {countryiso3code, date, value}, ... ]].
    """
    url = f"{URL_BANCO_MUNDIAL}/country/{';'.join(codigos_paises)}/indicator/{codigo_indicador}"
    _, registros = _get_json(url, {"format": "json", "mrnev": 1, "per_page": 100})
    resultado = {}
    for r in registros or []:
        if r["value"] is not None:
            resultado[r["countryiso3code"]] = {"valor": r["value"], "ano": r["date"]}
    return resultado


def indicadores_banco_mundial(codigos_paises):
    """Todos os indicadores de INDICADORES_BM, organizados por país.

    Retorna {"PRT": {"pib": {"valor": ..., "ano": ...}, ...}, ...} e um booleano
    que diz se a API respondeu. Um indicador que falha não derruba os outros.
    """
    def buscar():
        por_pais = {iso: {} for iso in codigos_paises}
        algum_ok = False
        for chave, indicador in INDICADORES_BM.items():
            try:
                valores = _buscar_indicador(codigos_paises, indicador["codigo"])
            except requests.RequestException:
                continue
            algum_ok = True
            for iso, dado in valores.items():
                if iso in por_pais:
                    por_pais[iso][chave] = dado
        if not algum_ok:
            raise requests.RequestException("Banco Mundial não respondeu")
        return por_pais

    try:
        # Os dados do Banco Mundial mudam pouco: guarda por 12 horas
        return _com_cache("bm", 12 * 3600, buscar), True
    except requests.RequestException:
        return {}, False


# ---------- Câmbio ----------

def cotacoes():
    """Quanto 1 real vale em cada moeda, ex.: {"EUR": 0.169, "USD": 0.192, ...}.

    Retorna (taxas, data da atualização) ou (None, None) se a API falhar.
    """
    def buscar():
        dados = _get_json(URL_CAMBIO)
        if dados.get("result") != "success":
            raise requests.RequestException("resposta inválida da API de câmbio")
        return dados["rates"], dados["time_last_update_unix"]

    try:
        return _com_cache("cambio", 3600, buscar)
    except requests.RequestException:
        return None, None


# ---------- Clima ----------

def clima_agora(latitude, longitude):
    """Temperatura, condição do tempo e hora local numa coordenada, ou None."""
    def buscar():
        dados = _get_json(URL_CLIMA, {
            "latitude": latitude, "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto", "forecast_days": 1,
        })
        return {
            "temperatura": dados["current"]["temperature_2m"],
            "codigo": dados["current"]["weather_code"],
            "hora_local": dados["current"]["time"].split("T")[1],
            "maxima": dados["daily"]["temperature_2m_max"][0],
            "minima": dados["daily"]["temperature_2m_min"][0],
        }

    try:
        return _com_cache(f"clima:{latitude},{longitude}", 600, buscar)
    except (requests.RequestException, KeyError):
        return None


def descrever_tempo(codigo):
    """Traduz o código de tempo da Open-Meteo (padrão WMO)."""
    if codigo == 0:
        return "céu limpo"
    if codigo <= 2:
        return "poucas nuvens"
    if codigo == 3:
        return "nublado"
    if codigo <= 48:
        return "neblina"
    if codigo <= 57:
        return "garoa"
    if codigo <= 67:
        return "chuva"
    if codigo <= 77:
        return "neve"
    if codigo <= 82:
        return "pancadas de chuva"
    return "trovoadas"


# ---------- Wikipedia ----------

def resumo_wikipedia(titulo):
    """Primeiro parágrafo do artigo e link para a página completa, ou None."""
    def buscar():
        dados = _get_json(URL_WIKIPEDIA + titulo)
        return {
            "texto": dados.get("extract", ""),
            "link": dados.get("content_urls", {}).get("desktop", {}).get("page"),
        }

    try:
        return _com_cache(f"wiki:{titulo}", 24 * 3600, buscar)
    except requests.RequestException:
        return None
