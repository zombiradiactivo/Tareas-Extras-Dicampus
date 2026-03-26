#!/usr/bin/env python
"""
Script de prueba para validar las visualizaciones sin interfaz gráfica.
Simula el proceso de carga, limpieza y generación de gráficos.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Configurar para no mostrar ventanas gráficas
plt.switch_backend('Agg')

def load_data():
    """Cargar el CSV de Netflix"""
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'netflix_titles.csv')
    df = pd.read_csv(csv_path)
    print(f"✓ Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

def clean_data(df):
    """Limpiar los datos"""
    df_clean = df.copy()
    
    # Rellenar valores faltantes en director y cast
    if 'director' in df_clean.columns:
        df_clean['director'] = df_clean['director'].fillna('Desconocido')
    if 'cast' in df_clean.columns:
        df_clean['cast'] = df_clean['cast'].fillna('Desconocido')
    
    # Rellenar country
    if 'country' in df_clean.columns:
        df_clean['country'] = df_clean['country'].fillna('Unknown')
        df_clean['country'] = df_clean['country'].str.strip()
        df_clean['country'] = df_clean['country'].replace('', 'Unknown')
    
    # Eliminar filas con valores nulos en columnas críticas
    critical_cols = ['type', 'title', 'release_year', 'listed_in']
    df_clean = df_clean.dropna(subset=critical_cols)
    
    # Eliminar duplicados
    df_clean = df_clean.drop_duplicates()
    
    # Enstandarizar título
    if 'title' in df_clean.columns:
        df_clean['title'] = df_clean['title'].str.title()
    
    # Convertir date_added a datetime
    if 'date_added' in df_clean.columns:
        df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
    
    # Extraer duración numérica
    if 'duration' in df_clean.columns:
        df_clean['duration_minutes'] = df_clean['duration'].str.extract('(\\d+)').astype(float)
    
    print(f"✓ Datos limpiados: {df_clean.shape[0]} filas, {df_clean.shape[1]} columnas")
    return df_clean

def test_tarea1(df_clean):
    """Tarea 1: Contar títulos añadidos a Netflix por año"""
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'date_added' in df_clean.columns:
            df_with_year = df_clean[df_clean['date_added'].notna()].copy()
            df_with_year['year_added'] = df_with_year['date_added'].dt.year
            titles_by_year = df_with_year.groupby('year_added').size().sort_index()
            
            ax.bar(titles_by_year.index, titles_by_year.values, color='#45b7d1', edgecolor='#2c3e50', linewidth=1.5)
            ax.set_title('Títulos Añadidos a Netflix por Año', fontsize=14, fontweight='bold')
            ax.set_xlabel('Año de Adición', fontsize=12)
            ax.set_ylabel('Número de Títulos', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3, linestyle='--')
            
            print(f"✓ Tarea 1: {len(titles_by_year)} años procesados")
        else:
            print("✗ Tarea 1: Columna date_added no disponible")
        
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Tarea 1: {str(e)}")
        return False

def test_tarea2(df_clean):
    """Tarea 2: Proporción Movies vs TV Shows + top 10 países"""
    try:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        if 'type' in df_clean.columns:
            type_counts = df_clean['type'].value_counts()
            colors = ['#ff6b6b', '#4ecdc4']
            explode = (0.05, 0.05)
            axes[0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
                       startangle=90, colors=colors, explode=explode)
            axes[0].set_title('Proporción de Contenido', fontsize=12, fontweight='bold')
        
        # Top 10 countries
        if 'country' in df_clean.columns:
            df_countries = df_clean[df_clean['country'].notna()].copy()
            countries_split = df_countries['country'].str.split(', ').explode()
            countries_count = countries_split.value_counts().head(10)
            
            axes[1].barh(range(len(countries_count)), countries_count.values, color='#96ceb4', edgecolor='#2c3e50')
            axes[1].set_yticks(range(len(countries_count)))
            axes[1].set_yticklabels(countries_count.index)
            axes[1].set_xlabel('Número de Títulos', fontsize=11)
            axes[1].set_title('Top 10 Países', fontsize=12, fontweight='bold')
            axes[1].invert_yaxis()
            axes[1].grid(True, alpha=0.3, axis='x', linestyle='--')
            
            print(f"✓ Tarea 2: {len(countries_count)} países procesados")
        
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Tarea 2: {str(e)}")
        return False

def test_tarea3(df_clean):
    """Tarea 3: Evolución doble películas vs series por año"""
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'type' in df_clean.columns and 'release_year' in df_clean.columns:
            movies_df = df_clean[df_clean['type'] == 'Movie'].copy()
            movies_by_year = movies_df.groupby('release_year').size().sort_index()
            
            tv_df = df_clean[df_clean['type'] == 'TV Show'].copy()
            tv_by_year = tv_df.groupby('release_year').size().sort_index()
            
            ax.plot(movies_by_year.index, movies_by_year.values, marker='o', linewidth=2.5, 
                   label='Películas', color='#ff6b6b', markersize=6)
            ax.plot(tv_by_year.index, tv_by_year.values, marker='s', linewidth=2.5, 
                   label='Series de TV', color='#4ecdc4', markersize=6)
            
            # Anotaciones
            max_movies_year = movies_by_year.idxmax()
            max_movies_val = movies_by_year.max()
            ax.annotate(f'{int(max_movies_val)}', xy=(max_movies_year, max_movies_val),
                       xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold', color='#ff6b6b')
            
            max_tv_year = tv_by_year.idxmax()
            max_tv_val = tv_by_year.max()
            ax.annotate(f'{int(max_tv_val)}', xy=(max_tv_year, max_tv_val),
                       xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold', color='#4ecdc4')
            
            ax.set_title('Evolución de Películas vs Series de TV por Año', fontsize=14, fontweight='bold')
            ax.set_xlabel('Año de Lanzamiento', fontsize=12)
            ax.set_ylabel('Número de Títulos', fontsize=12)
            ax.legend(loc='upper left', fontsize=11)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.tick_params(axis='x', rotation=45)
            
            print(f"✓ Tarea 3: Películas ({len(movies_by_year)} años), Series ({len(tv_by_year)} años)")
        
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Tarea 3: {str(e)}")
        return False

def test_tarea4(df_clean):
    """Tarea 4: Top 10 géneros con barras horizontal y valores"""
    try:
        fig, ax = plt.subplots(figsize=(12, 7))
        
        if 'listed_in' in df_clean.columns:
            genres = df_clean['listed_in'].str.split(', ').explode()
            top_genres = genres.value_counts().head(10)
            
            bars = ax.barh(range(len(top_genres)), top_genres.values, color='#96ceb4', edgecolor='#2c3e50', linewidth=1.5)
            ax.set_yticks(range(len(top_genres)))
            ax.set_yticklabels(top_genres.index, fontsize=11)
            ax.set_xlabel('Número de Títulos', fontsize=12)
            ax.set_title('Top 10 Géneros en Netflix', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x', linestyle='--')
            
            # Añadir valores dentro de las barras
            for i, (bar, value) in enumerate(zip(bars, top_genres.values)):
                ax.text(value + 5, i, str(int(value)), va='center', fontweight='bold', fontsize=10)
            
            print(f"✓ Tarea 4: {len(top_genres)} géneros procesados")
        
        plt.close(fig)
        return True
    except Exception as e:
        print(f"✗ Tarea 4: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("PRUEBA DE VISUALIZACIONES - ANALIZADOR DE NETFLIX")
    print("=" * 60)
    
    try:
        # Cargar y limpiar datos
        df = load_data()
        df_clean = clean_data(df)
        
        # Ejecutar pruebas
        print("\nEjecutando pruebas de visualizaciones:")
        print("-" * 60)
        
        results = []
        results.append(("Tarea 1: Barras títulos por año", test_tarea1(df_clean)))
        results.append(("Tarea 2: Tarta + top países", test_tarea2(df_clean)))
        results.append(("Tarea 3: Líneas películas vs series", test_tarea3(df_clean)))
        results.append(("Tarea 4: Barras horizontal géneros", test_tarea4(df_clean)))
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for name, result in results:
            status = "PASS" if result else "FAIL"
            print(f"[{status}] {name}")
        
        print("-" * 60)
        print(f"Total: {passed}/{total} pruebas pasadas")
        
        if passed == total:
            print("¡Todas las tareas implementadas correctamente!")
        else:
            print(f"⚠ {total - passed} tarea(s) con problemas")
        
    except Exception as e:
        print(f"\n✗ Error general: {str(e)}")
        return 1
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
