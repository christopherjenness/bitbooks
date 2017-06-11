import os
import binascii
import isbnlib
import bitcoin
import settings


def make_wallet():
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
    fname = "{dir}wallets/{name}.txt".format(dir=settings.user_dir,
                                             name=settings.ACCOUNT_NAME)
    with open(fname, "r") as text_file:
        priv = str(text_file.read())
    pub = bitcoin.privtopub(priv)
    addr = bitcoin.pubtoaddr(pub)
    return priv, pub, addr


def encode_OP_RETURN(isbn, price, quality):
    message = "{isbn}-{price}-{quality}".format(isbn=isbn,
                                                price=price,
                                                quality=quality)
    messagelen = format(len(message), 'x').rjust(2, '0')
    ID = binascii.hexlify(str(message))
    script = "6a" + messagelen + ID
    return script


def build_tx(inputs, priv, addr, script, fee=0, send=False):
    outputs = [{'value': 546, 'address': settings.MARKET_ADDRESS},
               {'value': 0, 'script': script}]
    fee = fee
    tx = bitcoin.mksend(inputs[0], outputs, addr, fee)
    if send:
        signed_tx = bitcoin.sign(tx, 0, priv)
        bitcoin.pushtx(signed_tx)
        return signed_tx


def get_postings():
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
    priv, pub, addr = read_wallet()
    inputs = bitcoin.unspent(addr)
    balance = 0
    for input in inputs:
        balance += input['value']
    return balance


def build_cancelation(isbn):
    return encode_OP_RETURN(isbn, 0, 0)


def cancel_posting(isbn):
    priv, pub, addr = read_wallet()
    script = build_cancelation(isbn)
    inputs = bitcoin.unspent(addr)
    signed_tx = build_tx(inputs, priv, addr, script, send=True)
    return signed_tx


def post_book(isbn, price, quality):
    priv, pub, addr = read_wallet()
    script = encode_OP_RETURN(isbn, price, quality)
    inputs = bitcoin.unspent(addr)
    signed_tx = build_tx(inputs, priv, addr, script, send=True)
    return signed_tx


def book_lookup(isbn):
    book = isbnlib.meta(isbn)
    title = book['Title']
    authors = ' '.join(book['Authors'])
    return title, authors
