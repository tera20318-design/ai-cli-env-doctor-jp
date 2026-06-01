# ai-cli-env-doctor-jp

日本語で読める、AI/CLI開発環境向けのローカル診断CLIです。

`git`、Python、Node.js / `npm`、`uv`、Codex CLI、PowerShell、`PATH` のよくある詰まりどころを読み取り専用で確認し、原因の見当と次の確認手順を日本語で表示します。

このプロジェクトは新しいOSSです。stars、downloads、外部採用事例などの実績はまだありません。

## Features

- Python 3.10+ で動作
- ランタイム依存は Python 標準ライブラリのみ
- 日本語のテキスト出力
- `--json` による機械可読な出力
- `--check` による個別チェック実行
- `--strict` によるCI向け終了コード制御
- 診断は読み取り専用で、設定ファイルや `PATH` を変更しません

## Implemented Checks

v0.1.0 で実装済みのチェック:

- `python`: 実行中のPythonバージョンとPythonコマンド
- `git`: `git --version`
- `node`: `node --version` と `npm --version`
- `uv`: `uv --version`
- `codex`: Codex CLIの検出と `--version`
- `powershell`: PowerShell検出と実行ポリシー確認
- `path`: `PATH` の空エントリ、重複、存在しないディレクトリの数

Windowsでは `npm.cmd` / `codex.cmd` を優先して検出します。PowerShellの実行ポリシーで `.ps1` shim が止まるケースを避けるためです。

## Installation

まだPyPIには公開していません。GitHubから取得してローカルインストールできます。

```bash
git clone https://github.com/tera20318-design/ai-cli-env-doctor-jp.git
cd ai-cli-env-doctor-jp
python -m pip install .
```

開発用ツールも入れる場合:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

全チェックを実行:

```bash
ai-cli-env-doctor-jp
```

Pythonだけ確認:

```bash
ai-cli-env-doctor-jp --check python
```

JSONで出力:

```bash
ai-cli-env-doctor-jp --json
```

サニタイズ済みJSON例は [examples/sample-output.json](examples/sample-output.json) にあります。

警告、エラー、未検出があると終了コード1にする:

```bash
ai-cli-env-doctor-jp --strict
```

`--strict` は警告、エラー、未検出があると終了コード `1` を返します。`uv` や Codex CLI のような任意ツールを全ての環境で必須にしたくない場合は、CIで必要なチェックだけを指定してください。

```bash
ai-cli-env-doctor-jp --strict --check python --check git --check node
```

`python -m` でも実行できます。

```bash
python -m ai_cli_env_doctor_jp --check python
```

## Exit Codes

- 通常実行では、診断結果に警告、エラー、未検出が含まれていても、レポートを表示できれば終了コード `0` を返します。
- `--strict` を付けると、選択したチェックのいずれかが `warning`、`error`、`not_found` の場合に終了コード `1` を返します。
- 未知のチェック名や不正なオプションなど、引数エラーは `argparse` の標準挙動に従います。
- `uv` や Codex CLI を必須にしたくないCIでは、`--check` で必要な項目だけを選んでください。

## Example Output

```text
AI CLI Env Doctor JP
ローカル環境の読み取り専用診断結果です。
共有前に、出力内のローカルパスやユーザー名を確認してください。

Summary: OK=1 警告=0 エラー=0 未検出=0 不明=0

[OK] Python
  概要: 実行中の Python は 3.12.0 です。
  検出情報:
    - current_executable: C:/Python312/python.exe
    - current_version: 3.12.0
  次の一手:
    - この項目は対応不要です。
```

## Privacy And Security

- テレメトリはありません。
- 外部サービスへ診断結果を送信しません。
- 通常診断ではユーザー設定、シェルプロファイル、レジストリ、`PATH`、パッケージ設定を書き換えません。
- このCLIは `PATH` 上で見つかった `python`、`git`、`node` などのバージョン確認コマンドを実行します。信頼できない作業環境や汚染された `PATH` では実行しないでください。
- `PATH` チェックは件数を中心に表示し、全内容のダンプはしません。
- 出力時にホームディレクトリ、OpenAI/GitHub/GitLab/npm/AWS形式の一部、`TOKEN` / `API_KEY` などの一部をベストエフォートで伏せ字にします。
- 出力をIssueなどに貼る前に、ローカルパスやユーザー名が残っていないか確認してください。
- 将来もし自動修復機能を追加する場合は、明示的なopt-in機能として分けます。

## Threat Model And Limitations

- このCLIはローカルの開発者支援ツールです。マルウェア対策、完全な秘密情報検出、またはサンドボックスを目的としていません。
- 読み取り専用の設計ですが、バージョン確認のために `PATH` 上のコマンドを実行します。攻撃者が `PATH` を差し替えられる環境では使わないでください。
- 伏せ字処理はベストエフォートです。未知のトークン形式、ツール固有のエラーメッセージ、ユーザー名、ホスト名、ローカルパスが残る可能性があります。
- ネットワーク上の最新バージョン確認、外部アップロード、自動修復は v0.1.0 の対象外です。
- READMEに書かれている機能だけが現在の実装範囲です。PyPI公開、採用実績、外部利用実績はまだありません。

## Architecture Notes

- 各診断は `src/ai_cli_env_doctor_jp/checks/` の小さな関数に分けています。
- 診断結果は `CheckResult` と `Evidence` に正規化し、テキスト出力とJSON出力の両方で同じデータを使います。
- 出力直前に `report.py` でベストエフォートの伏せ字処理を行います。
- ランタイム依存を増やさず、Python標準ライブラリだけで動くことを v0.1.0 の制約にしています。

## Development

```bash
python -m pip install -e ".[dev]"
```

検証コマンド:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
```

## Roadmap

今後の候補は [docs/roadmap.md](docs/roadmap.md) に分離しています。申請前レビューの記録は [docs/review-log.md](docs/review-log.md) に残しています。READMEには、現在動く機能だけを書きます。

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) を読んでください。診断は読み取り専用、ランタイム依存は標準ライブラリのみ、出力は日本語を基本にします。

## License

MIT License. See [LICENSE](LICENSE).
