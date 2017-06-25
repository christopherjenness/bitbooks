def mock_key(*args):
    TEST_KEY = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    return TEST_KEY


def mock_history(*args):
    history = [{'output': u'f8025248bc9b0a1e0156f50cb90639494b9746b0a3460fc0952e56a783c228dc:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'e77accab1c33bdb9701382b27104fd0d0492bc6ad8bb5ef851ab1b5f2b34cf9c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'9a646d96f4b385c1519b659e478deff32d9c494cd1391aab6f52426dfae37e1c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'02e72cf27a689b5d57fc956192dde08e12b39e6a1093c548909212d336692f93:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'cf3760d9059c630af0383549d0574850bca0dad685e90566b152a6e42d2561a6:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}]
    return history


def mock_unspent(*args):
    unspent = [{'output': 'f5c58769417c40ec2eb749593181d8489de18252bd81f960e8bbbaa28fdc36a3:0', 'value': 546}, {'output': 'dac331e027d3e3f37467b494e451a9f8295819fea43b90f807f8e768ede75600:0', 'value': 546}, {'output': 'd8b59131bf3374f71b8a12052fe4eba4cb0eeaad98e6b4c86ee08d0d3ecd66e6:0', 'value': 546}, {'output': '7fddd54c1b2e488dbb302400cc77fe9c393c957ae4013f029a3ba59566d97cc4:0', 'value': 546}]
    return unspent


def mock_message_history(*args):
    history = [{'output': u'95ba5d4dbda3c8ecfff34b0ab3e7957c01157399defdbe21c5ca2c5dff7a099f:0', 'block_height': None, 'value': 546, 'address': u'1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'}, {'output': u'9084282edfef8af0168aa0fbf9458e14bed41cf699c50d417525d1987dc21491:0', 'block_height': None, 'spend': u'ac7803279585f412e658d6d3da63bff50ba562f6eff4bb134908f0733a6d4060:0', 'value': 546, 'address': u'1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'}, {'output': u'eda70cdee5be07e04964131c0363699ff1289a2ffeef4f51f4cbffdbb24abe08:0', 'block_height': None, 'spend': u'46ce580438f6c9d5425116cfc2637b6ee20d0aca0749e7f2e46412073a33fd90:0', 'value': 546, 'address': u'1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'}, {'output': u'4f9d68e88a2151c82f0a6d31ed6b67924b2a6dd67dab02ea1108470211709c99:0', 'block_height': None, 'spend': u'aa124292ee3ce7457de60173f98705b020cd56bbd4fffc7ca7c045ef746a08f2:0', 'value': 546, 'address': u'1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'}, {'output': u'933044f110dfb3ba58f4c1d59ae5608f3a3510370b94e795b3b7682a2ce877f3:0', 'block_height': None, 'spend': u'ebed8ada80e3774cd812400ce0c0e0458fc9385cde1cef0c835beec59ca6f5ec:0', 'value': 546, 'address': u'1DRmwtSp9yKtThdNWm7Dbsx5Ds7cTSKYRr'}]
    return history
