from configparser import ConfigParser

class Setting:
    """
    <class Setting>
    各種設定
    """

    def __init__(self, configfile):
        self.config = ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(configfile, 'UTF-8')
        self.dryrun = self.config.getboolean('Kickbacktools', 'dryrun')
        self.nodeurl = self.config.get('Kickbacktools', 'node')
        self.private_key = self.config.get('Kickbacktools', 'private_key')
        self.message = self.config.get('Kickbacktools', 'message')
        self.exp_time = self.config.getint('Kickbacktools', 'exp_time')
        self.from_height = self.config.getint('Kickbacktools', 'from_block_height')
        self.to_height = self.config.getint('Kickbacktools', 'to_block_height')
        self.autoupdate = self.config.getboolean('Kickbacktools', 'autoupdate_from_block_height')
        self.kickback_rate = self.config.getfloat('Kickbacktools', 'kickback_rate')
        self.fixed_kickback = self.config.getfloat('Kickbacktools', 'fixed_kickback')
        self.limit_xym_amount = self.config.getfloat('Kickbacktools', 'limit_xym_amount')
        self.max_txfee = self.config.getfloat('Kickbacktools', 'max_txfee')
        # 定数
        self.HARVEST_ENUM = int(self.config.get('Kickbacktools', 'receipt_type_enum'), 0)
        self.BIRTHTIME = self.config.getint('Kickbacktools', 'birth_time')
        self.MOSAIC_ID = int(self.config.get('Kickbacktools', 'mosaic_id'), 0)
