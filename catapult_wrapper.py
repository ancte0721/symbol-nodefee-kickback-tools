import datetime
import time
import urllib.request
import json
import sha3
from binascii import unhexlify, hexlify
from symbolchain.core.CryptoTypes import PrivateKey, PublicKey, Hash256
from symbolchain.core.sym.KeyPair import KeyPair
from symbolchain.core.facade.SymFacade import SymFacade
from symbolchain.core.sym.MerkleHashBuilder import MerkleHashBuilder

class CatapultWrapper:
    """
    <class CatapultWrapper>
    APIやSDKを使いやすくするためのラッパークラス
    """

    def __init__(self, nettype, setting):
        self.setting = setting
        self.facade = SymFacade(nettype)
        self.keypair = KeyPair(PrivateKey(unhexlify(setting.private_key)))
        self.address = self.facade.network.public_key_to_address(self.keypair.public_key)
        self.hexaddress = self.get_hexaddress(self.address)

    # 16進数アドレス取得
    def get_hexaddress(self, address):
        req = urllib.request.Request(self.setting.nodeurl + '/accounts/' + str(address))
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
        return str(data['account']['address'])

    # ハーベスター一覧取得
    def get_harvesters(self):
        harvesters = []
        req = urllib.request.Request(self.setting.nodeurl + '/node/unlockedaccount')
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
        for linkkey in data['unlockedAccount']:
            time.sleep(0.5)
            # リンク元の公開鍵を取得
            req = urllib.request.Request(self.setting.nodeurl + '/accounts/' + str(linkkey))
            with urllib.request.urlopen(req) as res:
                data = json.load(res)
            harvesters.append(str(data['account']['supplementalPublicKeys']['linked']['publicKey']))
        return harvesters
        
    # 公開鍵からアドレスへの変換
    def get_publickey2address(self, plist):
        return list(map(lambda x: str(self.facade.network.public_key_to_address(PublicKey(unhexlify(x)))), plist))

    # ハーベスターの16進数アドレス取得
    def get_harvesters_hexaddress(self, harvesters_address):
        address = {}
        for a in harvesters_address:
            time.sleep(0.5)
            address[self.get_hexaddress(a)] = a
        return address

    # 指定ブロック以降のハーベスト取得
    def get_harvests(self):
        params = {
            'targetAddress': self.address,
            'receiptType': self.setting.HARVEST_ENUM,
            'fromHeight': self.setting.from_height,
            'order': 'desc',
            'pageSize': 100,
            'pageNumber': 1
        }
        if self.setting.to_height > 0:
            params['toHeight'] = self.setting.to_height
        req = urllib.request.Request('{}?{}'.format(self.setting.nodeurl + '/statements/transaction', urllib.parse.urlencode(params)))
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
        return data

    # トランザクション作成
    def create_tx(self, address, amount, message):
        tx = self.facade.transaction_factory.create_embedded({
            'type': 'transfer',
            'signer_public_key': self.keypair.public_key,
            'recipient_address': SymFacade.Address(address),
            'mosaics': [(self.setting.MOSAIC_ID, amount)],
            'message': bytes(1) + message.encode('utf8')
        })
        return tx

    # アグリゲートトランザクション作成
    def create_aggregatetx(self, tx_lst):
        # マークルハッシュの作成
        hash_builder = MerkleHashBuilder()
        for tx in tx_lst:
            hash_builder.update(Hash256(sha3.sha3_256(tx.serialize()).digest()))
        merkle_hash = hash_builder.final()
        # アグリゲートトランザクションの有効期限
        deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=self.setting.exp_time)).timestamp()) - self.setting.BIRTHTIME) * 1000
        # アグリゲートコンプリートの作成
        aggregate = self.facade.transaction_factory.create({
            'type': 'aggregateComplete',
            'signer_public_key': self.keypair.public_key,
            'fee': int(self.setting.max_txfee *1000000),
            'deadline': deadline,
            'transactions_hash': merkle_hash,
            'transactions': tx_lst
        })
        # 自己署名
        signature = self.facade.sign_transaction(self.keypair, aggregate)
        aggregate.signature = signature.bytes
        return aggregate

    # アグリゲートトランザクションの送信
    def publish_tx(self, aggregatetx):
        # ノードへアナウンス
        payload = {"payload": hexlify(aggregatetx.serialize()).decode('utf8').upper()}
        req = urllib.request.Request(self.setting.nodeurl + "/transactions",
                                     json.dumps(payload).encode(),
                                     {'Content-type': 'application/json'},
                                     method='PUT')
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
        return data
