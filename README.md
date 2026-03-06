# Claude-Code

Claude Code を活用するためのプロジェクトテンプレートです。

## フォルダ構成

```
Claude-Code/
├── src/                  # ソースコード
│   ├── commands/         # カスタムスラッシュコマンド
│   ├── hooks/            # Claude Code フック設定
│   ├── tools/            # カスタムツール
│   └── utils/            # 共通ユーティリティ
├── docs/                 # ドキュメント
├── examples/             # 使用例・サンプルコード
├── tests/                # テストコード
└── .github/
    └── workflows/        # CI/CD ワークフロー
```

## 各フォルダの役割

| フォルダ | 説明 |
|---|---|
| `src/commands/` | Claude Code で使うカスタムスラッシュコマンドを置く場所 |
| `src/hooks/` | PreToolUse・PostToolUse などのフック設定ファイル |
| `src/tools/` | MCP サーバーやカスタムツールの実装 |
| `src/utils/` | 複数のモジュールで共有するユーティリティ関数 |
| `docs/` | 仕様書・設計ドキュメント・ガイド |
| `examples/` | 動作確認用のサンプルコード |
| `tests/` | 単体テスト・統合テスト |
| `.github/workflows/` | GitHub Actions の CI/CD 設定 |

## はじめ方

1. このリポジトリをクローン
2. 必要なフォルダにコードを追加
3. `src/hooks/` にフック設定を配置して Claude Code と連携
