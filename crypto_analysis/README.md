# Proyecto-Cryptomonedas

Proyecto final de la asignatura de "Python para análisis de datos" del Máster en Big Data Science de la Universidad de Navarra. Elaboración de una aplicación para la represación de información de la cotización de criptomonedas. 

**Autores: Héctor González y Abdelaziz el Kadi.**

## Descripción

El codigo despliega una plataforma interactiva que utiliza datos de la API de Kraken para realizar un análisis exhaustivo de criptomonedas. Con un dashboard desplegado mediante Streamlit, ofrece visualizaciones detalladas e indicadores técnicos. El proyecto tiene una estructura modular y unala configuración centralizada, dispone de tests unitarios y de integración.

## Intrucciones de ejecución

1. Descargue el código fuente del proyecto, disponible en el archivo `crypto_analysis.zip` adjunto. Posteriormente, extraiga su contenido y navegue hasta la ubicación del proyecto.

2. Instale la biblioteca del proyecto `crypto_analysis` utilizando la herramienta `pip`. Este proceso instalará de manera automática todas las dependencias necesarias. Utilice el siguiente comando:

    ```
    pip install .\dist\crypto_analysis-0.1.0-py3-none-any.whl
    ```

3. Ejecute el script `run.py` utilizando Streamlit para desplegar la aplicación:

    ```
    streamlit run .\run.py
    ```

