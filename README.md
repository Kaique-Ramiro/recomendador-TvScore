# 🎬 TVScore — Microsserviço de Recomendação com Inteligência Artificial

Microsserviço desenvolvido em **Python e FastAPI** para o projeto **TVScore**, uma plataforma de descoberta, avaliação e recomendação de filmes e séries.

O objetivo deste serviço é gerar recomendações personalizadas a partir das preferências dos usuários, utilizando um algoritmo híbrido que combina avaliações, gêneros cinematográficos, favoritos, análise de sentimentos e similaridade semântica.

Este projeto foi desenvolvido como parte do **Trabalho de Conclusão de Curso (TCC) do SENAI — Desenvolvimento de Sistemas**.

## 1. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| FastAPI | Construção da API REST |
| Uvicorn | Servidor ASGI |
| HTTPX | Requisições HTTP assíncronas |
| Pydantic | Validação dos dados |
| Transformers | Processamento de linguagem natural |
| PyTorch | Execução dos modelos de IA |
| Sentence Transformers | Similaridade semântica |
| Python Dotenv | Configuração de variáveis de ambiente |
| TMDB API | Consulta de filmes, séries e gêneros |

## 2. Modelos de Inteligência Artificial

O microsserviço utiliza dois modelos principais.

### Análise de sentimentos — XLM-RoBERTa

**Modelo:** `cardiffnlp/twitter-xlm-roberta-base-sentiment`

Responsável por interpretar o sentimento presente nos comentários dos usuários.

Classificações possíveis:

- POSITIVO
- NEUTRO
- NEGATIVO

O modelo também retorna um nível de confiança na classificação.

Essa informação é utilizada para ajustar a pontuação de preferência por gênero.

### Similaridade semântica — MiniLM

**Modelo:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

Responsável por transformar sinopses em representações numéricas (*embeddings*) e comparar sua similaridade semântica.

Isso permite identificar filmes e séries com conteúdos semelhantes aos que o usuário já avaliou positivamente ou adicionou aos favoritos.

## 3. Como funciona o recomendador

O sistema utiliza um algoritmo de recomendação híbrido.

### Etapa 1 — Identificação das preferências

As preferências são calculadas a partir de:

- Notas atribuídas aos conteúdos.
- Gêneros dos filmes e séries avaliados.
- Sentimentos identificados nos comentários.
- Conteúdos adicionados aos favoritos.

A pontuação inicial de cada avaliação é:

`pontos = nota - 5`

Quando existe um comentário, o sistema aplica um ajuste proporcional à confiança do modelo de sentimentos:

| Sentimento | Ajuste |
|---|---|
| Positivo | +1,5 × confiança |
| Neutro | 0 |
| Negativo | −1,5 × confiança |

Cada gênero de um conteúdo favorito recebe **+3 pontos**.

### Etapa 2 — Busca de candidatos

O microsserviço identifica os gêneros com maior pontuação e consulta a API do TMDB para obter filmes ou séries compatíveis.

A busca combina preferências por gênero com critérios de popularidade e avaliação.

O sistema também exclui das recomendações os conteúdos que o usuário já avaliou ou favoritou.

### Etapa 3 — Cálculo da pontuação

O algoritmo principal combina três critérios:

| Critério | Peso |
|---|---|
| Afinidade com os gêneros preferidos | 60% |
| Similaridade entre conjuntos de gêneros | 25% |
| Nota do TMDB | 15% |

A pontuação é calculada em uma escala de 0 a 100.

### Etapa 4 — Similaridade de sinopses

Quando existem sinopses de conteúdos preferidos disponíveis, o sistema também utiliza o MiniLM para comparar o significado das descrições.

Nesse caso, a pontuação é reajustada:

`score_final = (score_anterior × 0,8) + (similaridade_semantica × 100 × 0,2)`

Essa etapa combina **80% do resultado do algoritmo anterior e 20% da similaridade semântica**.

### Etapa 5 — Resultado

O serviço ordena os candidatos pela pontuação e retorna até **10 recomendações personalizadas**, incluindo informações dos conteúdos e justificativas quando disponíveis.

## 4. Arquitetura do microsserviço

