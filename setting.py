from configparser import ConfigParser

class Setting:
    """
    <class Setting>
    各種設定
    """

    def __init__(self, configfile):
        config = ConfigParser()
        config.read(configfile, 'UTF-8')
        self.dryrun = config.getboolean('Kickbacktools', 'dryrun')
        self.nodeurl = config.get('Kickbacktools', 'node')
        self.private_key = config.get('Kickbacktools', 'private_key')
        self.message = config.get('Kickbacktools', 'message')
        self.exp_time = config.getint('Kickbacktools', 'exp_time')
        self.from_height = config.getint('Kickbacktools', 'from_block_height')
        self.to_height = config.getint('Kickbacktools', 'to_block_height')
        self.kickback_rate = config.getfloat('Kickbacktools', 'kickback_rate')
        self.fixed_kickback = config.getfloat('Kickbacktools', 'fixed_kickback')
        self.limit_xym_amount = config.getfloat('Kickbacktools', 'limit_xym_amount')
        self.max_txfee = config.getfloat('Kickbacktools', 'max_txfee')
        # 定数
        self.HARVEST_ENUM = int(config.get('Kickbacktools', 'receipt_type_enum'), 0)
        self.BIRTHTIME = config.getint('Kickbacktools', 'birth_time')
        self.MOSAIC_ID = int(config.get('Kickbacktools', 'mosaic_id'), 0)
