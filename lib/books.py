import os
import binascii
import isbnlib
import bitcoin

MARKET_ADDRESS = "18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns"
ACCOUNT_NAME = "MAIN-ACCOUNT"
user_dir = os.path.expanduser('~') + "/.book-lib/wallets/"


def make_wallet():
    priv = bitcoin.random_key()
    pub = bitcoin.privtopub(priv)
    addr = bitcoin.pubtoaddr(pub)
    fname = "{dir}{name}.txt".format(dir=user_dir, name=ACCOUNT_NAME)
    # This needs to be encrypted with password
    if not os.path.isfile(fname):
        with open(fname, "wb") as text_file:
            text_file.write(priv)
    return addr


def read_wallet():
    fname = "{dir}{name}.txt".format(dir=user_dir, name=ACCOUNT_NAME)
    with open(fname, "rb") as text_file:
        priv = text_file.read()
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
    outputs = [{'value': 546, 'address': MARKET_ADDRESS},
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
    txs = bitcoin.history(MARKET_ADDRESS)
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
        print 8888812333, postings
    for posting in postings:
        print ('8888'), (posting[0], posting[1])
        if (posting[0], posting[1]) not in canceled_postings:
            current_postings.append(posting)
    return list(set(current_postings))


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