O microsserviço se comunica com o backend Java/Spring Boot e com a API do TMDB.

```text
Aplicativo TVScore (Flutter)
          |
          v
Backend Java + Spring Boot
          |
          | JWT / HTTP
          v
Microsserviço Python + FastAPI
          |
          +--> Dados de avaliações e favoritos
          |
          +--> TMDB API
          |     Filmes, séries e gêneros
          |
          +--> XLM-RoBERTa
          |     Análise de sentimentos
          |
          +--> MiniLM
                Similaridade semântica
          |
          v
  Recomendações personalizadas
```

O backend Java é responsável pelo gerenciamento dos usuários, autenticação e dados de avaliações e favoritos.

O microsserviço Python é responsável pelo processamento das preferências e pela geração das recomendações.

**Observação:** o código contém rotas para integração com o backend Java, mas a implantação e a integração final do sistema completo ainda precisam ser validadas.

## 5. Estrutura do projeto

```text
recomendador-TvScore/
│
├── main.py
├── config.py
├── recomendador.py
├── requirements.txt
│
├── routes/
│   ├── recomendacoes.py
│   └── sentimentos.py
│
├── models/
│   └── schemas.py
│
└── services/
    ├── tmdb_service.py
    ├── integracao_java_service.py
    ├── preparacao_dados_service.py
    ├── recomendacao_service.py
    ├── recomendacao_series_service.py
    ├── sentimento_service.py
    └── similaridade_service.py
```

## 6. Instalação e configuração

### Pré-requisitos

- Python instalado.
- Git instalado.
- Chave válida da API do TMDB.
- Acesso à internet para consultar o TMDB e baixar os modelos de IA.
- Backend Java acessível, caso sejam utilizadas as rotas integradas.

### Clonar o repositório

```bash
git clone https://github.com/Kaique-Ramiro/recomendador-TvScore.git
cd recomendador-TvScore
```

### Criar um ambiente virtual

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

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
TMDB_API_KEY=SUA_CHAVE_TMDB
JAVA_API_URL=http://localhost:8080
```

A variável `TMDB_API_KEY` permite consultar o catálogo de filmes e séries.

A variável `JAVA_API_URL` define o endereço do backend Java. Caso não seja configurada, o código utiliza `http://localhost:8080` como padrão.

**Importante:** não publique o arquivo `.env`, as chaves de API ou tokens JWT no GitHub.

## 7. Executando o microsserviço

Na raiz do projeto, execute:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

`http://127.0.0.1:8000`

A documentação interativa do Swagger estará disponível em:

`http://127.0.0.1:8000/docs`

Ao acessar a rota principal `/`, a resposta esperada é:

```json
{
  "mensagem": "TVScore funcionando!"
}
```

Na primeira utilização das funcionalidades de IA, pode ser necessário aguardar o carregamento e download dos modelos.

## 8. Endpoints da API

### Recomendações

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/recomendacoes` | Recomenda filmes por gêneros informados |
| GET | `/recomendacoes/personalizadas` | Teste de recomendações com dados simulados |
| POST | `/recomendacoes/usuario` | Recomenda filmes com dados enviados no corpo |
| POST | `/recomendacoes/series` | Recomenda séries com dados enviados no corpo |
| GET | `/recomendacoes/teste-java` | Consulta avaliações e favoritos no backend Java |
| GET | `/recomendacoes/teste-preparacao` | Testa a preparação dos dados recebidos |
| GET | `/recomendacoes/filmes/java` | Recomenda filmes usando dados do backend Java |
| GET | `/recomendacoes/series/java` | Recomenda séries usando dados do backend Java |

As rotas de integração com Java utilizam autenticação **Bearer JWT**.

### Análise de sentimentos

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/sentimentos/analisar` | Classifica o sentimento de um comentário |

## 9. Exemplos de requisições

### Recomendações por gênero

```http
GET /recomendacoes?generos=28&generos=878&quantidade=10
```

Nesse exemplo:

- `28` representa ação.
- `878` representa ficção científica.
- `quantidade=10` solicita até 10 resultados.

A quantidade aceita valores entre 1 e 20.

### Recomendações personalizadas por dados enviados

