# bitbooks

![travis](https://travis-ci.org/christopherjenness/bitbooks.svg?branch=master) [![Coverage Status](http://coveralls.io/repos/github/christopherjenness/bitbooks/badge.svg?branch=master)](https://coveralls.io/github/christopherjenness/bitbooks?branch=master)

A decentralized, uncensorable marketplace for books.

## Overview

[Governments have a hisotry of banning books.](https://en.wikipedia.org/wiki/List_of_books_banned_by_governments) Here, we provide a tool to buy and sell books in a decentralized, unsensorable manner.

## Details

Decentralized marketplaces have previously utilized immutable decentralized blockchains as databases.  Unfortunately, the cost of writing to these immutable decentralized databases has increased dramatically, making these approaches impractical.

Instead of writing to immutable blockchains, bitbooks uses the blockchain mempool to buy and sell books.  It does not cost anything to send data to the blockchain mempool.

Mempool transactions are immutable and distributed for days.  After the data is removed from the mempool, the data can be trivially rebroadcasted if desired.

Alternatively, bitbooks supports writing data into the blockchain if you wish to pay the miner fee. However, we do not see any reason to use this feature.

## Installation

`python setup.py install`

## Usage

To get your wallet:

`bitbooks wallet`

To check your balance (small amount needed for posting books for sale or sending messages):

`bitbooks balance`

To post a book for sale:

`bitbooks post` - You will be prompted for ISBN, quality, and price of your book

To cancel a book posting:

`bitbooks cancel` - You will be prompted for ISBN of book to cancel

To send a message:

`bitbooks sendmessage` - You will be prompted for senders address and your message

To check your messages:

`bitbooks checkmessages`

## Warnings

Your wallet is saved unencrypted on your hardrive.  Do not send more than is needed to this wallet.  10 cents should be sufficient for most uses. 

Messages are not encrypted.

## Tips

bitbooks does not depend on confirmed transactions.  That means you can load your wallet for free with unconfirmed transactions.
