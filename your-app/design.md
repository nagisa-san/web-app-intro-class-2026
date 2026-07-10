# 私のアプリ設計

## 1. 題材
行きたい店と、特徴を記録するアプリ

## 2. テーブル設計 
テーブル名：shops
カラム：id / name(店名) / visited(訪問済み 0 or 1)

## 3. 変換表
todos → shops, title → name, done → visited, todo.db → shops.db, /todos → /shops