#!/bin/bash
set -evx

mkdir ~/.bpgcoin

# safety check
if [ ! -f ~/.bpgcoin/.bpgcoin.conf ]; then
  cp share/bpgcoin.conf.example ~/.bpgcoin/bpgcoin.conf
fi