```http
POST /recomendacoes/usuario
Content-Type: application/json
```

Exemplo de corpo JSON:

```json
{
  "avaliacoes": [
    {
      "id": 27205,
      "nota": 9,
      "generos": [28, 878, 12],
      "comentario": "Filme excelente!"
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

### Análise de sentimentos

```http
POST /sentimentos/analisar
Content-Type: application/json
```

Corpo:

```json
{
  "comentario": "Esse filme é maravilhoso!"
}
```

Exemplo ilustrativo de resposta:

```json
{
  "sentimento": "POSITIVO",
  "confianca": 0.9876
}
```

A classificação e a confiança reais dependem do modelo.

### Recomendações integradas ao backend Java

```http
GET /recomendacoes/filmes/java
Authorization: Bearer SEU_TOKEN_JWT
```

A API utiliza o token para consultar as avaliações e os favoritos do usuário no backend Java, preparar os dados e gerar recomendações.

## 10. Integração com o TVScore

O fluxo de integração implementado no código do microsserviço é:

1. Receber um token JWT do usuário autenticado.
2. Consultar `/api/avaliacoes/minhas` no backend Java.
3. Consultar `/api/favoritos` no backend Java.
4. Identificar os filmes e séries avaliados ou favoritados.
5. Consultar seus gêneros no TMDB.
6. Calcular as preferências do usuário.
7. Aplicar o algoritmo de recomendação e os modelos de IA.
8. Retornar recomendações em JSON.

O serviço separa filmes (`MOVIE`) e séries (`TV`) durante a preparação dos dados.

## 11. Testes e validação

Durante o desenvolvimento foram realizados testes manuais utilizando o Swagger disponibilizado pelo FastAPI.

Entre os cenários trabalhados estão:

- Consulta de recomendações por gêneros.
- Geração de recomendações personalizadas.
- Recomendações separadas de filmes e séries.
- Classificação de comentários positivos, negativos e neutros.
- Comunicação com endpoints do backend Java.
- Preparação de avaliações e favoritos para o recomendador.

Esses testes contribuíram para a validação local das principais rotas.

**Limitações atuais:** o repositório não demonstra, por si só, uma implantação de produção totalmente validada. A integração final com o aplicativo e o backend Java, o desempenho em hospedagem e os testes automatizados completos ainda devem ser confirmados.

## 12. Desafios técnicos

O desenvolvimento do microsserviço envolveu desafios como:

- Integração entre Python e Java por meio de APIs REST.
- Tratamento de autenticação JWT.
- Padronização de dados de filmes e séries.
- Consulta e organização de dados externos do TMDB.
- Processamento de comentários com NLP.
- Uso de modelos de aprendizado de máquina para similaridade.
- Consumo de memória e tempo de inicialização dos modelos.
- Disponibilização do serviço em ambientes de hospedagem.

## 13. Objetivo acadêmico

O projeto demonstra a aplicação prática dos conceitos estudados no curso Técnico em Desenvolvimento de Sistemas, principalmente:

- Desenvolvimento de APIs REST.
- Arquitetura de microsserviços.
- Integração entre diferentes linguagens.
- Consumo de APIs externas.
- Inteligência artificial aplicada a sistemas.
- Processamento de linguagem natural.
- Organização e preparação de dados.

## 14. Repositórios do projeto

**Microsserviço de recomendação — Python:**

https://github.com/Kaique-Ramiro/recomendador-TvScore

**Backend — Java/Spring Boot:**

https://github.com/GuedesSiilva/BackEnd_Projeto_TvScore

**Aplicativo — Flutter:**

https://github.com/victorbispoo/tvScoreFrontFlutter

## 15. Referências

- FastAPI — https://fastapi.tiangolo.com/
- Python — https://www.python.org/
- Hugging Face Transformers — https://huggingface.co/docs/transformers/
- Sentence Transformers — https://www.sbert.net/
- TMDB API — https://developer.themoviedb.org/
- PyTorch — https://pytorch.org/

---

**TVScore — Projeto de Conclusão de Curso | SENAI — Desenvolvimento de Sistemas**

Microsserviço desenvolvido para implementar recomendações personalizadas de filmes e séries com técnicas de inteligência artificial.