# 自動運転ミニカーチャレンジ Team 10

## 概要
このプロジェクトは、既存のRC車を改造してDonkey Carとして動作させるためのプロジェクトです。ラズパイ上で開発し、GitHubで管理する共同開発プロジェクトです。

### プロジェクトの目的
- 既存のRC車のハードウェア（ESC、サーボ）をDonkey Carで使用可能にする
- カスタムハードウェアに合わせたPWM値の探索と設定
- Donkey Carフレームワークを使用した自律走行の実現

### 主な特徴
- カスタムESCとサーボのPWM値の探索ツール（`motor_esc_test.py`, `servo_test.py`）
- PCA9685を使用したPWM制御
- Donkey Car標準構成（`mycar/`ディレクトリ）との統合

## 開発環境セットアップ

### 1. 必要なもの

#### ソフトウェア
- Cursor（VS Codeベースのエディタ）
- GitHubアカウント
- ラズパイへのSSHアクセス権限
- ラズパイとPCが同じネットワークに接続されていること（ラズパイはLANケーブル接続）

#### ハードウェア
- Raspberry Pi（I2C対応）
- PCA9685（16チャンネルPWMドライバ）
- ESC（電子速度制御器）
- サーボモーター（ステアリング用）
- RC車のシャーシ

### 2. Cursorでラズパイに接続

#### Remote-SSH拡張機能のインストール
1. Cursorを開く
2. 左サイドバーの拡張機能アイコンをクリック
3. 「Remote - SSH」を検索してインストール

#### ラズパイへの接続
1. Cursorのウェルカム画面で「Connect via SSH」をクリック
2. 接続先を入力: `koito@192.168.50.3`
3. パスワードを入力
4. 「Open Folder」で作業フォルダを開く（例: `/home/koito/プロジェクト名`）

### 3. 共同作業者のセットアップ

#### GitHubでコラボレーター追加（プロジェクトオーナー）
1. GitHubのリポジトリページ → Settings → Collaborators
2. 「Add people」で共同作業者を招待

#### プロジェクトのクローン（共同作業者）
```bash
# リポジトリをクローン
git clone https://github.com/ユーザー名/リポジトリ名.git

# フォルダに移動
cd リポジトリ名
```

または、Cursorの「Clone repo」から直接クローン可能

## 日常的な作業フロー

### 作業を始める前（必須）
```bash
# 最新の変更を取得
git pull
```

### コードを編集したら
```bash
# 変更をステージング
git add .

# コミット（変更内容を簡潔に説明）
git commit -m "機能追加: ○○機能を実装"

# GitHubにプッシュ
git push
```

### ブランチを使った作業（推奨）
```bash
# 新しいブランチを作成して切り替え
git checkout -b feature/新機能名

# 作業してコミット
git add .
git commit -m "新機能を追加"

# ブランチをプッシュ
git push origin feature/新機能名
```

その後、GitHubでPull Request（PR）を作成してレビュー・マージ

## Cursorの設定

### Claudeモデルの設定
1. Cursor右下の歯車アイコン → Settings
2. 「Models」タブ
3. 好みのClaudeモデルを選択

### 便利な機能
- **Composer**: `Cmd + I` でAI支援コーディング
- **Chat**: サイドバーでコードについて質問
- **ターミナル**: `Ctrl + ` でターミナルを開く

## よくある問題と解決方法

### コンフリクト（競合）が発生した場合
```bash
# 最新の変更を取得
git pull

# コンフリクトを手動で解決（Cursorのエディタで表示される）
# 解決後
git add .
git commit -m "コンフリクトを解決"
git push
```

### ラズパイのIPアドレスを確認
```bash
hostname -I
```

### SSH接続が切れた場合
Cursorの左下に表示されている接続状態をクリックして再接続

