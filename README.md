
<div align="center">
  <img src="https://raw.githubusercontent.com/victorbispoo/tvScoreFrontFlutter/main/lib/assets/tvScoreLogin.png" alt="Logo do TV Score" width="180" />

  <h1>TV Score — Inteligência Artificial e Recomendações</h1>
  <p><strong>Sua próxima boa história começa aqui.</strong></p>
  <p>Recomendações personalizadas de filmes e séries com Python, análise de sentimentos e inteligência artificial.</p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Cloudflare_AI-F38020?style=flat-square&logo=cloudflare&logoColor=white" alt="Cloudflare AI" />
  <img src="https://img.shields.io/badge/Render-000000?style=flat-square&logo=render&logoColor=white" alt="Render" />
  <img src="https://img.shields.io/badge/TMDB-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white" alt="TMDB" />
</div>

---

## Sobre o projeto

O **TV Score** é uma plataforma de descoberta, avaliação e recomendação de filmes e séries, desenvolvida como Trabalho de Conclusão de Curso (TCC) do **SENAI — Desenvolvimento de Sistemas**.

Este repositório contém o componente de **Inteligência Artificial e Recomendações**, desenvolvido em Python com FastAPI. Sua responsabilidade é analisar as preferências dos usuários e gerar sugestões personalizadas de filmes e séries.

O sistema utiliza um algoritmo híbrido que combina avaliações, favoritos, gêneros escolhidos no cadastro, conteúdos preferidos, análise de sentimentos e similaridade semântica entre sinopses.

A solução integra o aplicativo Flutter, o backend Java/Spring Boot, a API do TMDB e modelos de inteligência artificial executados por meio da Cloudflare Workers AI.

Os serviços de recomendações e análise de sentimentos estão publicados separadamente no Render e integrados ao backend Java.

## Escopo do projeto

O componente Python tem como objetivo oferecer recomendações relevantes para cada usuário, considerando seus interesses individuais em vez de apresentar apenas conteúdos populares.

O escopo contempla a consulta de dados do usuário autenticado, a identificação de preferências, a análise de comentários, a busca de conteúdos no TMDB, a comparação semântica de sinopses e a classificação dos candidatos por relevância.

O recomendador trabalha separadamente com filmes e séries, utilizando o histórico de cada tipo de conteúdo para construir perfis de preferência.

A solução também considera as escolhas realizadas durante o cadastro, permitindo personalização mesmo quando o usuário ainda possui poucas avaliações.

## Funcionalidades

| Recurso | Descrição |
| --- | --- |
| Recomendações de filmes | Geração de até 10 sugestões personalizadas de filmes. |
| Recomendações de séries | Geração de até 10 sugestões personalizadas de séries. |
| Integração com Java | Consulta de avaliações, favoritos e preferências do usuário autenticado. |
| Onboarding | Utilização dos gêneros e conteúdos preferidos selecionados no cadastro. |
| Análise de sentimentos | Classificação de comentários como positivos, negativos ou neutros. |
| Similaridade semântica | Comparação do significado das sinopses por meio de embeddings de IA. |
| Pontuação de preferências | Identificação dos gêneros mais relevantes para o usuário. |
| Algoritmo híbrido | Combinação de afinidade por gênero, similaridade de gêneros, nota TMDB e similaridade semântica. |
| Exclusão de conteúdos conhecidos | Evita recomendar títulos já avaliados, favoritados ou selecionados como preferidos. |
| Explicação das recomendações | Retorna justificativas baseadas nos gêneros compatíveis. |
| Integração com TMDB | Consulta de filmes, séries, sinopses, gêneros, pôsteres e notas. |
| APIs REST | Disponibilização de endpoints documentados automaticamente pelo Swagger. |
| Hospedagem em nuvem | Serviços de recomendações e sentimentos publicados no Render. |

O sistema diferencia a **nota atribuída pelo usuário**, a **nota do TMDB** e o **score de recomendação**. O score representa a compatibilidade estimada de um conteúdo com o perfil do usuário, não sua qualidade absoluta.

## Tecnologias

