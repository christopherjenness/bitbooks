"""Library for buying and selling books"""

import os
import binascii
import isbnlib
import bitcoin
import settings


def make_wallet():
    """
    Makes wallet

    Returns:
         addr (str): Address of wallet
    """
    priv = bitcoin.random_key()
    pub = bitcoin.privtopub(priv)
    addr = bitcoin.pubtoaddr(pub)
    fname = "{dir}wallets/{name}.txt".format(dir=settings.user_dir,
                                             name=settings.ACCOUNT_NAME)
    # This needs to be encrypted with password
    if not os.path.isfile(fname):
        with open(fname, "wb") as text_file:
            text_file.write(priv)
    return addr


def read_wallet():
    """
    Gets wallet details from disk

    Returns:
        priv, pub, addr (str, str, str): private key, public key, address
    """
    fname = "{dir}wallets/{name}.txt".format(dir=settings.user_dir,
                                             name=settings.ACCOUNT_NAME)
    with open(fname, "r") as text_file:
        priv = str(text_file.read())
    pub = bitcoin.privtopub(priv)
    addr = bitcoin.pubtoaddr(pub)
    return priv, pub, addr


def encode_OP_RETURN(isbn, price, quality):
    """
    Encode a book sale in OP_RETURN

    Args:
        isbn (int): 10 digit ISBN
        price (int): price in dollars (no cents)
        quality (int): int in range(1,6) to indicate quality

    Returns:
        script (str): script of encoded book sale.
    """
    message = "{isbn}-{price}-{quality}".format(isbn=isbn,
                                                price=price,
                                                quality=quality)
    messagelen = format(len(message), 'x').rjust(2, '0')
    ID = binascii.hexlify(str(message))
    script = "6a" + messagelen + ID
    return script


def build_tx(inputs, priv, addr, script, fee=0, send=False):
    """
    Build a transaction to post/cancel a book sale

    Args:
        inputs (list): list of UTXOs to use.
            Obtained with bitcoin.unspent()
        priv (str): private key for wallet
        addr (str): address to post sale to
        script (str): script with encoded message of sale/cancelation
        fee (int): satoshis to pay to miners to write to the blockchain
            There is no reason to do this.
        send (bool): if True, send to mempool

    Returns:
        signed_tx (str): signed transaction to send to mempool
        also, sends transaction to mempool
    """
    outputs = [{'value': 546, 'address': settings.MARKET_ADDRESS},
               {'value': 0, 'script': script}]
    fee = fee
    tx = bitcoin.mksend(inputs[0], outputs, addr, fee)
    signed_tx = bitcoin.sign(tx, 0, priv)
    if send:
        bitcoin.pushtx(signed_tx)
    return signed_tx


def get_postings():
    """
    Retrive all books for sale in the mempool

    Returns:
        current_postings (list): list of current postings
            each element is tuple of (poster, isbn, price, quality)
    """
    postings = []
    canceled_postings = []
    current_postings = []
    txs = bitcoin.history(settings.MARKET_ADDRESS)
    for tx in txs:
        poster, isbn, price = None, None, None
        fetched = bitcoin.fetchtx(tx['output'].split(':')[0])
        tx_outputs = bitcoin.deserialize(fetched)['outs']
        for output in tx_outputs:
            if (output['script'].startswith('76a914') and
                    output['value'] != 546):
                text = output['script'].lstrip('76a914').rstrip('88ac')
                poster = bitcoin.hex_to_b58check(text)
            if output['script'].startswith('6a'):
                text = str(binascii.unhexlify(output['script'][2:]))
                components = text.split('-')
        if len(components) == 3:
            isbn, price, quality = components
            isbn = isbn[-10:]
        if poster and isbn and price and quality:
            if price == '0':
                canceled_postings.append((poster, isbn))
            else:
                postings.append((poster, isbn, price, quality))
    for posting in postings:
        if (posting[0], posting[1]) not in canceled_postings:
            current_postings.append(posting)
    return list(set(current_postings))


def get_balance():
    """
    Get wallet balance

    Returns:
        balance (int): satoshis in wallet
    """
    priv, pub, addr = read_wallet()
    inputs = bitcoin.unspent(addr)
    balance = 0
    for input in inputs:
        balance += input['value']
    return balance


def _build_cancelation(isbn):
    """Builds cancelation transaction."""
    return encode_OP_RETURN(isbn, 0, 0)


def cancel_posting(isbn):
    """
    Cancel a book sale that is already in the mempool.
    Useful if you have already sold the book.

    Args:
        isbn (str): 10 digit ISBN 

    Returns:
        signed_tx (str): signed transaction of cancelled sale
    """
    priv, pub, addr = read_wallet()
    script = _build_cancelation(isbn)
    inputs = bitcoin.unspent(addr)
    signed_tx = build_tx(inputs, priv, addr, script, send=True)
    return signed_tx


def post_book(isbn, price, quality):
    """
    Post a book sale to the mempool.

    Args:
        isbn (str): 10 digit ISBN

    Returns:
        signed_tx (str): signed transaction of book sale.
    """
    priv, pub, addr = read_wallet()
    script = encode_OP_RETURN(isbn, price, quality)
    inputs = bitcoin.unspent(addr)
    signed_tx = build_tx(inputs, priv, addr, script, send=True)
    return signed_tx


def book_lookup(isbn):
    """
    Look up book by ISBN

    Args:
        isbn (str): 10 digit ISBN 

    Returns:
        title, authors (str, str): title and authors of books
    """
    book = isbnlib.meta(isbn)
    title = book['Title']
    authors = ' '.join(book['Authors'])
    return title, authors
