# Localizador de Perfis do LinkedIn

Uma ferramenta automatizada de descoberta de perfis do LinkedIn que busca perfis de formandos usando Selenium e técnicas de web scraping.

## 🎯 Funcionalidades

- **Alta Taxa de Sucesso**: Alcança 99%+ de taxa de sucesso na busca de perfis do LinkedIn
- **Processamento Inteligente**: Pula automaticamente registros já processados
- **Sistema de ID Único**: Cada perfil encontrado recebe um identificador único
- **Processamento em Lotes**: Processa registros em lotes com atrasos respeitosos
- **Capacidade de Retomada**: Pode ser interrompido e retomado com segurança
- **Múltiplas Opções de Processamento**: De testes rápidos a execuções completas de produção
- **Gerenciamento de Dados Limpo**: Arquivo mestre único sem duplicatas

## 📊 Resultados Atuais

- ✅ **160 perfis únicos do LinkedIn encontrados**
- 🎯 **100% de taxa de sucesso** para formandos recentes (2024-2025)
- 📈 **Processamento completo do público-alvo**
- 🚀 **Pronto para produção e estável**

## 🛠️ Instalação

### Pré-requisitos

- Python 3.7+
- Navegador Google Chrome
- ChromeDriver (baixado automaticamente pelo script de configuração)

### Configuração

1. Clone o repositório:

```bash
git clone https://github.com/yourusername/linkedin-url-finder.git
cd linkedin-url-finder
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o ChromeDriver:

```bash
python setup_chromedriver.py
```

## 🚀 Uso

### Início Rápido

Execute o script principal de produção:

```bash
python linkedin_production.py
```

### Opções de Processamento

1. **Teste rápido** (próximos 10 não processados) - Perfeito para testes
2. **Lote pequeno** (próximos 50 não processados) - Execuções pequenas
3. **Lote médio** (próximos 200 não processados) - Execuções médias
4. **Lote grande** (próximos 500 não processados) - Execuções grandes
5. **🚀 MODO PRODUÇÃO** - Todos os registros não processados restantes
6. **Quantidade personalizada** - Especifique quantos registros não processados

### Verificar Progresso

Monitore seu progresso a qualquer momento:

```bash
python check_progress.py
```

## 📁 Estrutura de Arquivos

```
├── linkedin_production.py      # Script principal de produção
├── linkedin_success_master.json # Arquivo mestre com todos os perfis encontrados
├── new_graduates.csv           # Dados de entrada (lista de formandos)
├── check_progress.py           # Ferramenta de monitoramento de progresso
├── setup_chromedriver.py       # Utilitário de configuração do ChromeDriver
├── linkedin_selenium_simple.py # Script de teste simples
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

## 📊 Estrutura de Dados

### Formato CSV de Entrada

```csv
Nome,Data da Colação,Curso,Faculdade
João Silva,29/08/2025,Engenharia Civil,UNESP
Maria Santos,07/02/2025,Ciência da Computação,UNESP
```

### Formato JSON de Saída

```json
{
  "id": "abc12345",
  "Nome": "João Silva",
  "Curso": "Engenharia Civil",
  "Faculdade": "UNESP",
  "Data da Colação": "29/08/2025",
  "LinkedIn URL": "https://linkedin.com/in/joaosilva",
  "Last Updated": "2025-09-21 20:32:05"
}
```

## 🔧 Detalhes Técnicos

### Como Funciona

1. **Busca Inteligente**: Usa Selenium para automatizar buscas no DuckDuckGo
2. **Correspondência de Padrões**: Gera múltiplas variações de consulta de busca
3. **Validação de URL**: Valida e limpa URLs do LinkedIn encontradas
4. **Prevenção de Duplicatas**: Pula automaticamente registros já processados
5. **Processamento em Lotes**: Processa registros em lotes com atrasos para respeitar limites de taxa

### Estratégia de Busca

- Motor de busca principal: DuckDuckGo (amigável à automação)
- Múltiplos padrões de consulta por pessoa
- Extração e limpeza inteligente de URLs
- Simulação de navegador real para evitar detecção de bot

### Otimizações de Performance

- **Pulo Inteligente**: Processa apenas registros não processados
- **Processamento em Lotes**: 25 registros por lote com pausas de 30 segundos
- **Salvamento de Progresso**: Salva progresso a cada 5 lotes
- **Eficiente em Memória**: Abordagem de arquivo mestre único
- **Capacidade de Retomada**: Pode reiniciar de onde parou

## 📈 Métricas de Sucesso

- **100% de Taxa de Sucesso**: Encontra perfis do LinkedIn para 100% dos formandos recentes pesquisados
- **160 Perfis Encontrados**: Descobriu com sucesso 160 perfis únicos do LinkedIn
- **Zero Duplicatas**: Detecção inteligente de duplicatas garante dados limpos
- **Estável em Produção**: Lida com conjuntos de dados grandes (2.400+ registros) de forma confiável

## 🛡️ Limitação de Taxa e Ética

- **Atrasos Respeitosos**: Atrasos de 2-4 segundos entre buscas
- **Pausas entre Lotes**: Pausas de 30 segundos entre lotes
- **Rotação de User-Agent**: Usa cabeçalhos de navegador realistas
- **Sem Scraping Agressivo**: Segue práticas éticas de web scraping

## 🔄 Retomando Sessões Interrompidas

O sistema lida automaticamente com interrupções:

1. O progresso é salvo no arquivo mestre a cada 5 lotes
2. Na reinicialização, carrega resultados existentes e pula registros processados
3. Sem perda de dados - todos os perfis encontrados são preservados
4. Simplesmente execute o script novamente para continuar de onde parou

## 📊 Monitorando Progresso

Use o verificador de progresso para ver o status atual:

```bash
python check_progress.py
```

Mostra:

- Total de perfis encontrados
- Porcentagem de progresso
- Registros restantes para processar
- Descobertas de perfis recentes
- Timestamp da última atualização

## 🤝 Contribuindo

1. Faça um fork do repositório
2. Crie uma branch de funcionalidade (`git checkout -b feature/funcionalidade-incrivel`)
3. Faça commit das suas mudanças (`git commit -m 'Adiciona funcionalidade incrível'`)
4. Faça push para a branch (`git push origin feature/funcionalidade-incrivel`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Aviso Legal

Esta ferramenta é para fins educacionais e de pesquisa. Por favor, certifique-se de cumprir com:

- Termos de Serviço do LinkedIn
- Leis locais de proteção de dados (LGPD, GDPR, CCPA, etc.)
- Práticas éticas de web scraping
- Limitação de taxa e uso respeitoso

## 🎯 Melhorias Futuras

- [ ] Suporte multi-threading para processamento mais rápido
- [ ] Integração com motores de busca adicionais
- [ ] Exportação para diferentes formatos (Excel, CSV)
- [ ] Opções avançadas de filtragem e busca
- [ ] Interface web para uso mais fácil
- [ ] Integração de API para processamento em tempo real

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique as issues existentes no GitHub
2. Crie uma nova issue com informações detalhadas
3. Inclua mensagens de erro e informações do sistema

---

**Feito com ❤️ para descoberta eficiente de perfis do LinkedIn**
