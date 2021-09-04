import sys
from logging import getLogger, FileHandler, Formatter, StreamHandler, DEBUG
import datetime
from setting import Setting
from catapult_wrapper import CatapultWrapper

"""
ハーベスト手数料をハーベスターに還元するノード運営者向けツール
./config.iniにて各種設定を行った後に実行してください
"""

def main():
    # ログ設定
    logger = getLogger(__name__)
    handler = FileHandler(filename="logs/{}.log".format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
    handler2 = StreamHandler(sys.stdout)
    handler2.setLevel(DEBUG)
    handler2.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler)
    logger.addHandler(handler2)
    logger.setLevel(DEBUG)

    setting = Setting("./config.ini")
    cw = CatapultWrapper('public', setting)
    logger.info("My public key: "+ str(cw.keypair.public_key))
    logger.info("My wallet address: "+ str(cw.address))

    # ハーベスターの数によって少々時間が掛かります
    harvesters_publickeys = cw.get_harvesters()
    harvesters_address = cw.get_publickey2address(harvesters_publickeys)
    logger.info("Harvesters address: "+ str(len(harvesters_address)))

    harvesters_hexaddress = cw.get_harvesters_hexaddress(harvesters_address)
    # 自身のアドレスは削除
    harvesters_hexaddress.pop(str(cw.hexaddress))
    harvests = cw.get_harvests()

    logger.info("Harvest history from height: " + str(setting.from_height))
    logger.info("Harvest history to height: " + str(setting.to_height))
    logger.info("### block height, harvest address, node fee amount ###")
    kickback_list = []
    for h in harvests['data']:
        height = h['statement']['height']
        receipts = h['statement']['receipts']
        for r in receipts:
            # ハーベスト詳細に絞る
            if int(r['mosaicId'], 16) != setting.MOSAIC_ID or r['type'] != setting.HARVEST_ENUM:
                continue
            # ハーベスター
            if r['targetAddress'] in harvesters_hexaddress:
                harvester_address = harvesters_hexaddress[r['targetAddress']]
            # ノード手数料
            if r['targetAddress'] == str(cw.hexaddress):
                fee_amount = r['amount']
        kickback_list.append([height, harvester_address, fee_amount])
        logger.info(str([height, harvester_address, str(int(fee_amount)/1000000)]))

    logger.info("Kickback transactions")
    logger.info("### target address, XYM amount, message ###")
    # トランザクションリスト作成
    tx_lst = []
    highest_block = 0
    for item in kickback_list:
        xym_amount = int(setting.fixed_kickback * 1000000) if setting.fixed_kickback > 0 else int(int(item[2]) * setting.kickback_rate)
        message = setting.message.replace("#BLOCK#", str(item[0]))
        if highest_block < int(item[0]):
            highest_block = int(item[0])
        logger.info(str([item[1], xym_amount/1000000, message]))
        # limit確認
        if setting.limit_xym_amount <= xym_amount/1000000:
            logger.error("XYM Limit over (config.ini -> limit_xym_amount)")
            raise Exception("制限を超えた送金を検知しました、送金処理を中断します")
        tx_lst.append(cw.create_tx(item[1], xym_amount, message))
    logger.info("Total transfer XYM amount: {} + {}(Max fee)".format(str(sum(map(lambda tx: tx.mosaics[0][1], tx_lst)) / 1000000), setting.max_txfee))

    # 送金対象が0件
    if len(tx_lst) <=0:
        logger.info("There is no transfer")
        raise Exception("送金対象がありません、送金処理を終了します")

    # ドライランモード
    if setting.dryrun:
        logger.info("ドライランのため送金を行わずに処理を終了します (config.ini -> dryrun)")
    else:
        aggregate_tx = cw.create_aggregatetx(tx_lst)
        # アグリゲートトランザクションのハッシュ値
        tx_hash = cw.facade.hash_transaction(aggregate_tx)
        logger.info("Transaction hash: "+ str(tx_hash))
        cw.publish_tx(aggregate_tx)
        logger.info("Published : http://explorer.symbolblockchain.io/transactions/"+ str(tx_hash))
        if setting.autoupdate:
            setting.config['Kickbacktools']['from_block_height'] = str(highest_block +1)
            with open("./config.ini", 'w', encoding='utf-8') as configfile:
                setting.config.write(configfile)
            logger.info("from_block_height update to " + str(highest_block +1))
        logger.info("Node fee kickback is completed")



if __name__ == "__main__":
    main()
