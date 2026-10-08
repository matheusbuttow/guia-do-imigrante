/* =========================================================================
 * dados.js — Base de dados local (curada) do Guia do Imigrante
 * -------------------------------------------------------------------------
 * Algumas informações NÃO estão disponíveis em APIs públicas gratuitas
 * (salário mínimo, índices de custo de vida/segurança/qualidade de vida,
 * rotas de visto). Por isso ficam aqui, com o ano de referência e a fonte.
 *
 * Todo o resto (PIB, expectativa de vida, homicídios, desemprego, inflação,
 * população, câmbio, clima, resumo do país) vem AO VIVO das APIs externas
 * — veja js/api.js.
 *
 * Fontes dos dados curados:
 *  - Salário mínimo: legislação oficial de cada país (valores de referência).
 *  - IDH: Relatório de Desenvolvimento Humano do PNUD (HDR 2025, dados 2023).
 *  - Custo de vida / Segurança / Qualidade de vida: índices aproximados do
 *    Numbeo (2025). Custo de vida usa Nova York = 100.
 * ========================================================================= */

/** Horas de trabalho por mês usadas para converter salário/hora em salário/mês
 *  (40 h/semana × 52 semanas ÷ 12 meses). */
const HORAS_POR_MES = 40 * 52 / 12; // ≈ 173,3 h

/** Brasil: usado como referência nas comparações ("quanto isso é no Brasil?"). */
const BRASIL = {
  iso3: 'BRA',
  iso2: 'br',
  nome: 'Brasil',
  moeda: { codigo: 'BRL', nome: 'Real brasileiro', simbolo: 'R$' },
  salarioMinimo: { valor: 1621, periodo: 'mes', pagamentosAno: 13, anoRef: 2026 },
  idh: 0.786,
  custoVida: 28,
  seguranca: 32,
  qualidadeVida: 105
};

