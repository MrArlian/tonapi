import argparse

from pytonapi.__meta__ import __version__


def main() -> None:
    """CLI entry-point."""
    parser = argparse.ArgumentParser(
        prog="pytonapi",
        description="pytonapi CLI.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"pytonapi {__version__}",
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