| Tecnologia | Aplicação |
| --- | --- |
| Python | Desenvolvimento da lógica de recomendação e integração |
| FastAPI | Criação dos serviços REST |
| Uvicorn | Servidor ASGI |
| HTTPX | Comunicação HTTP com Java, TMDB e Cloudflare |
| Pydantic | Validação dos dados recebidos |
| Asyncio | Execução de operações assíncronas |
| Cloudflare Workers AI | Execução dos modelos de inteligência artificial |
| Qwen 3.8 27B | Classificação dos sentimentos dos comentários |
| Qwen3 Embedding 0.6B | Geração de embeddings para comparação de sinopses |
| TMDB API | Consulta de catálogo, gêneros, sinopses e avaliações |
| Python Dotenv | Carregamento de variáveis de ambiente |
| Render | Hospedagem dos microsserviços |
| Java e Spring Boot | Backend principal, autenticação e dados dos usuários |
| MySQL | Persistência de informações pelo backend Java |
| JWT | Autenticação das consultas integradas ao backend |

## Inteligência Artificial

O TV Score utiliza dois recursos principais de inteligência artificial: **análise de sentimentos** e **similaridade semântica**.

Os modelos são disponibilizados pela Cloudflare Workers AI e acessados por requisições HTTP.

Não é necessário carregar os modelos completos na memória do servidor Python. O processamento dos modelos ocorre na infraestrutura da Cloudflare.

### Análise de sentimentos

**Modelo:** `@cf/qwen/qwen3.8-27b`

A análise de sentimentos interpreta os comentários escritos pelos usuários sobre filmes e séries.

O modelo recebe o comentário e uma instrução para classificá-lo exclusivamente em uma das categorias:

- `POSITIVO`
- `NEGATIVO`
- `NEUTRO`

Exemplo:

```json
{
  "comentario": "Esse filme é incrível, adorei a história!"
}
```

Resposta:

```json
{
  "sentimento": "POSITIVO"
}
```

O resultado é utilizado para complementar a nota do usuário no cálculo das preferências.

O serviço não retorna uma porcentagem de confiança. Sua resposta contém a classificação identificada pela IA.

### Similaridade semântica

**Modelo:** `@cf/qwen/qwen3-embedding-0.6b`

A similaridade semântica permite comparar o significado das sinopses de diferentes filmes e séries.

O modelo transforma os textos em vetores numéricos chamados **embeddings**, que representam características semânticas dos conteúdos.

O algoritmo utiliza a similaridade do cosseno para comparar esses vetores e identificar conteúdos com descrições semelhantes.

Por exemplo, um usuário que demonstra interesse por histórias de exploração espacial pode receber recomendações de outros conteúdos com temas relacionados, mesmo quando seus títulos são diferentes.

As referências utilizadas na comparação incluem sinopses de conteúdos:

- Avaliados com nota igual ou superior a 7;
- Adicionados aos favoritos;
- Selecionados como preferidos durante o cadastro.

A similaridade semântica complementa a classificação por gêneros e contribui para melhorar a personalização das sugestões.

## Como funciona o recomendador

O TV Score utiliza um algoritmo híbrido dividido em etapas.

### 1. Coleta de informações do usuário

O Python consulta o backend Java para obter:

- Avaliações realizadas pelo usuário;
- Filmes e séries adicionados aos favoritos;
- Gêneros selecionados no cadastro;
- Filmes e séries escolhidos como preferidos.

As consultas utilizam o token JWT do usuário autenticado.

Os dados são organizados separadamente para filmes (`MOVIE`) e séries (`TV`).

### 2. Identificação das preferências

O sistema calcula uma pontuação para os gêneros associados às avaliações do usuário.

A fórmula inicial é:

```python
pontos = nota - 5
```

Essa estratégia utiliza a nota 5 como referência.

| Nota | Pontuação inicial |
| --- | --- |
| 10 | +5 |
| 8 | +3 |
| 5 | 0 |
| 3 | -2 |
| 0 | -5 |

Dessa forma, avaliações altas aumentam a preferência pelos gêneros, enquanto avaliações baixas podem reduzi-la.

Quando existe um comentário, a IA de sentimentos realiza um ajuste adicional:

| Sentimento | Ajuste |
| --- | --- |
| Positivo | +1,5 |
| Neutro | 0 |
| Negativo | -1,5 |

A fórmula completa é:

```python
pontos = nota - 5 + ajuste_sentimento
```

Exemplo de uma avaliação com nota 9 e comentário positivo:

