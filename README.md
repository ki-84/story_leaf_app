# Story Leaf — promotional website

GitHub Pages: **https://ki-84.github.io/story_leaf_app/**

Story Leaf の宣伝サイト。サポートサイトは既存の
https://ki-84.github.io/story_leaf_support/en/ を維持します。

## 内容

- 公開作品は「The Little Wiggle Dance」「Half a Roll」「The Best Seat」の3冊のみ
- 各作品の冒頭4ページの試し読み、ページ別の英語朗読（全12ファイル）
- 公開中の App Store 掲載言語に合わせた22ロケール
- iPhone / iPad 向けの App Store 導線
- 各言語の静的HTML、canonical / hreflang、OGP、構造化データ、サイトマップ

3冊を共通の紹介エリアに並べ、PCは3列、スマートフォンは画像と紹介文の横並びにします。
CSS・JavaScriptは内容のハッシュを含むファイル名で出力し、更新前のデザインが
ブラウザーのキャッシュに残らないようにしています。

絵本本文と音声は英語のままです。紹介文、FAQ、操作、作品紹介は各言語で表示します。
ルートはブラウザー言語または保存済みの選択に振り分け、`/ja/` などの
直接指定したURLでは言語を自動変更しません。アラビア語はRTL表示です。
サポート・プライバシーポリシーへのリンクには英語ページである旨を表示しています。

## 編集・ビルド

Python 3.9 以降。通常のビルドに外部依存はありません。

```sh
python3 build.py
python3 verify.py
python3 -m http.server 4173 --directory public --bind 127.0.0.1
```

`http://localhost:4173/ja/` を開きます。

- `src/index.html` / `style.css` / `app.js`: 共通UI
- `locales/*.json`: ページ文言と作品ごとの紹介文
- `data/books.json`: 公開する3冊の抜粋。原本の本文・ページ順を維持
- `assets/books/`: 表紙と冒頭ページの軽量WebP
- `assets/audio/`: ページ単位のMP3。再生操作後だけ読み込み、ページ移動・閉じる操作で停止
- `data/audio-manifest.json`: 本文、音声SHA-256、生成設定、長さ
- `.github/workflows/pages.yml`: mainへのpushで検証後にGitHub Pagesへ公開

元のアプリ用リポジトリでは `marketing/website/` が正本です。
公開用リポジトリ `ki-84/story_leaf_app` にはこのディレクトリの内容だけを配置します。
アプリ本体・認証情報・音声モデルを公開用リポジトリに含めないでください。

## 書籍画像の更新（アプリ開発用チェックアウト内のみ）

Pillow が必要です。承認・配信済みの原本から抜粋します。

```sh
python3 prepare_assets.py
```

公開対象の追加はユーザーが指定した場合のみ。`build.py` の `PUBLIC_BOOK_IDS` と
`prepare_assets.py`、各言語の `summaries` を同じ順で更新します。
`verify.py` は、対象外の書籍画像・音声が配信フォルダに残っている場合も失敗します。
画像以外の元の書籍データは変更しません。

## 朗読音声の更新

アプリと同じ Supertonic 3 / F1 / 8 steps / speed 1.05 で生成。
モデルはローカルの `content/tts/supertonic` を利用し、HPにはMP3のみを配信します。
出力はAI合成音声であることをプレイヤー付近に明記しています。
声の合成に従量課金のAPIやマイク録音は使いません。

必要: numpy, onnxruntime, soundfile, ffmpeg、および公式MITヘルパー。

```sh
python3 generate_audio.py --helper /absolute/path/to/upstream/py/helper.py
python3 build.py
python3 verify.py
```

使用した公式ヘルパー:
https://github.com/supertone-oss-archive/supertonic/blob/main/py/helper.py

音声は公開するまでローカル生成のみで、ブラウザーでのリアルタイム合成は不要です。
音声入力が変わっていないページはマニフェストのハッシュで再生成を省略します。

## 公開

GitHub Pages の Source は **GitHub Actions**。
`main` へのpushで静的ページを生成・検証・デプロイします。
公開先を変える場合は `build.py` の `DEFAULT_URL` を変更してください。
App Store の Marketing URL は、公開確認後に言語別のURLへ更新できます。
このサイトの追加だけではApp Store Connectのメタデータは変更しません。

原作とスクリーンショット内の外部作品のクレジットは `LICENSE.txt` とサイト内で確認できます。
