import click


@click.command()
@click.argument("name")
@click.argument("count")
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
def hello(count, name):
    """你好，你女朋友在我手里！速速转账"""
    click.echo(f"{count}, {name}", )
    # for x in range(count):
    #     click.echo(f'Hello {count},{1}')


if __name__ == '__main__':
    hello()
