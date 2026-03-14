# X Runway

X Runway の目的は「自動拡散」ではなく、手動投稿で仮説検証するための配信パックをローカル生成することです。
X API / ブラウザ拡張 / 外部SaaS 連携は扱いません。

## 使い方

```bash
make x-assets
make x-pack CASE=high_bias_affiliate
make x-pack-all
make x-metrics-init
```

## 2週間の手動投稿プロトコル

1. `dist/x/<case>/thread.md` を手動で投稿（3〜4ポスト）。
2. 投稿URLと指標を `ops/x_metrics.csv` に追記。
3. 2週間で 3ケース × 3角度（BLOCKED/CHECK/VERIFIED）を回す。
4. 毎日同じ時間帯で比較し、文面以外の変数をなるべく固定する。

## 観測指標

- impressions
- engagement rate
- bookmarks
- profile visits
- link clicks
- GitHub stars 増分

## 暫定 Go / No-Go 基準

- median impressions >= 2000
- engagement rate >= 3%
- link_clicks / impressions >= 1%
- GitHub star conversion >= 5%
- 「使ってみたい」等の明確反応が 5件以上
