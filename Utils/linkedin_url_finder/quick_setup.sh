#!/bin/bash
# Script de Configuração Rápida - LinkedIn URL Finder

echo "🚀 Configurando LinkedIn URL Finder..."

# Instalar dependências Python
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Configurar ChromeDriver
echo "🔧 Configurando ChromeDriver..."
python setup_chromedriver.py

# Verificar status
echo "📊 Verificando status atual..."
python check_progress.py

echo "✅ Configuração completa!"
echo "Execute 'python linkedin_production.py' para começar"
