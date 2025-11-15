#!/usr/bin/env python3
"""
Script de inicio para el Analizador Sintáctico de Gramáticas.
Universidad Pedagógica y Tecnológica de Colombia - UPTC

Interfaz moderna con ttkbootstrap (tema Bootstrap morph)

Uso:
    python run.py           # Inicia la interfaz gráfica con tema oscuro
    python run.py test      # Ejecuta los tests unitarios (47 tests)
    python run.py check     # Verifica el entorno
    python run.py help      # Muestra ayuda
"""

import sys
import os

def check_environment():
    """Verifica que el entorno esté correctamente configurado."""
    print("🔍 Verificando entorno...\n")
    
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Verificar ttkbootstrap (interfaz moderna basada en tkinter)
# Verificar ttkbootstrap (interfaz moderna basada en tkinter)
    try:
        import ttkbootstrap
        print("✅ ttkbootstrap disponible")
    except Exception as e:
        print("❌ ERROR: ttkbootstrap no está instalado o no se puede importar")
        print("   Solución: instala las dependencias del proyecto:")
        print("     pip install -r requirements.txt")
        print("   o instalar solo ttkbootstrap:")
        print("     pip install ttkbootstrap")
        return False
    
    # Verificar pytest para tests
    try:
        import pytest
        print(f"✅ pytest disponible")
    except ImportError:
        print("⚠️  pytest no instalado (solo necesario para ejecutar tests)")
    
    # Verificar estructura de carpetas
    required_files = [
        "services/grammar.py",
        "services/parser_cyk.py",
        "services/parser_regular.py",
        "services/generator.py",
        "services/tree.py",
        "ui/main.py"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"\n❌ ERROR: Faltan archivos:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("✅ Estructura de archivos correcta\n")
    return True

def run_gui():
    """Inicia la interfaz gráfica con tema Bootstrap morph."""
    print("\nIniciando Analizador Sintáctico...")
    print("   (Cierra la ventana para salir)\n")
    
    # Agregar directorio raíz al path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from ui.main import App
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"❌ ERROR al iniciar la aplicación:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def run_tests():
    """Ejecuta los 47 tests unitarios del proyecto."""
    print("\n🧪 Ejecutando suite de tests (47 tests)...\n")
    
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Intentar usar pytest (más moderno)
        import pytest
        exit_code = pytest.main(["-v", "tests/"])
        sys.exit(exit_code)
    except ImportError:
        print("⚠️  pytest no instalado, ejecutando tests básicos...\n")
        try:
            from tests.test_parser import (
                test_generator_simple,
                test_cnf_check,
                test_cyk_simple,
                test_grammar_validation
            )
            
            test_generator_simple()
            test_cnf_check()
            test_cyk_simple()
            test_grammar_validation()
            
            print("\n✅ Tests básicos pasaron correctamente")
            print("   Para ejecutar la suite completa de 47 tests, instala pytest:")
            print("     pip install pytest")
        except Exception as e:
            print(f"\n❌ ERROR en los tests:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

def show_help():
    """Muestra información de ayuda."""
    print("""
Analizador Sintáctico de Gramáticas Formales

USO:
    python run.py           Inicia la interfaz gráfica (tema oscuro)
    python run.py test      Ejecuta los 47 tests unitarios
    python run.py check     Verifica el entorno y dependencias
    python run.py help      Muestra esta ayuda

INSTALACIÓN:
    1. Crear entorno virtual (recomendado):
       Windows:    python -m venv venv && venv\\Scripts\\activate
       Linux/Mac:  python3 -m venv venv && source venv/bin/activate
    
    2. Instalar dependencias:
       pip install -r requirements.txt
    
    3. Ejecutar:
       python run.py

CARACTERÍSTICAS:
    - Soporte de gramáticas Tipo 2 (GLC) y Tipo 3 (regulares)
    - Algoritmo CYK para análisis sintáctico
    - Generador de cadenas con BFS
    - 47 tests unitarios para validación
    - Exportación de árboles de derivación y cadenas generadas

DOCUMENTACIÓN:
    Consulta README.md para guía completa
    Consulta TESTING.md para información de tests

SOLUCIÓN DE PROBLEMAS:
    • Ejecuta 'python run.py check' para diagnosticar
    • Asegúrate de instalar: pip install -r requirements.txt
    • Si falta pytest: pip install pytest (para 47 tests)

AUTORES:
    Steven León - Mileth Martínez - Natalia Bernal
    """)


def main():
    """Función principal."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            if not check_environment():
                sys.exit(1)
            run_tests()
        
        elif command == "check":
            check_environment()
        
        elif command == "help":
            show_help()
        
        else:
            print(f"❌ Comando desconocido: {command}")
            print("   Usa 'python run.py help' para ver comandos disponibles")
            sys.exit(1)
    else:
        # Sin argumentos: iniciar GUI
        if not check_environment():
            print("\n⚠️  Hay problemas con el entorno.")
            print("   Usa 'python run.py check' para más detalles")
            sys.exit(1)
        run_gui()

if __name__ == "__main__":
    main()