## プロジェクト構成
```
.
├── README.md
├── motor_esc_test.py    # ESC（駆動モーター）のPWM値探索ツール
├── servo_test.py        # サーボモーターのPWM値探索ツール
├── mycar/               # Donkey Carの標準構成
│   ├── config.py       # Donkey Carの設定ファイル
│   ├── myconfig.py     # カスタム設定ファイル
│   ├── manage.py       # Donkey Car管理スクリプト
│   ├── train.py        # 学習スクリプト
│   ├── calibrate.py    # キャリブレーションスクリプト
│   ├── data/           # 学習データ
│   ├── logs/           # ログファイル
│   └── models/         # 学習済みモデル
└── env/                # Python仮想環境
```

## テストツールの使い方

### motor_esc_test.py
ESC（駆動モーター）のニュートラル位置と前進・後退のPWM値を確認するツールです。

```bash
# 実行前に車輪を地面から離すこと
python3 motor_esc_test.py
```

**注意事項:**
- 実行前に必ず車輪を地面から離してください
- ESCの電源をONにしてください
- 見つけた値（STOP, FWD, REV）を`mycar/myconfig.py`に反映してください

### servo_test.py
サーボモーターのニュートラル位置と左右の限界位置を探索するツールです。

```bash
python3 servo_test.py
```

**使い方:**
1. インタラクティブにサーボの動作範囲を探索
2. 各ステップでEnterキーで続行、'n'で限界位置を設定
3. 見つけた値（LEFT, CENTER, RIGHT）を`mycar/myconfig.py`に反映してください

**注意事項:**
- 小さいPWM値（1000us付近）がRIGHT（右）
- 大きいPWM値（2000us付近）がLEFT（左）
- このプロジェクトのサーボは一般的な方向と逆になっています

## ハードウェア設定

### PCA9685の接続
- VCC → 5V
- GND → GND
- SCL → GPIO 3 (I2C Clock)
- SDA → GPIO 2 (I2C Data)

### ESCとサーボの接続
- ESC → PCA9685 チャンネル0
- サーボ → PCA9685 チャンネル1

### 見つけたPWM値の設定
`motor_esc_test.py`と`servo_test.py`で見つけた値を`mycar/myconfig.py`に設定してください。

例:
```python
# ESC設定
THROTTLE_STOPPED_PWM = 1500
THROTTLE_FORWARD_PWM = 1370
THROTTLE_REVERSE_PWM = 1610

# サーボ設定
STEERING_LEFT_PWM = 2000  # 実際の左方向のPWM値
STEERING_RIGHT_PWM = 1000  # 実際の右方向のPWM値
STEERING_CENTER_PWM = 1500  # ニュートラル位置のPWM値
```

## Donkey Carの使い方

### データ収集
```bash
cd mycar
python manage.py drive
```

### 学習
```bash
python train.py
```

### 自律走行
```bash
python manage.py drive --model models/your_model.h5
```

## トラブルシューティング

### I2Cデバイスが検出されない場合
```bash
# I2Cが有効か確認
lsmod | grep i2c

# I2Cデバイスを再スキャン
sudo i2cdetect -y 1
```

### PWM値が正しく動作しない場合
- `motor_esc_test.py`と`servo_test.py`で再度確認してください
- ESCやサーボの電源が正しく接続されているか確認してください
- PCA9685のI2Cアドレスが正しいか確認してください（通常は0x40）

## TODO

- [ ] Donkey Car myconfig.py調整して、ESCとサーボの閾値を反映する
- [ ] コントローラーで操作できるようにする
- [ ] 画面を見てもらうためにChrome Remote Desktopをインストール - あとで
- [ ] 近藤さんの機械学習ソフトの使い方をみる
- [ ] 超音波センサーのソフトをDonkey Carのパーツとして使えるようにする
  - [ ] GPIO確認- 配線
  - [ ] Donkey Carのフォルダに配置
- [ ] 超音波モードとカメラでの機械学習モードの切り替えを入れる

## ライセンス
[ライセンス名を記載]

## コントリビューター
- [名前1]
- [名前2]