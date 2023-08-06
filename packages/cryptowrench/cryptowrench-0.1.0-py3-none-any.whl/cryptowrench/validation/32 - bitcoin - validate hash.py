from hashlib import sha256
from binascii import unhexlify
import requests, datetime as dt

def littleEndian(hex_str):
    aux = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    aux.reverse()
    return ''.join(aux)

def get_seconds_since_1970(datetime_str):
    date = dt.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    date_1970 = dt.datetime(1970, 1, 1, 0, 0, 0)
    return int((date-date_1970).total_seconds())

def get_target_from_nBits(nBits):
    target_packed = hex(nBits)[2:]
    target_first_two_bytes = int(target_packed[:2], 16)
    target_rest = int(target_packed[2:], 16)
    return hex(target_rest*2**(8*(target_first_two_bytes-3)))

def get_hash_from_header(block_header_as_bin):
    iter_1 = sha256(header_bin).digest()
    iter_2 = sha256(iter_1).hexdigest()
    bigEndian = [iter_2[i:i+2] for i in range(0, len(iter_2), 2)]
    bigEndian.reverse()
    bigEndian = ''.join(bigEndian)
    return hex(int(bigEndian, 16))

chain = 'main'
block_hash = '1'
url = f'https://api.blockcypher.com/v1/btc/{chain}/blocks/{block_hash}'

req = requests.get(url)
if req.status_code == 200:
    res = req.json()

    version = littleEndian(hex(res['ver'])[2:].zfill(8))
    # version = str(res['ver'])
    hashPrevBlock = littleEndian(res['prev_block'])
    hashMerkleRoot = littleEndian(res['mrkl_root'])
    time  = littleEndian(hex(get_seconds_since_1970(res['time']))[2:])
    bits  = littleEndian(hex(res['bits'])[2:])
    nonce = littleEndian(hex(res['nonce'])[2:])

    header_hex = version + hashPrevBlock + hashMerkleRoot + time + bits + nonce
    header_bin = unhexlify(header_hex)

    calculated_hash = get_hash_from_header(header_bin)
    
    target = get_target_from_nBits(res['bits'])
    print('Target: ' + target)
    print('Nonce: ' + str(res['nonce']))
    print('Block hash: ' + str(calculated_hash))

    if calculated_hash < target:
        print('Block hash meets the target.')
    else:
        print('Block hash does not meet the target.')
else:
    print(res)