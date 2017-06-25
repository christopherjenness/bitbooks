import mock
import bitcoin
import lib.settings as settings
import lib.messaging as messaging
import data


def test_encode_message():
    message = 'This is a two transaction test message.  I hope.'
    counter = 'a'
    encode = messaging.encode_message(message, counter)
    targets = ['6a2061615468697320697320612074776f207472616e73616374696f6e2074657374',
               '6a146162206d6573736167652e20204920686f70652e']
    assert encode == targets


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.unspent', new=data.mock_unspent)
def test_send_message():
    recipient_addr = settings.MARKET_ADDRESS
    scripts = ['6a2061615468697320697320612074776f207472616e73616374696f6e2074657374',
               '6a146162206d6573736167652e20204920686f70652e']
    fee = 0
    signed_txs = messaging.send_message(recipient_addr, scripts,
                                        fee, send=False)
    target = ['0100000001a336dc8fa2babbe860f981bd5282e19d48d881315949b72eec407c416987c5f5000000008b483045022100fc1a6e82851ac046d7a7fa5f4b964166583b29bbc16d68864878f04e8740115002200b8198e21ee24a7737e4cbdd33cb77a205353e85aee602d7f87a185360db0ad70141044db9f40d98590a7f898cbfb8877dfb424c820bd2cd37a8ba6b77b9375349fbfca7dea8964b8e4ccea330a257ccff20ef53bcbc8e04111c6d23d2af21e29fea11ffffffff0222020000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac0000000000000000226a2061615468697320697320612074776f207472616e73616374696f6e207465737400000000', '0100000001a336dc8fa2babbe860f981bd5282e19d48d881315949b72eec407c416987c5f5000000008b483045022100807d56181f0185a329e588ae5bf6040c3d9df6c4314076b3780bb01064723248022011e6a6bec90aca23504793f318d94a4f6a099c46d2f14b908a5681218f98f94b0141044db9f40d98590a7f898cbfb8877dfb424c820bd2cd37a8ba6b77b9375349fbfca7dea8964b8e4ccea330a257ccff20ef53bcbc8e04111c6d23d2af21e29fea11ffffffff0222020000000000001976a9145222c8f8adb2610e00d15e95622824c2e3ecc33f88ac0000000000000000166a146162206d6573736167652e20204920686f70652e00000000']
    assert signed_txs == target


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.unspent', new=data.mock_unspent)
@mock.patch('bitcoin.history', new=data.mock_message_history)
def test_get_messages():
    messages = messaging.get_messages()
    assert '1GCQwy9v6dSwsK1nTYXFZzHDG6hTFJ7EY' in messages.keys()
    assert messages['1GCQwy9v6dSwsK1nTYXFZzHDG6hTFJ7EY']['a']['a'] == 'test-message. For testing.'


def test_collapse_messages():
    test_addr1 = '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'
    test_addr2 = '1GCQwy9v6dSwsK1nTYXFZzHDG6hTFJ7EY'
    test_dict = {test_addr1: {'a': {'a': 'M1 part1', 'b': ' M1 part2'},
                              'b': {'a': 'M2 part1'}},
                 test_addr2: {'a': {'a': '2M1 part1'}}}
    test_collapsed_dict = messaging.collapse_messages(test_dict)
    target_dict = {'1GCQwy9v6dSwsK1nTYXFZzHDG6hTFJ7EY': ['2M1 part1'],
                   '1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr': ['M1 part1 M1 part2',
                                                          'M2 part1']}
    assert test_collapsed_dict == target_dict


def test__get_message_prefix():
    test_addr = bitcoin.privtoaddr(bitcoin.random_key())
    prefix = messaging._get_message_prefix(test_addr)
    assert prefix == 'a'