```text
Nota: 9
Pontuação inicial: 9 - 5 = 4
Sentimento: POSITIVO
Ajuste: +1,5

Pontuação final: 5,5
```

Os pontos são adicionados aos gêneros do conteúdo avaliado.

Se não existir comentário, a pontuação é calculada somente com a nota.

Se o serviço de sentimentos estiver indisponível, o recomendador mantém o cálculo baseado na nota.

### 3. Favoritos e preferências do cadastro

Além das avaliações, o sistema considera outras interações.

| Interação | Pontuação |
| --- | --- |
| Conteúdo adicionado aos favoritos | +3 por gênero |
| Gênero escolhido no cadastro | +2 |
| Conteúdo escolhido como preferido | +1 por gênero |

Esses sinais são acumulados para identificar os gêneros com maior afinidade.

O onboarding também permite oferecer recomendações personalizadas para usuários que ainda não possuem um histórico significativo de avaliações.

Os gêneros escolhidos são convertidos para os identificadores correspondentes do TMDB, considerando as categorias de filmes e séries.

### 4. Busca de conteúdos no TMDB

Após calcular as preferências, o sistema identifica até três gêneros com pontuação positiva para orientar a busca.

A consulta ao TMDB reúne candidatos provenientes de:

- Gêneros preferidos;
- Conteúdos populares;
- Conteúdos com boas avaliações.

O recomendador reúne até 40 candidatos para a etapa de classificação.

Quando não existem preferências positivas, são utilizados gêneros padrão para iniciar a recomendação.

Antes de calcular o resultado final, o sistema exclui os títulos que o usuário já avaliou, favoritou ou selecionou como preferidos.

### 5. Cálculo do score de recomendação

O algoritmo principal combina três critérios:

| Critério | Peso |
| --- | --- |
| Afinidade com os gêneros preferidos | 60% |
| Similaridade entre conjuntos de gêneros | 25% |
| Nota do TMDB | 15% |

A pontuação é calculada em uma escala de 0 a 100.

```text
Score base =
(Afinidade × 60)
+ (Similaridade de gêneros × 25)
+ ((Nota TMDB / 10) × 15)
```

A afinidade considera os pontos acumulados nos gêneros.

A similaridade de gêneros mede a correspondência entre os gêneros do candidato e os gêneros preferidos do usuário.

A nota TMDB contribui como indicador adicional de avaliação do conteúdo.

### 6. Aplicação da similaridade semântica

Quando existem sinopses de referência, o sistema utiliza os embeddings da Cloudflare para comparar os conteúdos candidatos.

A pontuação é reajustada pela fórmula:

```text
Score final =
(Score base × 0,80)
+ (Similaridade semântica × 100 × 0,20)
```

| Componente | Peso |
| --- | --- |
| Algoritmo de recomendação | 80% |
| Similaridade semântica | 20% |

Essa etapa considera tanto as preferências por gêneros quanto a proximidade temática entre as sinopses.

Caso não existam sinopses de referência ou a análise semântica esteja indisponível, o resultado permanece baseado no algoritmo principal.

### 7. Resultado das recomendações

Após o cálculo, os candidatos são ordenados pela pontuação final.

O serviço retorna até **10 recomendações personalizadas**, incluindo:

- Identificador TMDB;
- Título;
- Sinopse;
- Nota TMDB;
- Gêneros;
- Pôster;
- Score de recomendação;
- Justificativa da recomendação;
- Similaridade da sinopse, quando calculada.

O resultado é disponibilizado em JSON para integração com o restante do TV Score.

## Integração da solução

A arquitetura do TV Score é composta por três componentes principais:

- **Aplicativo Flutter:** interface de descoberta, avaliações, favoritos, perfil e recomendações.
- **Backend Java:** autenticação, gerenciamento de usuários, persistência das informações e integração com o aplicativo.
- **Microsserviços Python:** processamento de preferências, análise de sentimentos e geração de recomendações personalizadas.

### Fluxo de integração

