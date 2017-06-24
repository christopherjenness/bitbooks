def mock_key(*args):
    TEST_KEY = '5e08ea249bc4d925462c3b5ba290aab27aac9eeb0e2d6b3ff1118034961b9520'
    return TEST_KEY


def mock_history(*args):
    history = [{'output': u'f8025248bc9b0a1e0156f50cb90639494b9746b0a3460fc0952e56a783c228dc:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'e77accab1c33bdb9701382b27104fd0d0492bc6ad8bb5ef851ab1b5f2b34cf9c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'9a646d96f4b385c1519b659e478deff32d9c494cd1391aab6f52426dfae37e1c:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'02e72cf27a689b5d57fc956192dde08e12b39e6a1093c548909212d336692f93:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}, {'output': u'cf3760d9059c630af0383549d0574850bca0dad685e90566b152a6e42d2561a6:0', 'block_height': None, 'value': 546, 'address': u'18VJ5dy5YR6bK8H5EFb2o6dFz3pKaze8Ns'}]
    return history


def mock_unspent(*args):
    unspent = [{'output': 'f5c58769417c40ec2eb749593181d8489de18252bd81f960e8bbbaa28fdc36a3:0', 'value': 546}, {'output': 'dac331e027d3e3f37467b494e451a9f8295819fea43b90f807f8e768ede75600:0', 'value': 546}, {'output': 'd8b59131bf3374f71b8a12052fe4eba4cb0eeaad98e6b4c86ee08d0d3ecd66e6:0', 'value': 546}, {'output': '7fddd54c1b2e488dbb302400cc77fe9c393c957ae4013f029a3ba59566d97cc4:0', 'value': 546}]
    return unspent
