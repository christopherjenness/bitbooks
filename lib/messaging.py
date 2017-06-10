import books
import bitcoin

def encode_message(message, counter):
    scripts = []
    messages = [message[i:i+30] for i in range(0, len(message), 30)]
    partition_counter = 'a'
    for partition in messages:
        partition = counter + partition_counter + partition
        messagelen = format(len(partition), 'x').rjust(2, '0')
        ID = binascii.hexlify(str(partition))
        script = "6a" + messagelen + ID
        scripts.append(script)
        parition_counter = chr(ord(partition_counter) + 1)
    return scripts


def send_message(recipient_addr, scripts, fee=0, send=False):
    priv, pub, addr = books.read_wallet()
    for script in scripts:
        outputs = [{'value': 546, 'address': recipient_addr}]
        inputs = bitcoin.history(addr)
        outputs.append({'value': 0, 'script': script})
        fee = fee
        tx = bitcoin.mksend(inputs[0], outputs, addr, fee)
        signed_tx = bitcoin.sign(tx, 0, priv)
        if send:
            bitcoin.pushtx(signed_tx)
        print signed_tx
        print ''
    return signed_tx

message = 'This is a test message.  I am going to span two txs'
scripts = encode_message(message, counter='a')
send_message(MARKET_ADDRESS, scripts)


