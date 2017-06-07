import isbnlib
from electrum.wallet import WalletStorage, Wallet
import os
from bitcoin import sha256, privtopub, pubtoaddr, history, fetchtx, deserialize, unspent, mksend, sign, pushtx, pushtx
import binascii

isbn = '978-0387848570'
book = isbnlib.meta(isbn)

MARKET_ADDRESS = "18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns"
SEED_TEXT = "travel nowhere air position hill peace suffer parent beautiful rise blood power home crumble teach"
PASSWORD = "secret"
ACCOUNT_NAME = "MAIN"
user_dir = os.path.expanduser('~') + "/.book-lib/wallets/"


def make_wallet(seed, password, name):
    priv = sha256(seed)
    pub = privtopub(priv)
    addr = pubtoaddr(pub)
    fname = "{dir}{name}.txt".format(dir=user_dir, name=ACCOUNT_NAME)
    # This needs to be encrypted with password
    with open(fname, "wb") as text_file:
        text_file.write(priv)
    return addr


def encode_OP_RETURN(isbn, price):
    message = "{isbn}{price}".format(isbn=isbn, price=price)
    MessageLen = format(len(message),'x').rjust(2,'0')
    ID = binascii.hexlify(str(message))
    script = "6a"+MessageLen+ID
    return script


def build_tx(priv, script, fee=0, s=True):
    outputs = [{'value': 1, 'address': MARKET_ADDRESS}, {'value': 0, 'script': script}]
    fee = fee
    tx = mksend(inputs[0], outputs, addr, fee)
    if send:
        signed_tx = sign(tx, 0, priv)
        pushtx(signed_tx)

addr = make_wallet(SEED_TEXT, PASSWORD, ACCOUNT_NAME)
script = encode_OP_RETURN(1483746362, 20)
