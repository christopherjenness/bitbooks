"""Messaging system on top of the bitcoin mempool"""

import binascii
from collections import defaultdict
import books
import bitcoin
import settings
import os


def encode_message(message, counter):
    """
    Encodes a message into an OP_RETURN output

    Args:
        message (str): Message to be encoded
        counter (str): Counter to order the messages in
            the mempool.

    Returns:
        scripts (list): list of strings, each element is a single
            encoded message.  Multiple encodings are needed
            if the message is longer than 40 char.

    Notes:
        Message are encoded in OP_RETURN with two prefix characters.
        Char 1 keeps track of which message number it is
        Char 2 keeps track of which submessage number it is, 
            if the message needs to be broken up to encode.
    """
    scripts = []
    messages = [message[i:i+30] for i in range(0, len(message), 30)]
    partition_counter = 'a'
    for partition in messages:
        partition = counter + partition_counter + partition
        messagelen = format(len(partition), 'x').rjust(2, '0')
        ID = binascii.hexlify(str(partition))
        script = "6a" + messagelen + ID
        scripts.append(script)
        partition_counter = chr(ord(partition_counter) + 1)
    return scripts


def send_message(recipient_addr, scripts, fee=0, send=False):
    """
    Send encoded message

    Args:
        recipient_addr (str): address of user to send message too
        scripts (list): list of strings, each element is a single
            encoded message.  Multiple encodings are needed
            if the message is longer than 40 char.
        fee (int): Satoshis to pay in miner fees.
            Not actually required.
        send (bool): If True, send transactions to mempool.

    Returns:
        signed_txs (list): list of strings where each element
            is a signed transaction encoding a message

        Also sends transaction to the mempool.

    Notes: 
        This is currently sending the message to blockchain.info,
        but this is trivially changed if needed.
    """
    priv, pub, addr = books.read_wallet()
    signed_txs = []
    for script in scripts:
        outputs = [{'value': 546, 'address': recipient_addr}]
        inputs = bitcoin.unspent(addr)
        outputs.append({'value': 0, 'script': script})
        fee = fee
        tx = bitcoin.mksend(inputs[0], outputs, addr, fee)
        signed_tx = bitcoin.sign(tx, 0, priv)
        if send:
            bitcoin.pushtx(signed_tx)
        signed_txs.append(signed_tx)
    if send:
        _write_message(recipient_addr, signed_txs)
    return signed_txs


def _write_message(recipient_addr, signed_txs):
    """

    Writes message to disk. Used to persist sent messages.

    Args:
        recipient_addr (str): address of user to send message to
        signed_txs (list): list of strings where each element
            is a signed transaction encoding a message

    Returns:
        None
        Writes message to disk
    """
    fname = "{dir}sent/{name}.txt".format(dir=settings.user_dir,
                                          name=recipient_addr)
    with open(fname, "a") as text_file:
        text_file.write(str(signed_txs) + '\n')


def get_messages():
    """
    Gets inbox messages from the mempool

    Returns:
        messages (dict): dict of messages
            {sender: {message_num: {submessage_num: message}}}
    """
    messages = defaultdict(dict)
    priv, pub, addr = books.read_wallet()
    txs = bitcoin.history(addr)
    for tx in txs:
        sender, message_num, submessage_num, message = None, None, None, None
        fetched = bitcoin.fetchtx(tx['output'].split(':')[0])
        tx_outputs = bitcoin.deserialize(fetched)['outs']
        for output in tx_outputs:
            if (output['script'].startswith('76a914') and
                    output['value'] != 546):
                text = output['script'].lstrip('76a914').rstrip('88ac')
                sender = bitcoin.hex_to_b58check(text)
            if output['script'].startswith('6a'):
                text = str(binascii.unhexlify(output['script'].lstrip('6a')))
                message_num = text[1]
                submessage_num = text[2]
                message = text[3:]
            if sender and message:
                if sender != addr:
                    if sender not in messages:
                        messages[sender] = defaultdict(dict)
                    messages[sender][message_num].update({submessage_num:
                                                          message})
    return messages


def collapse_messages(message_dict):
    """
    Collapses message_dict into parsable dictionary

    Args:
        messages (dict): dict of messages
            {sender: {message_num: {submessage_num: message}}}

    Returns:
        all_messages (dict): dict of messages
            {sender: [message 1, messsage 2, ...]}
    """
    all_messages = {}
    for sender in message_dict.keys():
        messages = []
        for message_num in sorted(message_dict[sender].keys()):
            current_message = []
            for submessage in sorted(message_dict[sender][message_num].keys()):
                current_message.append(message_dict[sender][message_num][submessage])
            messages.append(''.join(current_message))
        all_messages[sender] = messages
    return all_messages


def _get_message_prefix(recipient_addr):
    """
    Get prefix message number so messages can be ordered

    Args: 
        recipient_addr (str): address of user to send message to

    Returns:
        prefix (str): string of len 1.  Index of message
    """
    fname = "{dir}sent/{name}.txt".format(dir=settings.user_dir,
                                          name=recipient_addr)
    if not os.path.isfile(fname):
        return 'a'
    num_sent = sum(1 for line in open(fname))
    return chr(97 + num_sent)
