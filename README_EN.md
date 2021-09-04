# symbol-nodefee-kickback-tools
A tool for node operators that returns harvest fees to harvesters

[In japanese](./README.md)

# Features
- Remittance to the address harvested with the specified block height
- Regarding the remittance amount, the ratio to the node fee or the absolute value can be set arbitrarily
- You can set a limit per remittance, and if the program tries to remit more than that amount, the remittance work will be stopped
- Dry run function that allows you to check in advance how much money will be sent to which address, although it will not actually be sent

# Requirement
Python 3.7 later
 * symbol-sdk-core-python 1.0.0

# Installation
```
cp config.ini.example config.ini
```

Edit the contents of config.ini according to your environment and the return rules you want to do.

# Usage
```
python nodefee-kickback.py
```

# Note
- Be sure to check the operation and remittance amount in dryrun mode (dryrun = True) for the first time.
- Be careful about the leakage of the private key (the leakage of the config.ini file).
- The author does not take any responsibility for the damage caused by using this program.

# License
[MIT License](./LICENSE)
