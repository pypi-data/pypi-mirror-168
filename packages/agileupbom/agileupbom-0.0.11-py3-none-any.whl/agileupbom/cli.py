import click
import pkg_resources

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(help='CLI to support pipeline bill-of-materials management.')
def cli() -> int:
    pass


@cli.command(help='Display the current version.')
def version() -> None:
    click.echo(f"AgileUP BOM Version: {pkg_resources.get_distribution('agileupbom').version}")


@cli.command(help='Check client configuration.')
def check() -> None:
    click.secho('- Checking client configuration', fg='green')


if __name__ == '__main__':
    exit(cli())
