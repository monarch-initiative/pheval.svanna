import click

from pheval_svanna.prepare.prepare_commands import prepare_commands_command


@click.group()
def main():
    pass


main.add_command(prepare_commands_command)

if __name__ == "__main__":
    main()
