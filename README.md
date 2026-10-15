# 伊良部語 使役・受動 調査ノート

調査員用ページ： https://michinorishimoji.github.io/causproject-questionnaire/

## 更新

`questionnaire-compact.html` と必要な `img/` 内の画像を編集し、`main` にプッシュすると、GitHub ActionsがGitHub Pagesを更新します。

```sh
git add questionnaire-compact.html img/
git commit -m "Update questionnaire"
git push
```

新しい画像を追加する場合は、`.gitignore` の画像許可リストにも追加してください。公開する画像だけを指定します。

公開処理の結果はリポジトリのActionsで確認できます。調査員は同じURLを再読み込みして最新版を開けます。

## 記録の保存

回答・メモ・優先度は各調査員のブラウザに自動保存されます。GitHubには送信されず、他の端末とは同期されません。調査後は「バックアップ保存」でJSONを保存し、必要に応じて担当者へ別途共有してください。CSVでも書き出せます。

ローカルHTMLのブラウザ保存と公開ページのブラウザ保存は別です。移行時は、ローカル版でバックアップを保存し、公開ページの「読み込み」で復元してください。

ブラウザで編集した例文や優先度はHTML本体には反映されません。全員共通の初期内容を変更するときはHTML本体を編集してプッシュします。既存の手入力は、ページ更新より優先して表示される場合があります。

## 公開対象

現在の調査票HTMLと、HTMLの画像一覧から参照される画像、および公開処理用のファイルのみです。原票PDF、Word文書、旧版HTML、作業用ファイル、回答バックアップは含めません。

画像は調査用にAIで生成した刺激です。伊良部語の候補には未確認の語彙・語形を含みます。

## 公開前の確認

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

ブラウザで http://localhost:8000/ を開きます。

## ブラウザで編集した最新版を配布する

「バックアップ保存」で保存したJSONから、例文・和訳・優先度・画像選択だけをHTML本体に取り込めます。回答、メモ、話者ID、日付、進捗は取り込みません。

```sh
python3 scripts/sync_questionnaire.py /path/to/backup.json
python3 scripts/build_site.py
git add questionnaire-compact.html
git commit -m "Update shared questionnaire settings"
git push
```

バックアップJSONそのものはリポジトリに追加しないでください。独自に追加したカードがある場合は、公開用の番号・内容を確認してから取り込みます。
