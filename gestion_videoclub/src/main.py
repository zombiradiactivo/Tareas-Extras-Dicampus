from src.database.db_handler import create_tables
from src.ui.menu import MenuPrincipal

def main():
    # 1. Creamos las tablas si no existen
    create_tables()
    
    # 2. Iniciamos la interfaz
    app = MenuPrincipal()
    app.ejecutar()

if __name__ == "__main__":
    main()