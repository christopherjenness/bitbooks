import pytest
import mock
import books
import cli
import settings

def mock_key():
    TEST_KEY = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    return TEST_KEY

@mock.patch('settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.random_key', new=mock_key)
def test_make_wallet():
    addr = books.make_wallet()
    assert addr == '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'


@mock.patch('settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
def test_read_wallet():
    priv, pub, addr = books.read_wallet()
    assert addr == '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'


def test_encode_OP_RETURN():
    isbn = '0439708184'
    price = 10
    quality = 4
    script = books.encode_OP_RETURN(isbn, price, quality)
    assert script == '6a0f303433393730383138342d31302d34'

