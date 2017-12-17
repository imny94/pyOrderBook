def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

dependencies = ["tkinter", "PIL", "sqlite3", "bintrees"]
for i in dependencies:
    install_and_import(i)