```text
             APLICATIVO FLUTTER
                     |
                     v
             BACKEND JAVA
              Spring Boot
                     |
            Autenticação JWT
                     |
                     v
          API DE RECOMENDAÇÕES
             Python/FastAPI
                     |
          +----------+-----------+
          |          |           |
          v          v           v
     Dados Java     TMDB      Cloudflare AI
          |          |           |
          |          |     +-----+------+
          |          |     |            |
          |          |     v            v
          |          |  Sentimentos  Embeddings
          |          |     |            |
          +----------+-----+------------+
                     |
                     v
          ALGORITMO HÍBRIDO
                     |
                     v
          SCORE DE RECOMENDAÇÃO
                     |
                     v
          TOP 10 FILMES OU SÉRIES
                     |
                     v
               BACKEND JAVA
                     |
                     v
             APLICATIVO FLUTTER
```

O Python consulta as informações do usuário no backend Java e utiliza os dados do TMDB para complementar as avaliações com gêneros e sinopses.

O serviço de sentimentos é consultado pelo recomendador quando existem comentários associados às avaliações.

As duas aplicações Python são executadas separadamente no Render.

## Serviços publicados

| Serviço | Endereço |
| --- | --- |
| Recomendações | [tvscore-recomendacoes.onrender.com](https://tvscore-recomendacoes.onrender.com) |
| Swagger de recomendações | [Documentação interativa](https://tvscore-recomendacoes.onrender.com/docs) |
| Análise de sentimentos | [tvscore-sentimentos.onrender.com](https://tvscore-sentimentos.onrender.com) |
| Swagger de sentimentos | [Documentação interativa](https://tvscore-sentimentos.onrender.com/docs) |
| Backend Java | [tvscore-backend.onrender.com](https://tvscore-backend.onrender.com) |
| Swagger Java | [Documentação interativa](https://tvscore-backend.onrender.com/swagger-ui/index.html) |

Os serviços foram implantados e tiveram seus principais fluxos de integração validados por meio de requisições realizadas no Swagger.

## Como executar

### Pré-requisitos

- Python 3.10 ou superior, recomendado;
- Git instalado;
- Conexão com a internet;
- Chave de acesso à API do TMDB;
- Conta e credenciais da Cloudflare Workers AI;
- Backend Java acessível para as rotas integradas.

### Instalação

Clone o repositório:

```bash
git clone https://github.com/Kaique-Ramiro/recomendador-TvScore.git
cd recomendador-TvScore
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências dos serviços atuais:

```bash
pip install -r requirements_recomendacoes.txt
```

Os arquivos `requirements_recomendacoes.txt` e `requirements_sentimentos.txt` contêm as dependências leves utilizadas pelos serviços publicados.

O arquivo `requirements.txt` também permanece no repositório e contém dependências de uma implementação anterior baseada em modelos locais.

A versão atual utiliza modelos hospedados na Cloudflare, sem necessidade de carregar Transformers, PyTorch ou Sentence Transformers para executar os serviços principais.

### Configuração das variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
TMDB_API_KEY=SUA_CHAVE_TMDB

JAVA_API_URL=http://localhost:8080

CLOUDFLARE_ACCOUNT_ID=SEU_ACCOUNT_ID
CLOUDFLARE_API_TOKEN=SEU_TOKEN_CLOUDFLARE

SENTIMENTOS_API_URL=http://127.0.0.1:8001
```

| Variável | Finalidade |
| --- | --- |
| `TMDB_API_KEY` | Autenticação nas consultas ao TMDB |
| `JAVA_API_URL` | Endereço do backend Java |
| `CLOUDFLARE_ACCOUNT_ID` | Identificação da conta Cloudflare |
| `CLOUDFLARE_API_TOKEN` | Autenticação para executar os modelos de IA |
| `SENTIMENTOS_API_URL` | Endereço-base do serviço de sentimentos |

Em produção, os endereços dos serviços podem ser configurados como:

```env
JAVA_API_URL=https://tvscore-backend.onrender.com
SENTIMENTOS_API_URL=https://tvscore-sentimentos.onrender.com
```

As credenciais da Cloudflare e a chave do TMDB devem ser configuradas nas variáveis de ambiente dos serviços que utilizam essas integrações.

**Importante:** não publique arquivos `.env`, tokens JWT, chaves de API ou outras credenciais no GitHub.

### Executar o serviço de recomendações

```bash
uvicorn main_recomendacoes:app --reload --port 8000
```

Documentação:

```text
http://127.0.0.1:8000/docs
```

### Executar o serviço de sentimentos

Em outro terminal:

```bash
uvicorn main_sentimentos:app --reload --port 8001
```

Documentação:

```text
http://127.0.0.1:8001/docs
```

### Executar os serviços em uma única aplicação

O repositório também permite iniciar os dois grupos de rotas na mesma aplicação:

```bash
uvicorn main:app --reload --port 8000
```

Nesse modo, configure `SENTIMENTOS_API_URL` com o endereço-base da própria aplicação, caso o recomendador precise consultar o serviço de sentimentos localmente.

## Endpoints da API

### Recomendações

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | `/` | Verifica o funcionamento do serviço |
| GET | `/recomendacoes` | Consulta filmes pelos gêneros informados |
| GET | `/recomendacoes/personalizadas` | Gera recomendações com dados simulados |
| POST | `/recomendacoes/usuario` | Recomenda filmes com avaliações e favoritos enviados |
| POST | `/recomendacoes/series` | Recomenda séries com dados enviados |
| GET | `/recomendacoes/teste-java` | Consulta os dados do usuário no backend Java |
| GET | `/recomendacoes/teste-preparacao` | Exibe os dados preparados para o algoritmo |
| GET | `/recomendacoes/filmes/java` | Gera recomendações de filmes com dados reais do Java |
| GET | `/recomendacoes/series/java` | Gera recomendações de séries com dados reais do Java |

As rotas integradas ao Java utilizam autenticação **Bearer JWT**.

### Análise de sentimentos

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | `/` | Verifica o funcionamento do serviço |
| POST | `/sentimentos/analisar` | Classifica o sentimento de um comentário |

## Exemplos de requisições

### Recomendações por gênero

```http
GET /recomendacoes?generos=28&generos=878&quantidade=10
```

Nesse exemplo:

- `28` representa ação;
- `878` representa ficção científica;
- `quantidade=10` solicita até dez resultados.

O parâmetro `quantidade` aceita valores de 1 a 20.

### Recomendações com dados enviados

```http
POST /recomendacoes/usuario
Content-Type: application/json
```

Corpo da requisição:

```json
{
  "avaliacoes": [
    {
      "id": 27205,
      "nota": 9,
      "generos": [28, 878, 12],
      "comentario": "Gostei muito da história e dos personagens!"
    }
  ],
  "favoritos": [
    {
      "id": 603,
      "generos": [28, 878]
    }
  ]
}
```

O sistema utiliza as avaliações e os favoritos informados para calcular as preferências e gerar recomendações.

### Análise de sentimentos

```http
POST /sentimentos/analisar
Content-Type: application/json
```

Corpo da requisição:

```json
{
  "comentario": "Esse filme é maravilhoso!"
}
```

Exemplo de resposta:

```json
{
  "sentimento": "POSITIVO"
}
```

### Recomendações integradas ao Java

```http
GET /recomendacoes/filmes/java
Authorization: Bearer SEU_TOKEN_JWT
```

O token é encaminhado ao backend Java para consultar as informações do usuário autenticado.

O Python organiza os dados, calcula as preferências, aplica os recursos de IA e retorna as recomendações personalizadas.

## Integração com o backend Java

A integração utiliza quatro endpoints principais:

| Endpoint Java | Informação |
| --- | --- |
| `/api/avaliacoes/minhas` | Avaliações e comentários do usuário |
| `/api/favoritos` | Conteúdos adicionados aos favoritos |
| `/api/usuarios/eu/generos` | Gêneros escolhidos no cadastro |
| `/api/usuarios/eu/conteudos-preferidos` | Filmes e séries escolhidos como preferidos |

As requisições são realizadas de forma assíncrona utilizando HTTPX e Asyncio.

O Python encaminha o token JWT recebido ao Java e processa os dados retornados.

### Tratamento dos comentários

Os comentários são obtidos pelo campo `comentario` das avaliações retornadas pelo backend Java.

O fluxo é:

```text
Usuário avalia um conteúdo
          |
          v
Java armazena nota e comentário
          |
          v
Python consulta /api/avaliacoes/minhas
          |
          v
Python identifica o comentário
          |
          v
Serviço de sentimentos / Cloudflare
          |
          v
Classificação: POSITIVO, NEGATIVO ou NEUTRO
          |
          v
Ajuste na pontuação dos gêneros
          |
          v
Recomendações personalizadas
```

A análise de sentimentos é aplicada quando existem comentários associados às avaliações.

Comentários vazios ou ausentes não impedem a geração de recomendações.

## Organização do código

```text
recomendador-TvScore/
│
├── main.py
├── main_recomendacoes.py
├── main_sentimentos.py
├── config.py
├── recomendador.py
│
├── requirements.txt
├── requirements_recomendacoes.txt
├── requirements_sentimentos.txt
├── teste_render.py
├── .gitignore
├── README.md
│
├── models/
│   ├── __init__.py
│   └── schemas.py
│
├── routes/
│   ├── __init__.py
│   ├── recomendacoes.py
│   └── sentimentos.py
│
└── services/
    ├── __init__.py
    ├── integracao_java_service.py
    ├── onboarding_service.py
    ├── preparacao_dados_service.py
    ├── recomendacao_service.py
    ├── recomendacao_series_service.py
    ├── sentimento_service.py
    ├── similaridade_service.py
    └── tmdb_service.py
```

### Responsabilidades dos arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Inicializa a aplicação com recomendações e sentimentos |
| `main_recomendacoes.py` | Inicializa o serviço exclusivo de recomendações |
| `main_sentimentos.py` | Inicializa o serviço exclusivo de sentimentos |
| `config.py` | Carrega a configuração da API TMDB |
| `recomendador.py` | Calcula preferências e scores por gênero |
| `routes/recomendacoes.py` | Define os endpoints de recomendações |
| `routes/sentimentos.py` | Define o endpoint de análise de sentimentos |
| `models/schemas.py` | Valida avaliações e favoritos recebidos |
| `services/integracao_java_service.py` | Consulta os endpoints do backend Java |
| `services/onboarding_service.py` | Processa preferências escolhidas no cadastro |
| `services/preparacao_dados_service.py` | Organiza avaliações, favoritos e onboarding |
| `services/recomendacao_service.py` | Gera recomendações personalizadas de filmes |
| `services/recomendacao_series_service.py` | Gera recomendações personalizadas de séries |
| `services/sentimento_service.py` | Consulta o modelo de sentimentos da Cloudflare |
| `services/similaridade_service.py` | Gera embeddings com a Cloudflare |
| `services/tmdb_service.py` | Consulta filmes, séries, gêneros e sinopses no TMDB |
| `teste_render.py` | Contém rotas auxiliares utilizadas durante o desenvolvimento |

## Qualidade e testes

Durante o desenvolvimento, os serviços foram testados manualmente utilizando a documentação Swagger do FastAPI e do backend Java.

### Testes de recomendações

Foram validados os seguintes fluxos:

- Comunicação entre o Python e o backend Java;
- Consulta de avaliações, favoritos e preferências;
- Preparação dos dados recebidos;
- Processamento das escolhas do onboarding;
- Geração de recomendações personalizadas de filmes;
- Geração de recomendações personalizadas de séries;
- Utilização de embeddings para similaridade semântica;
- Retorno de listas com dez recomendações.

### Testes de sentimentos

Foram realizadas requisições com comentários positivos e negativos, verificando as classificações retornadas pelo serviço publicado.

A API aceita comentários de até 3.000 caracteres e exige que o campo não esteja vazio.

### Testes de integração em produção

Os principais endpoints foram executados após a publicação dos serviços no Render.

Os testes confirmaram a comunicação entre:

- Python e backend Java;
- Python e TMDB;
- Python e Cloudflare Workers AI;
- Serviço de recomendações e serviço de sentimentos.

Essas verificações validam os fluxos principais testados, mas não substituem uma suíte completa de testes automatizados, testes de carga ou validação integral do aplicativo.

### Verificação de sintaxe

Para verificar os arquivos Python:

```bash
python -m compileall .
```

O projeto também permite testes manuais diretamente pelo Swagger, sem necessidade de ferramentas adicionais.

## Implantação no Render

O projeto utiliza dois serviços web independentes, ambos originados do mesmo repositório GitHub.

### Serviço de recomendações

**Arquivo de entrada:** `main_recomendacoes.py`

Comando de instalação:

```bash
pip install -r requirements_recomendacoes.txt
```

Comando de inicialização:

```bash
uvicorn main_recomendacoes:app --host 0.0.0.0 --port $PORT
```

Endereço:

```text
https://tvscore-recomendacoes.onrender.com
```

### Serviço de sentimentos

**Arquivo de entrada:** `main_sentimentos.py`

Comando de instalação:

```bash
pip install -r requirements_sentimentos.txt
```

Comando de inicialização:

```bash
uvicorn main_sentimentos:app --host 0.0.0.0 --port $PORT
```

Endereço:

```text
https://tvscore-sentimentos.onrender.com
```

As credenciais e os endereços dos serviços externos devem ser configurados nas variáveis de ambiente do Render.

A separação dos serviços permite executar recomendações e análise de sentimentos de maneira independente, mantendo a comunicação entre eles por API REST.

## Tratamento de erros e limitações

O sistema inclui tratamentos para situações como:

- Falhas de comunicação com o backend Java;
- Token inválido ou sem autorização;
- Erros em consultas ao TMDB;
- Ausência de comentários;
- Indisponibilidade do serviço de sentimentos;
- Falhas na geração de embeddings;
- Ausência de preferências suficientes;
- Conteúdos sem sinopse disponível.

Quando não existem preferências positivas, o recomendador utiliza gêneros padrão para buscar candidatos.

Se a análise de sentimentos falhar, o cálculo das preferências continua utilizando as notas e os favoritos.

Se a similaridade semântica estiver indisponível, as recomendações continuam utilizando a pontuação do algoritmo principal.

A disponibilidade das recomendações ainda depende do acesso ao backend Java e ao TMDB nas rotas integradas.

## Desafios técnicos

O desenvolvimento envolveu desafios relacionados à integração entre tecnologias e ao uso de inteligência artificial.

Entre os principais desafios estão:

- Comunicação entre Python e Java utilizando APIs REST;
- Autenticação de usuários por JWT;
- Padronização de dados de filmes e séries;
- Integração de preferências escolhidas no cadastro;
- Processamento de comentários em linguagem natural;
- Implementação de um algoritmo híbrido de recomendação;
- Geração e comparação de embeddings semânticos;
- Integração com modelos de IA hospedados na Cloudflare;
- Separação dos serviços de recomendações e sentimentos;
- Implantação e testes dos serviços no Render.

A utilização da Cloudflare Workers AI permitiu executar os modelos remotamente, reduzindo a necessidade de memória e processamento nos servidores Python.

## Objetivo acadêmico

O projeto demonstra a aplicação prática de conhecimentos adquiridos durante o curso Técnico em Desenvolvimento de Sistemas do SENAI.

Entre os conceitos utilizados estão:

- Desenvolvimento de APIs REST;
- Programação em Python;
- Arquitetura de microsserviços;
- Integração entre sistemas;
- Autenticação JWT;
- Consumo de APIs externas;
- Processamento e preparação de dados;
- Inteligência artificial aplicada;
- Processamento de linguagem natural;
- Sistemas de recomendação;
- Similaridade semântica;
- Implantação de aplicações em nuvem.

O componente de inteligência artificial foi desenvolvido para complementar as funcionalidades do TV Score, oferecendo uma experiência personalizada de descoberta de filmes e séries.

## Repositórios relacionados

- [Aplicativo Flutter](https://github.com/victorbispoo/tvScoreFrontFlutter)
- [Backend Java](https://github.com/GuedesSiilva/BackEnd_Projeto_TvScore)
- [Inteligência Artificial e Recomendações Python](https://github.com/Kaique-Ramiro/recomendador-TvScore)

## Referências

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [HTTPX](https://www.python-httpx.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- [TMDB API](https://developer.themoviedb.org/)
- [Render](https://render.com/)
- [Spring Boot](https://spring.io/projects/spring-boot)

## Créditos

Os dados de filmes, séries, sinopses, gêneros, notas e imagens utilizados pelo recomendador são fornecidos pelo [TMDB](https://www.themoviedb.org/).

Este produto utiliza a API do TMDB, mas não é endossado nem certificado pelo TMDB.

Os modelos de inteligência artificial são executados por meio da **Cloudflare Workers AI**.

O TV Score foi desenvolvido como Trabalho de Conclusão de Curso do **SENAI — Desenvolvimento de Sistemas**, integrando aplicativo Flutter, backend Java e microsserviços Python.

---

<p align="center"><strong>TV Score · Descubra, avalie e encontre sua próxima história favorita.</strong></p>
<p align="center">Inteligência Artificial aplicada à recomendação personalizada de filmes e séries.</p>
