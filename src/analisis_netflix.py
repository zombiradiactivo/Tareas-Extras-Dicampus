import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class NetflixAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Netflix")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.df = None
        self.cleaned_df = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Analizador de Datos de Netflix", 
                               font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Cargar CSV", 
                  command=self.load_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mostrar Información", 
                  command=self.show_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Detectar Nulos", 
                  command=self.detect_nulls).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Datos", 
                  command=self.clean_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Estadísticas", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Visualizaciones", 
                  command=self.show_visualizations).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", 
                  command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para cargar datos")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab for data preview
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="Vista Preliminar")
        
        # Tab for statistics
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Estadísticas")
        
        # Tab for visualizations
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Visualizaciones")
        
    def load_csv(self):
        try:
            # Default to the data folder
            file_path = filedialog.askopenfilename(
                initialdir=os.path.join(os.path.dirname(__file__), '..', 'data'),
                title="Seleccionar archivo CSV",
                filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
            )
            
            if not file_path:
                return
                
            self.df = pd.read_csv(file_path)
            self.status_var.set(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            self.show_preview()
            messagebox.showinfo("Éxito", "Datos cargados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def show_preview(self):
        # Clear previous content
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        if self.df is None:
            ttk.Label(self.preview_frame, text="No hay datos cargados").pack(pady=20)
            return
            
        # Create a text widget to show dataframe info
        text_widget = tk.Text(self.preview_frame, wrap=tk.NONE, width=80, height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=text_widget.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(self.preview_frame, orient=tk.HORIZONTAL, command=text_widget.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Insert dataframe info
        info_text = f"FORMAS: {self.df.shape}\n\n"
        info_text += f"TIPOS DE DATOS:\n{self.df.dtypes}\n\n"
        info_text += f"PRIMERAS 5 FILAS:\n{self.df.head()}\n\n"
        info_text += f"ESTADÍSTICAS DESCRIPTIVAS:\n{self.df.describe(include='all')}"
        
        text_widget.insert(tk.END, info_text)
        text_widget.configure(state=tk.DISABLED)
    
    def show_info(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero cargue los datos")
            return
            
        info_window = tk.Toplevel(self.root)
        info_window.title("Información del DataFrame")
        info_window.geometry("600x500")
        
        text_widget = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        info_text = f"INFORMACIÓN DEL DATASET\n{'='*50}\n\n"
        info_text += f"Dimensiones: {self.df.shape[0]} filas × {self.df.shape[1]} columnas\n\n"
        info_text += f"Tipos de datos:\n{self.df.dtypes.to_string()}\n\n"
        info_text += f"Valores nulos por columna:\n{self.df.isnull().sum().to_string()}\n\n"
        info_text += f"Duplicados: {self.df.duplicated().sum()}\n\n"
        info_text += f"Primeras 5 filas:\n{self.df.head().to_string()}\n\n"
        info_text += f"Estadísticas descriptivas:\n{self.df.describe(include='all').to_string()}"
        
        text_widget.insert(tk.END, info_text)
        text_widget.configure(state=tk.DISABLED)
    
    def clean_data(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero cargue los datos")
            return
            
        try:
            # Create a copy for cleaning
            df_clean = self.df.copy()
            
            # 1. Handle missing values according to criteria
            # director and cast → 'Desconocido'
            if 'director' in df_clean.columns:
                df_clean['director'] = df_clean['director'].fillna('Desconocido')
            if 'cast' in df_clean.columns:
                df_clean['cast'] = df_clean['cast'].fillna('Desconocido')
            
            # Keep critical columns, fill missing values in optional columns
            if 'country' in df_clean.columns:
                df_clean['country'] = df_clean['country'].fillna('Unknown')
            
            # For country, also standardize formatting
            if 'country' in df_clean.columns:
                df_clean['country'] = df_clean['country'].str.strip()
                df_clean['country'] = df_clean['country'].replace('', 'Unknown')
            
            # Remove rows with null values only in critical columns (type, title, release_year, listed_in, date_added)
            critical_cols = ['type', 'title', 'release_year', 'listed_in']
            df_clean = df_clean.dropna(subset=critical_cols)
            
            # 2. Remove duplicates
            df_clean = df_clean.drop_duplicates()
            
            # 3. Standardize text formats
            # Title case for title column
            if 'title' in df_clean.columns:
                df_clean['title'] = df_clean['title'].str.title()
            
            # 4. Convert date_added to datetime
            if 'date_added' in df_clean.columns:
                df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
            
            # 5. Extract numeric duration
            if 'duration' in df_clean.columns:
                # Extract numbers from duration string
                df_clean['duration_minutes'] = df_clean['duration'].str.extract('(\\d+)').astype(float)
                # For TV shows, we might want to keep seasons separate, but for simplicity we'll just note it
            
            self.cleaned_df = df_clean
            self.status_var.set("Datos limpiados correctamente")
            messagebox.showinfo("Éxito", "Datos limpiados correctamente")
            
            # Show preview of cleaned data
            self.show_cleaned_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar datos:\n{str(e)}")
    
    def show_cleaned_preview(self):
        if self.cleaned_df is None:
            return
            
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Vista Preliminar de Datos Limpiados")
        preview_window.geometry("700x500")
        
        text_widget = tk.Text(preview_window, wrap=tk.NONE, width=80, height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar = ttk.Scrollbar(preview_window, orient=tk.VERTICAL, command=text_widget.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(preview_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        info_text = f"DATOS LIMPIADOS\n{'='*50}\n\n"
        info_text += f"Dimensiones: {self.cleaned_df.shape[0]} filas × {self.cleaned_df.shape[1]} columnas\n\n"
        info_text += f"Tipos de datos:\n{self.cleaned_df.dtypes.to_string()}\n\n"
        info_text += f"Primeras 5 filas:\n{self.cleaned_df.head().to_string()}\n\n"
        info_text += f"Valores nulos después de limpieza:\n{self.cleaned_df.isnull().sum().to_string()}"
        
        text_widget.insert(tk.END, info_text)
        text_widget.configure(state=tk.DISABLED)
    
    def show_statistics(self):
        if self.cleaned_df is None:
            messagebox.showwarning("Advertencia", "Primero limpie los datos")
            return
            
        # Clear previous content
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Create a text widget for statistics
        text_widget = tk.Text(self.stats_frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Calculate statistics with numpy
        stats_text = f"ESTADÍSTICAS CON NUMPY\n{'='*50}\n\n"
        
        # Numerical columns for analysis
        numerical_cols = self.cleaned_df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) > 0:
            for col in numerical_cols:
                data = self.cleaned_df[col].dropna()
                if len(data) > 0:
                    mean_val = np.mean(data)
                    std_val = np.std(data)
                    percentiles = np.percentile(data, [25, 50, 75])
                    
                    stats_text += f"Columna: {col}\n"
                    stats_text += f"  Media: {mean_val:.2f}\n"
                    stats_text += f"  Desviación estándar: {std_val:.2f}\n"
                    stats_text += f"  Percentil 25%: {percentiles[0]:.2f}\n"
                    stats_text += f"  Percentil 50% (mediana): {percentiles[1]:.2f}\n"
                    stats_text += f"  Percentil 75%: {percentiles[2]:.2f}\n\n"
        else:
            stats_text += "No se encontraron columnas numéricas para análisis.\n"
            
        # Additional info about categorical data
        stats_text += f"INFORMACIÓN DE VARIABLES CATEGÓRICAS\n{'='*50}\n\n"
        categorical_cols = self.cleaned_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_count = self.cleaned_df[col].nunique()
            top_value = self.cleaned_df[col].mode()[0] if not self.cleaned_df[col].mode().empty else "N/A"
            stats_text += f"Columna: {col}\n"
            stats_text += f"  Valores únicos: {unique_count}\n"
            stats_text += f"  Valor más frecuente: {top_value}\n\n"
        
        text_widget.insert(tk.END, stats_text)
        text_widget.configure(state=tk.DISABLED)
    
    def show_visualizations(self):
        if self.cleaned_df is None:
            messagebox.showwarning("Advertencia", "Primero limpie los datos")
            return
            
        # Clear previous content
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        # Create a container frame
        container = ttk.Frame(self.viz_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons frame for navigation
        buttons_frame = ttk.Frame(container)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(buttons_frame, text="Seleccionar visualización:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Tarea 1", command=self._viz_tarea1).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Tarea 2", command=self._viz_tarea2).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Tarea 3", command=self._viz_tarea3).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Tarea 4", command=self._viz_tarea4).pack(side=tk.LEFT, padx=5)
        
        # Create frame for displaying plots
        self.plot_display_frame = ttk.Frame(container)
        self.plot_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display Tarea 1 by default
        self._viz_tarea1()
    
    def _viz_tarea1(self):
        """Tarea 1: Contar títulos añadidos a Netflix por año con groupby y gráfico de barras"""
        # Clear previous content
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'date_added' in self.cleaned_df.columns:
            # Extract year from date_added
            df_with_year = self.cleaned_df[self.cleaned_df['date_added'].notna()].copy()
            df_with_year['year_added'] = pd.to_datetime(df_with_year['date_added']).dt.year
            
            # Group by year and count
            titles_by_year = df_with_year.groupby('year_added').size().sort_index()
            
            # Create bar chart
            ax.bar(titles_by_year.index, titles_by_year.values, color='#45b7d1', edgecolor='#2c3e50', linewidth=1.5)
            ax.set_title('Títulos Añadidos a Netflix por Año', fontsize=14, fontweight='bold')
            ax.set_xlabel('Año de Adición', fontsize=12)
            ax.set_ylabel('Número de Títulos', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3, linestyle='--')
        else:
            ax.text(0.5, 0.5, 'Columna date_added no disponible', ha='center', va='center')
        
        plt.tight_layout()
        self._embed_plot(fig)
    
    def _viz_tarea2(self):
        """Tarea 2: Proporción Movies vs TV Shows + top 10 países"""
        # Clear previous content
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Análisis de Contenido y Distribución Geográfica', fontsize=14, fontweight='bold')
        
        # Plot 1: Pie chart - Movies vs TV Shows
        if 'type' in self.cleaned_df.columns:
            type_counts = self.cleaned_df['type'].value_counts()
            colors = ['#ff6b6b', '#4ecdc4']
            explode = (0.05, 0.05)
            axes[0].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
                       startangle=90, colors=colors, explode=explode)
            axes[0].set_title('Proporción de Contenido', fontsize=12, fontweight='bold')
        
        # Plot 2: Top 10 countries (if available)
        if 'country' in self.cleaned_df.columns:
            df_countries = self.cleaned_df[self.cleaned_df['country'].notna()].copy()
            # Split countries and explode
            countries_split = df_countries['country'].str.split(', ').explode()
            countries_count = countries_split.value_counts().head(10)
            
            axes[1].barh(range(len(countries_count)), countries_count.values, color='#96ceb4', edgecolor='#2c3e50')
            axes[1].set_yticks(range(len(countries_count)))
            axes[1].set_yticklabels(countries_count.index)
            axes[1].set_xlabel('Número de Títulos', fontsize=11)
            axes[1].set_title('Top 10 Países', fontsize=12, fontweight='bold')
            axes[1].invert_yaxis()
            axes[1].grid(True, alpha=0.3, axis='x', linestyle='--')
        else:
            axes[1].text(0.5, 0.5, 'Columna country no disponible', ha='center', va='center', transform=axes[1].transAxes)
        
        plt.tight_layout()
        self._embed_plot(fig)
    
    def _viz_tarea3(self):
        """Tarea 3: Evolución doble películas vs series por año de lanzamiento"""
        # Clear previous content
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'type' in self.cleaned_df.columns and 'release_year' in self.cleaned_df.columns:
            # Filter and group movies
            movies_df = self.cleaned_df[self.cleaned_df['type'] == 'Movie'].copy()
            movies_by_year = movies_df.groupby('release_year').size().sort_index()
            
            # Filter and group TV shows
            tv_df = self.cleaned_df[self.cleaned_df['type'] == 'TV Show'].copy()
            tv_by_year = tv_df.groupby('release_year').size().sort_index()
            
            # Plot lines
            ax.plot(movies_by_year.index, movies_by_year.values, marker='o', linewidth=2.5, 
                   label='Películas', color='#ff6b6b', markersize=6)
            ax.plot(tv_by_year.index, tv_by_year.values, marker='s', linewidth=2.5, 
                   label='Series de TV', color='#4ecdc4', markersize=6)
            
            # Annotations for maximum values
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
        else:
            ax.text(0.5, 0.5, 'Columnas requeridas no disponibles', ha='center', va='center')
        
        plt.tight_layout()
        self._embed_plot(fig)
    
    def _viz_tarea4(self):
        """Tarea 4: Top 10 géneros con barras horizontal y valores numéricos"""
        # Clear previous content
        for widget in self.plot_display_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        if 'listed_in' in self.cleaned_df.columns:
            # Process genres
            genres = self.cleaned_df['listed_in'].str.split(', ').explode()
            top_genres = genres.value_counts().head(10)
            
            # Create horizontal bar chart
            bars = ax.barh(range(len(top_genres)), top_genres.values, color='#96ceb4', edgecolor='#2c3e50', linewidth=1.5)
            ax.set_yticks(range(len(top_genres)))
            ax.set_yticklabels(top_genres.index, fontsize=11)
            ax.set_xlabel('Número de Títulos', fontsize=12)
            ax.set_title('Top 10 Géneros en Netflix', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x', linestyle='--')
            
            # Add values inside bars
            for i, (bar, value) in enumerate(zip(bars, top_genres.values)):
                ax.text(value + 5, i, str(int(value)), va='center', fontweight='bold', fontsize=10)
        else:
            ax.text(0.5, 0.5, 'Columna listed_in no disponible', ha='center', va='center')
        
        plt.tight_layout()
        self._embed_plot(fig)
    
    def _embed_plot(self, fig):
        """Embed matplotlib figure in Tkinter frame"""
        canvas = FigureCanvasTkAgg(fig, master=self.plot_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        from matplotlib.backends._backend_tk import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, self.plot_display_frame)
        toolbar.update()

    def detect_nulls(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero cargue los datos")
            return
            
        null_counts = self.df.isnull().sum()
        total_rows = len(self.df)
        
        # Calcular porcentaje de nulos usando NumPy
        null_percentages = (null_counts / total_rows) * 100
        
        # Mostrar resultados
        result_window = tk.Toplevel(self.root)
        result_window.title("Valores Nulos y Porcentajes")
        result_window.geometry("600x400")
        
        text_widget = tk.Text(result_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        result_text = f"VALORES NULOS POR COLUMNA\n{'='*50}\n\n"
        result_text += f"{'Columna':<20} {'Nulos':<10} {'Porcentaje':<15}\n"
        result_text += f"{'-'*50}\n"
        
        for col, count in null_counts.items():
            percentage = null_percentages[col]
            result_text += f"{col:<20} {count:<10} {percentage:.2f}%\n"
        
        text_widget.insert(tk.END, result_text)
        text_widget.configure(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = NetflixAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
