# 記事スクレイピング研修用リポジトリ

当リポジトリは社内研修で使用しているものを社外にも公開したものです。

## 推奨環境
|環境     | バージョン |
| ------ | --------- |
|python  | 3.9       |
|node.js | 16.7.0    |
|pip3    | 22.0.4    |
|make    | 3.81      |

## 使い方（web）
初期設定
```bash
$ make install
```

サーバー起動
```bash
$ make up
```

サーバー更新
```bash
$ make reload
```

## 使い方(Cli)
5件のエクセルデータ取得する
```bash
$ python3 backend/scrape.py 5
```


10件のcsvデータ取得する
```bash
$ python3 backend/scrape.py 10 'csv'
```