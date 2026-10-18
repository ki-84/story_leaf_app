# Story Leaf の多読向け検索・掲載方針

2026-10-18 調査・反映。日本語の「英語多読」に相当する学習法を探す人と、
理解できる英語のインプットを増やしたい人に、アプリの目的が伝わる名前・説明を使う。
この方針はHPと**今後のApp Store掲載文**の両方に適用する。

## 学習法を正しく説明する

Extensive Reading（ER）は、理解しやすく興味を持てる本を、意味を楽しみながら
たくさん読むアプローチ。難しい本の逐語訳や速読競争として説明しない。
読みやすい本を選び、頻繁な辞書確認で流れを止めず、合わない本は替え、自分のペースで続ける。
辞書は必要なときの補助、朗読は読む・聴く機会を支える機能として紹介する。

Comprehensible Input は理解できる言語への接触を指す、より広い概念。
読むことと聴くことの両方を含み、ERの別名として扱わない。
必ず話せる、暗記も練習も不要、特定期間で上達する、といった効果を約束しない。

根拠:

- [Extensive Reading Foundation: What is ER?](https://erfoundation.org/wordpress/what_is/)
- [ERFの各言語版ガイド](https://erfoundation.org/wordpress/guides/)
- [SSS: 英語多読と多読三原則](https://www.seg.co.jp/sss/learning/)
- [Stephen Krashen: The Case for Comprehensible Input](https://www.sdkrashen.com/content/articles/case_for_comprehensible_input.pdf)

## 各言語の呼び方と掲載位置

確認済みの語と名前・サブタイトルは [data/discovery.json](data/discovery.json) に保持する。
用語の存在は確認済みだが、国ごとの検索量・人気順位を測定したものではない。
特定の国で唯一の呼び方、最多検索語などとは表現しない。
中国語の簡体字・繁体字は表記と使用例に合わせて分ける。

| HPロケール | 主な学習法名 | 用例の一次資料 |
| --- | --- | --- |
| ja | 英語多読・多聴 / 多読 | [SSS](https://www.seg.co.jp/sss/learning/) |
| en | Extensive Reading | [ERF](https://erfoundation.org/wordpress/what_is/) |
| de | Extensives Lesen | [ウィーン大学](https://ucrisportal.univie.ac.at/de/publications/extensives-lesen-im-daf-unterricht-der-sekundarstufe-eine-interve/) |
| fr | Lecture extensive | [ポワティエ大学](https://formations.univ-poitiers.fr/plugins/odf-web/odf/_content/course-renforcement-d-anglais-cmi-s2-fr-fr-fr-fr-fr-fr/Renforcement%20en%20anglais%20CMI-1%20%28S2%29.pdf) |
| es | Lectura extensiva | [ERFスペイン語ガイド](https://erfoundation.org/guide/ERF_Guide-Sp.pdf) |
| it | Lettura estensiva | [ペルージャ外国人大学](https://ricerca.unistrapg.it/handle/20.500.12071/31646) |
| nl | Extensief lezen | [SLO・オランダ教育課程開発機関](https://www.slo.nl/thema/meer/tule/engels/kerndoel-13/?mode=toelichting-en-verantwoording) |
| pt-BR / pt-PT | Leitura extensiva | [ERFポルトガル語ガイド](https://erfoundation.org/guide/ERF_Guide_Portuguese.pdf) |
| ru | Экстенсивное чтение | [ウラル連邦大学研究者の論文](https://www.gramota.net/article/ped20250157/fulltext) |
| uk | Екстенсивне читання | [ウーマニ国立教育大学](https://znp.udpu.edu.ua/article/view/134426) |
| pl | Czytanie ekstensywne | [外国語教育誌JOwS](https://jows.pl/artykuly/jak-tworczo-wykorzystac-czytanie) |
| tr | Kapsamlı okuma | [ERFトルコ語ガイド](https://erfoundation.org/guide/ERF_Guide_Turkish.pdf) |
| ar | القراءة الموسعة | [ERFアラビア語ガイド](https://erfoundation.org/guide/Arabic_guide.pdf) |
| hi | विस्तृत पठन | [IGNOU教材](https://egyankosh.ac.in/bitstream/123456789/7681/1/Unit-2.pdf) |
| ko | 영어 다독 / 다독 | [鮮文大学](https://language.sunmoon.ac.kr/language/cm/cntnts/cntntsView.do?cntntsId=239348&mi=41128) |
| zh-Hans | 英语泛读 | [江南大学](https://dletc.jiangnan.edu.cn/syjx/kcdg/yyfd.htm) |
| zh-Hant | 英文廣讀 / 廣泛閱讀 / 英語泛讀 | [桃園市教育輔導團](https://ceag.tyc.edu.tw/act-3-info.aspx?d=74C53D32F8EF7558) |
| th | การอ่านแบบกว้างขวาง | [チュラロンコン大学](https://digital.car.chula.ac.th/chulaetd/4920/) |
| vi | Đọc mở rộng | [ホーチミン市教育大学誌](https://journal.hcmue.edu.vn/index.php/hcmuejos/article/view/5826) |
| id | Membaca ekstensif | [ERFインドネシア語ガイド](https://erfoundation.org/guide/ERF_Guide_Indonesian.pdf) |
| ms | Bacaan ekstensif | [Institut Pendidikan Guru Kampus Kent教材](https://ipkent.edu.my/document/pskent/pskent18/modul/bmm/BMM3043.pdf) |

## HP

- ページタイトルに現地の学習法名と英語学習であることを明記する。
- H1・導入文にも自然な形で目的を示す。キーワードを羅列した見出しにはしない。
- 各言語のFAQに、ERとComprehensible Inputの違い・始め方を掲載する。
- 説明文、OGP、構造化データも実際のページ内容と一致させる。
- 各言語の静的HTML、canonical、相互hreflang、サイトマップを維持する。
- 検索順位・クリック数・インデックス登録を保証したとは報告しない。
  公開反映と検索エンジンによるクロール・表示を区別する。

参照:
[Googleのタイトルリンク](https://developers.google.com/search/docs/appearance/title-link)、
[スニペット](https://developers.google.com/search/docs/appearance/snippet)、
[多言語ページ](https://developers.google.com/search/docs/specialty/international/localized-versions)。

## 次回以降のApp Store掲載文

- 文言の正本はアプリリポジトリの `app/fastlane/metadata_src/*.json`。
  生成先のtxtだけを直接編集しない。
- 名前かサブタイトルの目立つ位置に、現地のER用語を含める。
  名前に収まらないロシア語・ウクライナ語・ポーランド語・タイ語はサブタイトルを使う。
- 名前・サブタイトルは各30文字以内。プロモーション文は170文字以内、説明は4000文字以内。
- keywordsは関連語のみ。100文字に加え、App Store Connectの参照に合わせて
  UTF-8で100バイト以内にも収める。ブランド名の重複、競合名、無関係な集客語を入れない。
- 説明の冒頭に「やさしい英語をたくさん読む・聴く」用途を明記する。
  プロモーション文や説明に単語を詰めるだけでApp Store検索が改善するとは扱わない。
- 英語圏では `Extensive Reading` を名前、`Comprehensible input` をサブタイトルに配置する。
  他言語でも関連語としてComprehensible Inputを説明し、正式なER用語を補う。
- 現在の収録冊数・機能・広告条件・リリースノートなどの事実は維持する。
  アプリ独自のレベル分けを、CEFRやERFの公式認定レベルだと表現しない。
- `python3 app/fastlane/build_metadata.py` で生成し、全22言語の長さ・内容を確認する。
  掲載文ファイルの更新とApp Store Connectへのアップロードは別の操作。

Appleの一次資料:
[名前・サブタイトルの制限](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information)、
[キーワード・説明の参照](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information)、
[検索とプロダクトページ](https://developer.apple.com/app-store/product-page/)。
