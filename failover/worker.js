// Porteiro do Guia do Imigrante (Cloudflare Worker).
//
// Toda visita chega primeiro aqui. O Worker tenta o primeiro servidor da lista;
// se ele demorar demais, der erro 5xx ou estiver fora do ar, tenta o seguinte.
// Assim o site continua respondendo mesmo com um dos servidores caído.
//
// Troque os endereços abaixo pelos dos seus dois deploys.
const SERVIDORES = [
  "https://guia-do-imigrante.onrender.com", // principal
  "https://guia-do-imigrante.vercel.app",   // reserva
];

// Tempo máximo de espera por servidor. O Render grátis "dorme" e pode levar
// quase 1 minuto para acordar; com este limite a visita vai para o reserva
// em vez de ficar esperando.
const TEMPO_LIMITE_MS = 8000;

// O último servidor da lista ganha um prazo maior: depois dele não há para quem
// passar, então vale mais esperar uma página lenta do que mostrar erro.
const TEMPO_LIMITE_ULTIMO_MS = 30000;

export async function atender(request, servidores = SERVIDORES, tempoLimite = TEMPO_LIMITE_MS) {
  const url = new URL(request.url);

  for (const [posicao, servidor] of servidores.entries()) {
    const ultimo = posicao === servidores.length - 1;
    try {
      const resposta = await fetch(servidor + url.pathname + url.search, {
        method: request.method,
        headers: { "Accept": request.headers.get("Accept") || "*/*" },
        signal: AbortSignal.timeout(ultimo ? TEMPO_LIMITE_ULTIMO_MS : tempoLimite),
      });

      // 5xx = o servidor está com problema: passa para o próximo.
      // 404 e outros 4xx são respostas válidas do site (ex.: país inexistente).
      if (resposta.status < 500) {
        const copia = new Response(resposta.body, resposta);
        copia.headers.set("X-Servidor", servidor); // mostra quem respondeu
        return copia;
      }
    } catch (erro) {
      // Fora do ar ou estourou o tempo: tenta o próximo da lista
    }
  }

  return new Response("O Guia do Imigrante está temporariamente fora do ar. Tente de novo em instantes.", {
    status: 503,
    headers: { "Content-Type": "text/plain; charset=utf-8", "Retry-After": "30" },
  });
}

export default { fetch: (request) => atender(request) };