/** Lista de países no "radar" de quem quer imigrar. */
const PAISES = [
  {
    iso3: 'PRT', iso2: 'pt', nome: 'Portugal', continente: 'Europa',
    capital: 'Lisboa', coords: [38.7223, -9.1393], wiki: 'Portugal',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Português'],
    salarioMinimo: { valor: 920, periodo: 'mes', pagamentosAno: 14, anoRef: 2026,
      obs: 'Pago em 14 parcelas por ano (inclui 13º e subsídio de férias).' },
    idh: 0.890, custoVida: 44, seguranca: 70, qualidadeVida: 165,
    vistos: ['Visto D7 (renda passiva)', 'Visto D8 (nômade digital)',
             'Visto para procura de trabalho', 'Acordo de mobilidade CPLP'],
    resumo: 'Mesmo idioma, clima ameno e grande comunidade brasileira.'
  },
  {
    iso3: 'ESP', iso2: 'es', nome: 'Espanha', continente: 'Europa',
    capital: 'Madri', coords: [40.4168, -3.7038], wiki: 'Espanha',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Espanhol', 'Catalão', 'Galego', 'Basco'],
    salarioMinimo: { valor: 1184, periodo: 'mes', pagamentosAno: 14, anoRef: 2025,
      obs: 'SMI pago em 14 parcelas por ano.' },
    idh: 0.918, custoVida: 48, seguranca: 64, qualidadeVida: 170,
    vistos: ['Visto de nômade digital', 'Arraigo (regularização por residência)',
             'Visto de estudante', 'Nacionalidade pela Lei da Memória Democrática'],
    resumo: 'Qualidade de vida alta, idioma próximo e custo moderado.'
  },
  {
    iso3: 'IRL', iso2: 'ie', nome: 'Irlanda', continente: 'Europa',
    capital: 'Dublin', coords: [53.3498, -6.2603], wiki: 'Irlanda',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Inglês', 'Irlandês'],
    salarioMinimo: { valor: 14.15, periodo: 'hora', anoRef: 2026 },
    idh: 0.949, custoVida: 70, seguranca: 56, qualidadeVida: 160,
    vistos: ['Critical Skills Employment Permit', 'General Employment Permit',
             'Stamp 2 (estudante, pode trabalhar 20h/semana)'],
    resumo: 'Polo de tecnologia na Europa; intercâmbio de inglês é porta de entrada.'
  },
  {
    iso3: 'DEU', iso2: 'de', nome: 'Alemanha', continente: 'Europa',
    capital: 'Berlim', coords: [52.52, 13.405], wiki: 'Alemanha',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Alemão'],
    salarioMinimo: { valor: 13.90, periodo: 'hora', anoRef: 2026 },
    idh: 0.959, custoVida: 63, seguranca: 61, qualidadeVida: 185,
    vistos: ['Blue Card UE', 'Chancenkarte (Cartão de Oportunidade)',
             'Visto para formação profissional (Ausbildung)'],
    resumo: 'Maior economia da Europa, alta demanda por profissionais qualificados.'
  },
  {
    iso3: 'NLD', iso2: 'nl', nome: 'Países Baixos', continente: 'Europa',
    capital: 'Amsterdã', coords: [52.3676, 4.9041], wiki: 'Países_Baixos',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Neerlandês'],
    salarioMinimo: { valor: 14.06, periodo: 'hora', anoRef: 2025 },
    idh: 0.955, custoVida: 66, seguranca: 71, qualidadeVida: 200,
    vistos: ['Highly Skilled Migrant', 'Orientation Year (recém-formados)',
             'Blue Card UE'],
    resumo: 'Inglês amplamente falado e uma das melhores qualidades de vida do mundo.'
  },
  {
    iso3: 'GBR', iso2: 'gb', nome: 'Reino Unido', continente: 'Europa',
    capital: 'Londres', coords: [51.5074, -0.1278], wiki: 'Reino_Unido',
    moeda: { codigo: 'GBP', nome: 'Libra esterlina', simbolo: '£' },
    idiomas: ['Inglês'],
    salarioMinimo: { valor: 12.71, periodo: 'hora', anoRef: 2026,
      obs: 'National Living Wage (21 anos ou mais).' },
    idh: 0.946, custoVida: 64, seguranca: 52, qualidadeVida: 168,
    vistos: ['Skilled Worker visa', 'Global Talent visa', 'Graduate visa'],
    resumo: 'Mercado financeiro e acadêmico forte; exige patrocínio do empregador.'
  },
  {
    iso3: 'ITA', iso2: 'it', nome: 'Itália', continente: 'Europa',
    capital: 'Roma', coords: [41.9028, 12.4964], wiki: 'Itália',
    moeda: { codigo: 'EUR', nome: 'Euro', simbolo: '€' },
    idiomas: ['Italiano'],
    salarioMinimo: { valor: null, periodo: 'mes', anoRef: 2025,
      obs: 'Não há salário mínimo nacional: os pisos são definidos por convenções coletivas de cada setor.' },
    idh: 0.915, custoVida: 55, seguranca: 55, qualidadeVida: 150,
    vistos: ['Cidadania por descendência (regras restringidas em 2025)',
             'Visto de trabalho (Decreto Flussi)', 'Visto de nômade digital'],
    resumo: 'Muitos brasileiros têm direito à cidadania; porta de entrada para a UE.'
  },
  {
    iso3: 'CAN', iso2: 'ca', nome: 'Canadá', continente: 'América do Norte',
    capital: 'Ottawa', coords: [45.4215, -75.6972], wiki: 'Canadá',
    moeda: { codigo: 'CAD', nome: 'Dólar canadense', simbolo: 'C$' },
    idiomas: ['Inglês', 'Francês'],
    salarioMinimo: { valor: 17.75, periodo: 'hora', anoRef: 2025,
      obs: 'Mínimo federal; cada província define o seu próprio valor.' },
    idh: 0.939, custoVida: 64, seguranca: 58, qualidadeVida: 170,
    vistos: ['Express Entry', 'Provincial Nominee Program (PNP)',
             'Study Permit + PGWP (permissão de trabalho pós-estudo)'],
    resumo: 'Imigração por pontos bem estruturada; incentiva residência permanente.'
  },
  {
    iso3: 'USA', iso2: 'us', nome: 'Estados Unidos', continente: 'América do Norte',
    capital: 'Washington, D.C.', coords: [38.9072, -77.0369], wiki: 'Estados_Unidos',
    moeda: { codigo: 'USD', nome: 'Dólar americano', simbolo: 'US$' },
    idiomas: ['Inglês'],
    salarioMinimo: { valor: 7.25, periodo: 'hora', anoRef: 2025,
      obs: 'Mínimo federal; muitos estados pagam bem mais (ex.: Califórnia, Washington).' },
    idh: 0.938, custoVida: 70, seguranca: 50, qualidadeVida: 178,
    vistos: ['H-1B (trabalho especializado)', 'EB-2 NIW (green card por mérito)',
             'F-1 (estudante)'],
    resumo: 'Maiores salários em tecnologia, mas processo de visto competitivo.'
  },
  {
    iso3: 'AUS', iso2: 'au', nome: 'Austrália', continente: 'Oceania',
    capital: 'Camberra', coords: [-35.2809, 149.13], wiki: 'Austrália',
    moeda: { codigo: 'AUD', nome: 'Dólar australiano', simbolo: 'A$' },
    idiomas: ['Inglês'],
    salarioMinimo: { valor: 24.95, periodo: 'hora', anoRef: 2025 },
    idh: 0.958, custoVida: 68, seguranca: 57, qualidadeVida: 190,
    vistos: ['Skilled Independent (subclasse 189)', 'Skills in Demand (patrocinado)',
             'Student visa (subclasse 500)'],
    resumo: 'Um dos maiores salários mínimos do mundo; estudantes podem trabalhar.'
  },
  {
    iso3: 'NZL', iso2: 'nz', nome: 'Nova Zelândia', continente: 'Oceania',
    capital: 'Wellington', coords: [-41.2865, 174.7762], wiki: 'Nova_Zelândia',
    moeda: { codigo: 'NZD', nome: 'Dólar neozelandês', simbolo: 'NZ$' },
    idiomas: ['Inglês', 'Maori'],
    salarioMinimo: { valor: 23.50, periodo: 'hora', anoRef: 2025 },
    idh: 0.938, custoVida: 63, seguranca: 58, qualidadeVida: 175,
    vistos: ['Skilled Migrant Category', 'Accredited Employer Work Visa',
             'Student visa'],
    resumo: 'Natureza, tranquilidade e equilíbrio entre vida pessoal e trabalho.'
  },
  {
    iso3: 'JPN', iso2: 'jp', nome: 'Japão', continente: 'Ásia',
    capital: 'Tóquio', coords: [35.6762, 139.6503], wiki: 'Japão',
    moeda: { codigo: 'JPY', nome: 'Iene', simbolo: '¥' },
    idiomas: ['Japonês'],
    salarioMinimo: { valor: 1121, periodo: 'hora', anoRef: 2025,
      obs: 'Média nacional ponderada; varia por província.' },
    idh: 0.925, custoVida: 43, seguranca: 77, qualidadeVida: 170,
    vistos: ['Visto de descendente (nikkei)', 'Engineer / Specialist in Humanities',
             'Specified Skilled Worker (SSW)'],
    resumo: 'Muito seguro e com custo surpreendentemente acessível; idioma é o desafio.'
  }
];

/** Indicadores buscados AO VIVO na API do Banco Mundial.
 *  `melhor` indica se um valor maior ('alto') ou menor ('baixo') é melhor —
 *  usado para destacar o vencedor no comparador. */
const INDICADORES_BM = {
  pib:        { codigo: 'NY.GDP.PCAP.CD',  nome: 'PIB per capita',           unidade: 'US$',  melhor: 'alto' },
  vida:       { codigo: 'SP.DYN.LE00.IN',  nome: 'Expectativa de vida',      unidade: 'anos', melhor: 'alto' },
  homicidios: { codigo: 'VC.IHR.PSRC.P5',  nome: 'Homicídios por 100 mil hab.', unidade: '',  melhor: 'baixo' },
  desemprego: { codigo: 'SL.UEM.TOTL.ZS',  nome: 'Desemprego',               unidade: '%',    melhor: 'baixo' },
  inflacao:   { codigo: 'FP.CPI.TOTL.ZG',  nome: 'Inflação anual',           unidade: '%',    melhor: 'baixo' },
  populacao:  { codigo: 'SP.POP.TOTL',     nome: 'População',                unidade: '',     melhor: null }
};
