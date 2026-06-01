# Contributing

このプロジェクトへの小さな改善は歓迎します。v0.1.xでは、診断項目の正確さ、テスト、READMEの実行可能性を優先します。

## Development Setup

```bash
python -m pip install -e ".[dev]"
```

## Checks Before PR

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
```

## Contribution Policy

- ランタイム依存はPython標準ライブラリのみを維持してください。
- 診断は読み取り専用にしてください。
- ユーザー向け出力は日本語を基本にしてください。
- 実装されていない機能をREADMEに書かないでください。
- stars、downloads、利用実績、採用事例を作らないでください。
- 申請や宣伝のために、実態より成熟しているように見せないでください。

## Adding A Check

1. `src/ai_cli_env_doctor_jp/checks/` に小さなモジュールを追加します。
2. `CheckResult` を返す `run()` を実装します。
3. 実機コマンドに依存しないユニットテストを追加します。
4. `README.md` のImplemented Checksに、実際に動く範囲だけ追記します。
