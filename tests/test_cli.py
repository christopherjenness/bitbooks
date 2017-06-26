import mock
import click
from click.testing import CliRunner
import lib.cli as cli
import lib.settings as settings
import data


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
def test_wallet():
    runner = CliRunner()
    result = runner.invoke(cli.wallet)
    assert result.exit_code == 0


def test_post():
    runner = CliRunner()
    result = runner.invoke(cli.post, input='0387848576\n200\n3\nn\n')
    assert result.exit_code == 0


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
def test_balance():
    runner = CliRunner()
    result = runner.invoke(cli.balance)
    assert result.exit_code == 0


def test_cancel():
    runner = CliRunner()
    result = runner.invoke(cli.cancel, input='0387848576\nn')
    assert result.exit_code == 0


@mock.patch('lib.settings.ACCOUNT_NAME', new='TEST-ACCOUNT')
@mock.patch('bitcoin.unspent', new=data.mock_unspent)
@mock.patch('bitcoin.history', new=data.mock_message_history)
def test_getMessages():
    runner = CliRunner()
    result = runner.invoke(cli.getMessages)
    assert result.exit_code == 0


@mock.patch('lib.messaging.send_message', return_value=True)
def test_sendMessages(*args):
    runner = CliRunner()
    result = runner.invoke(cli.sendMessage,
                           input='settings.MARKET_ADDRESS\nhi\n')
    assert result.exit_code == 0


def test_postings():
    runner = CliRunner()
    result = runner.invoke(cli.postings)
    assert result.exit_code == 0
