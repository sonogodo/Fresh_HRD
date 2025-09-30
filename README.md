# Ache o candidato certo para a sua vaga

Este projeto implementa o **hR**, hybridResources, uma solução web para realizar o matching entre vagas de emprego de tecnologia do nível júnior e candidatos possíveis, como foco no mercado de tecnologia, através do uso de análise de texto e cobertura de competências. A API foi desenvolvida com [FastAPI](https://fastapi.tiangolo.com/) e pode ser utilizada para identificar os candidatos mais aderentes a uma vaga específica ou para processar múltiplas vagas de uma só vez.

A versão aqui apresentada é a **free** e com uma quantidade limitada de candidatos com formação em 2025. A versão premium é mais precisa e mais próxima das capacidades humanas, com pesquisa semântica/contextual e com atualização semestral de candidatos de diversas formações. Versão premium disponível sob encomenda.

## Sumário

- [Estrutura do repositório](#Estrutura-do-repositório)
- [Hipótese](#hipótese)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)

---

## Estrutura do repositório

- JSONs/
- Matching/
- Utils/
- api.py
- dataExploration.ipynb
- requirements.txt
- vercel.json

## Hipótese

Como analisado no arquivo dataExploration.py, a maior parte das vagas (mais de 40%) são do nível júnior. Ao automatizarmos o matching dos candidatos com as respectivas vagas, propomos dedicar a atenção dos funcionários de empresas de head hunting às vagas com mais nuances e especificidades, como é o caso de vagas de nível pleno, sênior ou de liderança.

Com o hybridResources propomos um paradigma de trabalho baseado em **inteligência híbrida**:

*Aos humanos, o complexo e subjetivo. Às máquinas, o simples e massivo.*

## Funcionalidades

- Recebe uma descrição de vaga e retorna os 3 candidatos mais aderentes de acordo com a descrição;
- Ou recebe um arquivo JSON com múltiplas vagas e retorna os 3 melhores candidatos para cada vaga.

**ATENÇÃO**: o JSON deve ser sempre na estrutura do arquivo vagas_padrao.json, disponível na pasta JSONs.

## Instalação

1. Clone o repositório:
  ```sh
  git clone <url-do-repositorio>
  cd <nome-da-pasta>
  ```

2. Instale as dependências:
  ```sh
  pip install -r requirements.txt
  ```

3. (Opcional) Para rodar localmente:
  ```sh
  uvicorn api:app --reload
  ```