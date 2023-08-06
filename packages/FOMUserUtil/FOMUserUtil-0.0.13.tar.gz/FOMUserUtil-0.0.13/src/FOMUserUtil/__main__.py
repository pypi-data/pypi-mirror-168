try:
    from . import fomuser
except ImportError:
    import fomuser

if __name__ == '__main__':
    cli = fomuser.CLI()
    cli.defineParser()
