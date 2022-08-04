# 概要

PATLITE製インターフェースコンバータ[PHE-3FB2](https://www.patlite.jp/product/phe_3fb2.html) のサンプルプログラム。

# 使用モジュール

## argparse

UNIXライクのコマンドラインオプションパーサー。Python標準ライブラリ。

## configparser

INIファイルから値を読み込む。Python標準ライブラリ。

## PySerial

シリアル通信モジュール。詳細は[公式サイト](https://pyserial.readthedocs.io/en/latest/)を参照。

## PyInstaller

pythonスクリプトをexe化するモジュール。詳細は[公式サイト](https://pyinstaller.org/en/stable/)を参照。

起動にはDLLが必要になる。onefileオプションを使用することで、DLLを含めたexe化が可能。

```
> pyinstaller [ファイル名.py] --onefile
```
