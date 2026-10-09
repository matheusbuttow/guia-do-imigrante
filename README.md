# Guia do Imigrante

Site em Python (Flask) que ajuda brasileiros a comparar países para imigrar: salário mínimo
convertido para reais, custo de vida, segurança, qualidade de vida, IDH, moeda, clima,
indicadores socioeconômicos e mapa.

## Como funciona

O navegador pede uma página ao Flask. O Flask consulta as APIs externas (com a biblioteca
`requests`), faz as contas e devolve o HTML pronto, montado com os templates Jinja.
O mapa é gerado em Python com a biblioteca `folium`.

## APIs consumidas

| Serviço | Uso no site | Endpoint |
|---|---|---|
| **World Bank API** | PIB per capita, expectativa de vida, homicídios, desemprego, inflação, população | `api.worldbank.org/v2/country/{países}/indicator/{código}` |
| **ExchangeRate-API** | Cotação das moedas em R$ | `open.er-api.com/v6/latest/BRL` |
| **Open-Meteo** | Tempo agora na capital | `api.open-meteo.com/v1/forecast` |
| **Wikipedia REST API** | Resumo do país | `pt.wikipedia.org/api/rest_v1/page/summary/{título}` |
| **OpenStreetMap** | Mapa (via folium/Leaflet) | `tile.openstreetmap.org` |

Nenhuma exige chave. As respostas ficam em cache na memória (câmbio 1 h, Banco Mundial 12 h,
Wikipedia 24 h, clima 10 min).

## Estrutura

```
app.py            → rotas do Flask, cálculos e geração do mapa
apis.py           → requisições às APIs externas + cache
dados.py          → dados compilados à mão (salário mínimo, índices, vistos)
quiz.py           → perguntas e cálculo de compatibilidade do quiz
templates/        → páginas HTML (Jinja): base, index, pais, comparar, quiz, fontes, 404
static/style.css  → visual
requirements.txt  → bibliotecas necessárias
```

## Páginas

- `/` tabela dos países (ordenável, com filtro por continente e busca) e mapa
- `/pais/<código>` ficha do país: tempo agora, conversor de moeda, comparação com o Brasil,
  indicadores do Banco Mundial, vistos e resumo da Wikipedia (ex.: `/pais/PRT`)
- `/comparar?a=PRT&b=CAN` dois países lado a lado
- `/quiz` "Qual país combina com você?": 8 perguntas e os 5 países mais compatíveis, com os motivos
- `/fontes` de onde vem cada dado e se as APIs estão respondendo
- `/mapa?metrica=seguranca` o mapa sozinho (a página inicial o mostra num iframe)

## Rodar no computador

```bash
pip install -r requirements.txt
python app.py
```
Depois abra <http://localhost:5000>.

## Publicar na internet (sem usar git no computador)

**Render (recomendado)**
1. Crie uma conta em <https://github.com> e um repositório público novo.
2. No repositório, clique em *Add file → Upload files* e arraste `app.py`, `apis.py`, `dados.py`,
   `requirements.txt` e as pastas `templates` e `static`. Clique em *Commit changes*.
3. Crie uma conta em <https://render.com> entrando com o GitHub.
4. *New → Web Service*, escolha o repositório e preencha:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: Free
5. O site fica em `https://NOME.onrender.com`. No plano grátis ele "dorme" depois de 15 min
   sem acesso, e a primeira visita seguinte demora cerca de 1 minuto para carregar.

**PythonAnywhere (alternativa)**
1. Crie uma conta em <https://www.pythonanywhere.com>.
2. Na aba *Files*, envie os arquivos e as pastas.
3. Na aba *Consoles*, abra um Bash e rode `pip install --user folium`.
4. Na aba *Web*, crie um app *Flask* apontando para o `app.py`.
   Atenção: a conta grátis só acessa sites de uma lista liberada; se alguma API não carregar,
   use o Render.

## Alta disponibilidade (dois servidores)

O site pode rodar em dois servidores ao mesmo tempo, com um "porteiro" na frente que
passa a visita para o reserva quando o principal não responde.

```
visitante → Cloudflare Worker (failover/worker.js) → Render   (principal)
                                                   ↘ Vercel   (reserva)
```

1. **Principal:** publique no Render, como explicado acima.
2. **Reserva:** em <https://vercel.com>, entre com o GitHub, clique em *Add New → Project* e
   importe o mesmo repositório. O arquivo `vercel.json` já diz à Vercel como rodar o Flask.
3. **Porteiro:** em <https://dash.cloudflare.com>, vá em *Workers & Pages → Create → Worker*,
   cole o conteúdo de `failover/worker.js`, troque os dois endereços no começo do arquivo
   pelos seus e clique em *Deploy*. O endereço para divulgar é o do Worker
   (`https://NOME.SEU-USUARIO.workers.dev`).

Para conferir qual servidor respondeu, abra as ferramentas do navegador (F12 → Rede) e veja
o cabeçalho `X-Servidor` da resposta.

Outras proteções já incluídas no código:
- `/saude` responde sem consultar APIs externas; serve para monitores como o UptimeRobot.
- Se uma API externa cair, o site mostra o último valor que tinha guardado em vez de falhar.
