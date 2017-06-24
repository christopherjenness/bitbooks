import mock
import lib.books as books
import lib.settings as settings


def mock_key(*args):
    TEST_KEY = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    return TEST_KEY


def mock_history(*args):
    history = [{'output': u'f8025248bc9b0a1e0156f50cb90639494b9746b0a3460fc0952e56a783c228dc:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'e77accab1c33bdb9701382b27104fd0d0492bc6ad8bb5ef851ab1b5f2b34cf9c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'9a646d96f4b385c1519b659e478deff32d9c494cd1391aab6f52426dfae37e1c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'02e72cf27a689b5d57fc956192dde08e12b39e6a1093c548909212d336692f93:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'cf3760d9059c630af0383549d0574850bca0dad685e90566b152a6e42d2561a6:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}]
    return history


def mock_unspent(*args):
    unspent = [{'output': 'f5c58769417c40ec2eb749593181d8489de18252bd81f960e8bbbaa28fdc36a3:0', 'value': 546}, {'output': 'dac331e027d3e3f37467b494e451a9f8295819fea43b90f807f8e768ede75600:0', 'value': 546}, {'output': 'd8b59131bf3374f71b8a12052fe4eba4cb0eeaad98e6b4c86ee08d0d3ecd66e6:0', 'value': 546}, {'output': '7fddd54c1b2e488dbb302400cc77fe9c393c957ae4013f029a3ba59566d97cc4:0', 'value': 546}]
    return unspent


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


@mock.patch('bitcoin.history', new=mock_history)
def test_get_postings():
    current_postings = books.get_postings()
    post = current_postings[0]
    sender, isbn, price, quality = post
    assert sender == '1Jd6hfigG6ta56JGXCbFxDKwDifPTd7fNX'
    assert isbn == '0387848576'
    assert price == '200'
    assert quality == '3'


@mock.patch('bitcoin.unspent', new=mock_unspent)
def test_get_balance():
    balance = books.get_balance()
    assert balance == 2184


def test__build_cancelation():
    isbn = '0439708184'
    cancelled_tx = books._build_cancelation(isbn)
    assert cancelled_tx == '6a0e303433393730383138342d302d30'


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.unspent', new=mock_unspent)
def test_cancel_posting():
    isbn = '0439708184'
    signed_tx = books.cancel_posting(isbn, send=False)
    target = '0100000001a336dc8fa2babbe860f981bd5282e19d48d881315949b72eec407c416987c5f5000000008b483045022100877f984db564ce450f57d9e26b34e60daad4fd6ef2b00b76621dbde5d97a723602203003eb163d4a4c3f419a72faf21ffeac3e0cc051db2435d7b15fdf4c89e845160141044db9f40d98590a7f898cbfb8877dfb424c820bd2cd37a8ba6b77b9375349fbfca7dea8964b8e4ccea330a257ccff20ef53bcbc8e04111c6d23d2af21e29fea11ffffffff0222020000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac0000000000000000106a0e303433393730383138342d302d3000000000'
    assert signed_tx == target


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.unspent', new=mock_unspent)
def test_post_book():
    isbn = isbn = '0439708184'
    price = 200
    quality = 3
    signed_tx = books.post_book(isbn, price, quality, send=False)
    target = '0100000001a336dc8fa2babbe860f981bd5282e19d48d881315949b72eec407c416987c5f5000000008a473044022067f62c9c4f55bdeb008fac649be3742bfd91bb8da0fecd4c7c938f0e3903712402206ca9137954e9f53a9e2b55b566be91099c5b6eba041ad157f3e6b47da812877b0141044db9f40d98590a7f898cbfb8877dfb424c820bd2cd37a8ba6b77b9375349fbfca7dea8964b8e4ccea330a257ccff20ef53bcbc8e04111c6d23d2af21e29fea11ffffffff0222020000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac0000000000000000126a10303433393730383138342d3230302d3300000000'
    assert signed_tx == target


def test_book_lookup():
    isbn = '0439708184'
    title, authors = books.book_lookup(isbn)
    assert title == "Harry Potter And The Sorcerer's Stone"
    assert authors == 'J. K. Rowling'
