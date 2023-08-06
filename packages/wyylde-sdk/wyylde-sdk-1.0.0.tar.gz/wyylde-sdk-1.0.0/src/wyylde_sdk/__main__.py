"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Wyylde SDK."""


if __name__ == "__main__":
    main(prog_name="wyylde-sdk")  # pragma: no cover
