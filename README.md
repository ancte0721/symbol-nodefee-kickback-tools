# symbol-nodefee-kickback-tools
ハーベスト報酬をハーベスターに還元するノード運営者向けツール

Qiitaに詳細な解説記事を用意しています
[[Symbol] ノード運営者向けハーベスト還元ツールを開発しました](https://qiita.com/nobu_kyutech/items/b77164b77691a76c3b31)

[In english](./README_EN.md)

# Features
- 指定範囲のブロック高でハーベストしたアドレスへの送金
- 送金額に関して、ノード報酬に対する割合、または絶対値を任意に設定可能
- 送金あたりの限度額が設定でき、その金額以上の送金をプログラムが行おうとした場合、送金作業を停止
- 実際には送金しないが、どのアドレスにいくら送金するか事前に確認できるドライラン機能

# Requirement
Python 3.7 later
 * symbol-sdk-core-python 1.0.0

# Installation
```
cp config.ini.example config.ini
```

config.iniの内容を自分の環境や行いたい還元ルールに沿って編集してください

# Usage
```
python nodefee-kickback.py
```
実行毎にlogsディレクトリにログファイルが出力されます

# Note
- 初回は必ずドライランモード（dryrun = True）にて動作や送金額を確認してから実施してください
- 秘密鍵の流出（config.iniファイルの流出）には注意してください
- 本プログラムを利用したことで発生した損害について、作者はいかなる責任も負いません

# License
[MIT License](./LICENSE)
