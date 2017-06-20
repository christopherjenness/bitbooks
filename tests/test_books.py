import pytest
import mock
import lib.books as books
import lib.settings as settings


def mock_key():
    TEST_KEY = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    return TEST_KEY


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.random_key', new=mock_key)
def test_make_wallet():
    addr = books.make_wallet()
    assert addr == '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
def test_read_wallet():
    priv, pub, addr = books.read_wallet()
    assert addr == '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'


def test_encode_OP_RETURN():
    isbn = '0439708184'
    price = 10
    quality = 4
    script = books.encode_OP_RETURN(isbn, price, quality)
    assert script == '6a0f303433393730383138342d31302d34'


def test_build_tx():
    inputs = [{'output': '4d4ba9372df63596693f429c6900ea072e5f005dd0d929e9e204cd767cf80430:2', 'value': 6724}]
    priv = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    addr = settings.MARKET_ADDRESS
    script = '6a0f303433393730383138342d31302d34'
    signed_tx = books.build_tx(inputs, priv, addr, script, fee=0, send=False)
    assert signed_tx == '01000000013004f87c76cd04e2e929d9d05d005f2e07ea00699c423f699635f62d37a94b4d020000008a47304402201a554496aba439197b33094992a58e0212b050921e292dc7dd01acacc7ef138e02204cc8135e11d6a81028878c537fdad664a228e80943d2c0a12b71eff46bf027da0141044db9f40d98590a7f898cbfb8877dfb424c820bd2cd37a8ba6b77b9375349fbfca7dea8964b8e4ccea330a257ccff20ef53bcbc8e04111c6d23d2af21e29fea11ffffffff0322020000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac0000000000000000116a0f303433393730383138342d31302d3422180000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac00000000'

