#!/bin/bash

# Script de inicio rápido para la aplicación de Multiplicación de Matrices Paralelas

echo "=================================================="
echo "  Multiplicación de Matrices Paralelas"
echo "  Python + Streamlit + Multiprocessing"
echo "=================================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️  No se encontró entorno virtual."
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo "❌ Error al crear entorno virtual"
        exit 1
    fi

    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python -c "import streamlit" &> /dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi

    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "=================================================="
echo "🚀 Iniciando aplicación Streamlit..."
echo "=================================================="
echo ""
echo "La aplicación se abrirá en: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

# Ejecutar Streamlit
streamlit run app.py
