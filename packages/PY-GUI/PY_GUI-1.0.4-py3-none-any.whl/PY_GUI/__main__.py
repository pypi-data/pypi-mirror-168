try:
    from . import Main
except ImportError:
    from __init__ import Main
def parse(text):
    return text
def main():
    Main(parse, "cat")
if __name__ == "__main__":
    main()