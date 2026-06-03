"""Gerador de banner ASCII da Mission Control AI (trilha EnviroSat).

Uso:
    python banner_ascii.py                       # banner padrão
    python banner_ascii.py --fonts               # lista as fontes do PyFiglet
    python banner_ascii.py --font slant --text "Mission Control AI"
    python banner_ascii.py --demo                # compara algumas fontes
"""
import argparse

import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def render_banner(linha1_txt="Global Solution",
                  linha2_txt="Mission Control AI",
                  font="ansi_shadow"):
    """Gera e imprime o banner em ASCII art, no estilo da CLI."""
    linha1 = pyfiglet.figlet_format(linha1_txt, font=font)
    linha2 = pyfiglet.figlet_format(linha2_txt, font=font)
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))


def listar_fontes():
    """Imprime todas as fontes disponíveis no PyFiglet."""
    for fonte in sorted(pyfiglet.FigletFont.getFonts()):
        console.print(fonte)


def demo():
    """Mostra a frase em algumas fontes diferentes para comparação."""
    fontes = ["ansi_shadow", "slant", "standard", "small",
              "big", "banner3", "doom", "isometric1"]
    for fonte in fontes:
        console.rule(f"[bold #06B6D4]{fonte}")
        try:
            console.print(pyfiglet.figlet_format("Mission Control", font=fonte))
        except Exception as e:
            console.print(f"(fonte indisponível: {e})", style="red")


def main():
    parser = argparse.ArgumentParser(
        description="Banner ASCII da Mission Control AI"
    )
    parser.add_argument("--fonts", action="store_true",
                        help="lista as fontes disponíveis")
    parser.add_argument("--font", default="ansi_shadow",
                        help="fonte do PyFiglet a usar")
    parser.add_argument("--text", default="Mission Control AI",
                        help="texto da segunda linha")
    parser.add_argument("--demo", action="store_true",
                        help="compara várias fontes lado a lado")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demo()
    else:
        render_banner(linha2_txt=args.text, font=args.font)


if __name__ == "__main__":
    main()
