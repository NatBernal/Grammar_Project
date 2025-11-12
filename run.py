#!/usr/bin/env python3
"""
Script de inicio para el Analizador Sintáctico de Gramáticas.
Universidad Pedagógica y Tecnológica de Colombia - UPTC

Uso:
    python run.py           # Inicia la interfaz gráfica
    python run.py test      # Ejecuta los tests
    python run.py help      # Muestra ayuda
"""

import sys
import os

def check_environment():
    """Verifica que el entorno esté correctamente configurado."""
    print("🔍 Verificando entorno...")
    
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Verificar tkinter
    try:
        import tkinter
        print("✅ tkinter disponible")
    except ImportError:
        print("❌ ERROR: tkinter no está instalado")
        print("   Instalación:")
        print("   - Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   - Fedora: sudo dnf install python3-tkinter")
        return False
    
    # Verificar estructura de carpetas
    required_files = [
        "services/grammar.py",
        "services/parser_cyk.py",
        "services/generator.py",
        "services/tree.py",
        "ui/main.py"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ ERROR: Faltan archivos:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("✅ Estructura de archivos correcta")
    return True

def run_gui():
    """Inicia la interfaz gráfica."""
    print("\n🚀 Iniciando interfaz gráfica...")
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
        sys.exit(1)

def run_tests():
    """Ejecuta los tests del proyecto."""
    print("\n🧪 Ejecutando tests...\n")
    
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
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
        
        print("\n✅ Todos los tests pasaron correctamente")
    except Exception as e:
        print(f"\n❌ ERROR en los tests:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def show_help():
    """Muestra información de ayuda."""
    print("""
╔══════════════════════════════════════════════════════════╗
║  Analizador Sintáctico de Gramáticas Formales          ║
║  Universidad Pedagógica y Tecnológica de Colombia       ║
╚══════════════════════════════════════════════════════════╝

USO:
    python run.py           Inicia la interfaz gráfica
    python run.py test      Ejecuta los tests
    python run.py check     Verifica el entorno
    python run.py help      Muestra esta ayuda

EJEMPLOS DE GRAMÁTICAS:
    examples/ejemplo_cnf.json       - Gramática simple en CNF
    examples/ejemplo_regular.json   - Gramática regular (Tipo 3)

DOCUMENTACIÓN:
    Ver README.md para guía completa de uso

SOPORTE:
    - Revisa README.md
    - Ejecuta 'python run.py check' para diagnosticar problemas
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