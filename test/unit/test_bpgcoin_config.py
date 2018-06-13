import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from bpgcoin_config import BPGCoinConfig


@pytest.fixture
def bpgcoin_conf(**kwargs):
    defaults = {
        'rpcuser': 'bpgcoinrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 19551,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    bpgcoin_config = bpgcoin_conf()
    creds = BPGCoinConfig.get_rpc_creds(bpgcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'bpgcoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 18551

    bpgcoin_config = bpgcoin_conf(rpcpassword='s00pers33kr1t', rpcport=76761)
    creds = BPGCoinConfig.get_rpc_creds(bpgcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'bpgcoinrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 76761

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', bpgcoin_conf(), re.M)
    creds = BPGCoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'bpgcoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 17551


# ensure bpgcoin network (mainnet, testnet) matches that specified in config
# requires running bpgcoind on whatever port specified...
#
# This is more of a bpgcoind/jsonrpc test than a config test...
