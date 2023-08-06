import click
import courts_api


@click.command()
@click.argument('group', default=None, required=False)
@click.option('--reset/--no-reset', default=False, help='Delete existing group keys in config')
def configure(group, reset):
    courts_api.config.update(group, reset)


@click.group()
def main():
    pass

main.add_command(configure)

if __name__ == '__main__':
    main()