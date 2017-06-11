import click
import books
import messaging


QUALITY_DICT = {'1': 'USED - POOR',
                '2': 'USED - OK',
                '3': 'USED - GREAT',
                '4': 'NEW - OPEN',
                '5': 'NEW - UNOPENED'}


@click.group()
def cli():
    return None


@cli.command()
def wallet():
    """Displays wallet address.  Generates a wallet if you do not have one"""
    books.make_wallet()
    balance = books.get_balance()
    addr = books.read_wallet()[2]
    click.echo("Address: {addr}".format(addr=addr))
    click.echo("Balance: {bal}".format(bal=balance))
    click.echo('Load a small amount of funds to post books and send messages')
    click.echo('This wallet is unecrypted.  Do not store too much on it')


@cli.command()
@click.option('--isbn', prompt='10 digit ISBN',
              help='The 10 digit ISBN of your book for sale')
@click.option('--price', prompt='Sale price (whole dollar amount, no cents)',
              help=('How much are you asking for your book.'
                    'Do not include cents.'))
@click.option('--quality', prompt='Quality (1-5)',
              help='Quality of book. 1-5 scale')
def post(isbn, price, quality):
    title, authors = books.book_lookup(isbn)
    click.echo("Your book is: {title} by {authors}".format(title=title,
                                                           authors=authors))
    click.echo("Sale price: {price}".format(price=price))
    click.echo(("Quality: {quality},"
               "{description}").format(quality=quality,
                                       description=QUALITY_DICT[quality]))
    if click.confirm('Do you want to post this book?'):
        click.echo('We Sellin')
    else:
        click.echo('nah')


@cli.command()
def balance():
    bal = books.get_balance()
    click.echo("Your balance is: {bal}".format(bal=bal))


@cli.command()
@click.option('--isbn', prompt='ISBN to cancel',
              help='ISBN of book sale you want to remove')
def cancel(isbn):
    books.cancel_posting(isbn)


@cli.command()
@click.option('--sender', help='Address of sender', default=None)
def getMessages(sender):
    raw_message_dict = messaging.get_messages()
    message_dict = messaging.collapse_messages(raw_message_dict)
    if sender:
        messages = message_dict[sender]
        for message in messages:
            click.echo(message)
    else:
        for sender in message_dict.keys():
            click.echo(click.style(sender, fg='green'))
            messages = message_dict[sender]
            for message in messages:
                click.echo(message)


@cli.command()
@click.option('--addr', prompt='To',
              help="Recipient's Address")
@click.option('--message', prompt='Message',
              help='Message to send')
def sendMessage(addr, message):
    counter = messaging._get_message_prefix(addr)
    message = messaging.encode_message(message, counter)
    messaging.send_message(addr, message, send=True)
    click.echo('Sent!')


@cli.command()
def postings():
    postings = books.get_postings()
    for posting in postings:
        cli.echo(posting)


if __name__ == '__main__':
    cli()
