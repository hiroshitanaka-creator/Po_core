"""
Freedom Pressure Tensor V2 — ML-native 6次元自由圧力テンソル

Phase 6-A: キーワードカウンタから真のMLテンソルへ。

アーキテクチャ:
  1. sentence-transformer で入力を 384D 埋め込み (利用可能な場合)
  2. 6つのアンカー埋め込みとのコサイン類似度で 6D 射影
  3. 6x6 哲学的相関行列 Σ で次元間相互作用を計算
  4. EMA (指数移動平均) で時系列状態を維持
  5. 存在論的整合性チェック (choice↑ + authenticity↓ = 非整合)

Sartre の自由論を工学的に実装:
  「実存は本質に先立つ」→ 選択(choice)が全次元の起点
  「自由の刑」→ choice が高いほど responsibility も高い (Σ[0,1] = 0.6)

フォールバック戦略:
  sentence-transformers 未インストール / モデル未ダウンロードの場合、
  keyword-based fallback (FreedomPressureTensor 相当) に自動降格。
  CI 環境での動作を保証する。
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict, List, Optional

import numpy as np

from po_core.tensors.axis_calibration import load_calibration_model_from_env
from po_core.tensors.base import Tensor
from po_core.text.embedding_cache import GLOBAL_EMBEDDING_CACHE
from po_core.text.normalize import detect_language_simple, normalize_text

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 哲学的相関行列 Σ の定義
# 行/列順: [choice, responsibility, urgency, ethics, social, authenticity]
# 理論的根拠:
#   choice ↔ responsibility (+0.6): Sartre — 自由は責任と不可分
#   responsibility ↔ ethics (+0.7): Kant — 義務論的倫理 (categorical imperative)
#   responsibility ↔ social (+0.5): Levinas — 他者への責任
#   ethics ↔ social (+0.6): Dewey — 社会的倫理
#   choice ↔ authenticity (+0.5): Sartre — 真正な選択
#   authenticity ↔ ethics (+0.4): Aristotle — 徳倫理 (eudaimonia)
# ---------------------------------------------------------------------------
_DEFAULT_CORRELATION_MATRIX = np.array(
    [
        # choice  resp   urgency ethics social  authentic
        [1.0, 0.6, 0.2, 0.3, 0.2, 0.5],  # choice
        [0.6, 1.0, 0.3, 0.7, 0.5, 0.3],  # responsibility
        [0.2, 0.3, 1.0, 0.2, 0.3, 0.1],  # urgency
        [0.3, 0.7, 0.2, 1.0, 0.6, 0.4],  # ethics
        [0.2, 0.5, 0.3, 0.6, 1.0, 0.2],  # social
        [0.5, 0.3, 0.1, 0.4, 0.2, 1.0],  # authenticity
    ],
    dtype=np.float64,
)

# Anchor phrase roots (EN/JA) used for semantic projection calibration.
# JA examples correspond to typical user prompts: 「どちらを選ぶべきか」「責任を取るべきか」 etc.
_ANCHOR_PHRASES_EN: List[str] = [
    "I must make an important choice between multiple alternatives and decide my path.",
    "I am responsible and accountable for the consequences of my actions and obligations.",
    "This is urgent and must be addressed immediately with no time to wait.",
    "This involves deep ethical moral questions about what is right and wrong.",
    "This affects many people society and has broad social consequences for others.",
    "I want to act genuinely and authentically according to my true self and values.",
]

_ANCHOR_PHRASES_JA: List[str] = [
    "複数の選択肢の中からどれを選ぶべきかを判断しなければならない。",
    "自分の行動の結果に責任を持ち、義務を果たす必要がある。",
    "これは緊急で、今すぐ対応しなければ締め切りに間に合わない。",
    "何が正しいか間違っているかという倫理的な問題が含まれている。",
    "これは社会や他者に影響し、多くの人々に関わる。",
    "自分らしさや本心に沿って誠実に行動したい。",
]

# キーワードフォールバック (sentence-transformers が使えない場合)
_KEYWORD_ANCHORS_EN: List[List[str]] = [
    ["should", "must", "decide", "choose", "option", "alternative", "what"],
    ["responsible", "duty", "obligation", "accountable", "answer"],
    ["now", "urgent", "immediate", "quickly", "soon", "deadline"],
    ["right", "wrong", "good", "bad", "moral", "ethical", "virtue"],
    ["we", "us", "society", "people", "community", "others", "everyone"],
    ["authentic", "genuine", "true", "self", "real", "sincere"],
]
_KEYWORD_ANCHORS_JA: List[List[str]] = [
    ["選ぶ", "選択", "判断", "決め", "どちら", "べき"],
    ["責任", "義務", "説明責任", "結果", "影響"],
    ["緊急", "至急", "今すぐ", "すぐ", "締め切り", "期限"],
    ["倫理", "道徳", "正しい", "間違", "善", "悪", "正義"],
    ["社会", "他者", "人々", "みんな", "公共", "コミュニティ"],
    ["自分らし", "本音", "本心", "誠実", "自己", "アイデンティティ"],
]


def _sigmoid(x: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1D arrays."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


@dataclass(frozen=True)
class FreedomPressureV2Snapshot:
    """
    FreedomPressureV2 の計算結果スナップショット。

    TensorValue.dimensions に埋め込まれ、TensorSnapshot に格納される。
    """

    values: Dict[str, float]  # 6次元値 (EMA適用後)
    coherence_score: float  # 存在論的整合性 (0〜1)
    raw_6d: List[float]  # 相関前の生値 (デバッグ用)
    backend: str  # "sbert" | "tfidf" | "keyword"
    overall: float  # L2 ノルムを [0,1] に正規化した総合値

    def to_dict(self) -> Dict[str, Any]:
        return {
            "values": self.values,
            "coherence_score": self.coherence_score,
            "raw_6d": self.raw_6d,
            "backend": self.backend,
            "overall": self.overall,
        }


class FreedomPressureV2(Tensor):
    """
    ML-native 6次元自由圧力テンソル (Phase 6-A)。

    FreedomPressureTensor (v1) のキーワードカウンタを廃し、
    sentence-transformer による意味埋め込みとアンカー類似度で
    6次元を計算する。

    使い方:
        fp_v2 = FreedomPressureV2()  # 初期化時にモデルロード試行
        snapshot = fp_v2.compute_v2("Should I report this misconduct?")
        print(snapshot.values)  # {'choice': 0.72, 'responsibility': 0.68, ...}
        print(snapshot.coherence_score)  # 0.91

    後退互換:
        Tensor.compute() も実装しているため、FreedomPressureTensor と
        同じインターフェースで使用できる。
    """

    DIMS = ["choice", "responsibility", "urgency", "ethics", "social", "authenticity"]
    DEFAULT_DIMENSIONS = 6

    def __init__(
        self,
        name: str = "Freedom_Pressure_V2",
        correlation_matrix: Optional[np.ndarray] = None,
        ema_alpha: float = 0.3,
        correlation_blend: float = 0.35,
        model_name: str = "all-MiniLM-L6-v2",
        anchor_phrases_en: Optional[List[str]] = None,
        anchor_phrases_ja: Optional[List[str]] = None,
        keyword_anchors_en: Optional[List[List[str]]] = None,
        keyword_anchors_ja: Optional[List[List[str]]] = None,
    ) -> None:
        """
        Args:
            name: テンソル名
            correlation_matrix: 6x6 哲学的相関行列。None の場合はデフォルトを使用。
            ema_alpha: EMA 係数 (0=状態更新なし, 1=即時更新)
            correlation_blend: 相関行列の影響度 (0=無効, 1=完全適用)
            model_name: sentence-transformers モデル名
            anchor_phrases_en: 英語アンカーの差し替え設定
            anchor_phrases_ja: 日本語アンカーの差し替え設定
            keyword_anchors_en: 英語キーワードアンカー差し替え設定
            keyword_anchors_ja: 日本語キーワードアンカー差し替え設定
        """
        super().__init__(name, self.DEFAULT_DIMENSIONS)
        self.dimension_names = self.DIMS

        self._Σ: np.ndarray = (
            correlation_matrix
            if correlation_matrix is not None
            else _DEFAULT_CORRELATION_MATRIX.copy()
        )
        # 行ごとに正規化 (重み付き平均として使用)
        row_sums = self._Σ.sum(axis=1, keepdims=True)
        self._Σ_norm: np.ndarray = self._Σ / row_sums

        self._ema_alpha = ema_alpha
        self._blend = correlation_blend
        self._ema_state: Optional[np.ndarray] = None

        self._anchor_phrases_en = list(anchor_phrases_en or _ANCHOR_PHRASES_EN)
        self._anchor_phrases_ja = list(anchor_phrases_ja or _ANCHOR_PHRASES_JA)
        self._keyword_anchors_en = [
            list(v) for v in (keyword_anchors_en or _KEYWORD_ANCHORS_EN)
        ]
        self._keyword_anchors_ja = [
            list(v) for v in (keyword_anchors_ja or _KEYWORD_ANCHORS_JA)
        ]

        # EMA 履歴 (直近20件を保持)
        self._history: Deque[np.ndarray] = deque(maxlen=20)

        # encoder と anchor_embeddings の遅延初期化
        self._encoder: Any = None
        self._anchor_embeddings_en: Optional[np.ndarray] = None
        self._anchor_embeddings_ja: Optional[np.ndarray] = None
        self._backend: str = "keyword"  # 初期状態はキーワードフォールバック
        self._model_name = model_name
        self._calibration_model = load_calibration_model_from_env()
        self._init_encoder()

    # ------------------------------------------------------------------
    # encoder 初期化
    # ------------------------------------------------------------------

    def _init_encoder(self) -> None:
        """sentence-transformers を遅延ロード。失敗時はキーワードフォールバック。"""
        try:
            from sentence_transformers import SentenceTransformer  # noqa: PLC0415

            self._encoder = SentenceTransformer(self._model_name)
            anchors_en = self._encoder.encode(
                self._anchor_phrases_en, show_progress_bar=False
            )
            anchors_ja = self._encoder.encode(
                self._anchor_phrases_ja, show_progress_bar=False
            )
            self._anchor_embeddings_en = np.array(anchors_en, dtype=np.float64)
            self._anchor_embeddings_ja = np.array(anchors_ja, dtype=np.float64)
            self._backend = "sbert"
            logger.debug(
                "FreedomPressureV2: sbert backend initialized (%s)", self._model_name
            )
        except Exception as exc:
            logger.info(
                "FreedomPressureV2: sentence-transformers unavailable (%s), "
                "falling back to keyword backend.",
                exc,
            )
            self._backend = "keyword"

    # ------------------------------------------------------------------
    # 公開 API
    # ------------------------------------------------------------------

    def compute_v2(
        self,
        text: str,
        memory_depth: int = 0,
    ) -> FreedomPressureV2Snapshot:
        """
        ML-native 6次元自由圧力を計算する (メインAPI)。

        Args:
            text: 分析するテキスト
            memory_depth: 過去の会話の深さ (urgency への加算ブースト)

        Returns:
            FreedomPressureV2Snapshot
        """
        # Step 1: 6D 生値計算 (embedding or keyword)
        raw_6d = self._compute_raw_6d(text)

        # Step 1.5: 校正パラメータがあれば適用 (なければ従来ロジック)
        raw_6d = self._apply_calibration(raw_6d)

        # Step 2: メモリ深度によるブースト
        if memory_depth > 0:
            boost = min(memory_depth * 0.03, 0.2)
            raw_6d = np.clip(
                raw_6d + boost * np.array([0.2, 0.3, 0.1, 0.2, 0.1, 0.1]), 0.0, 1.0
            )

        # Step 3: 哲学的相関テンソル適用
        correlated = self._apply_correlation(raw_6d)

        # Step 4: EMA 時系列更新
        ema_state = self._update_ema(correlated)

        # Step 5: 存在論的整合性チェック
        coherence = self._check_ontological_coherence(ema_state)

        # Step 6: 総合スコア (L2 ノルムを 6D 最大値で正規化)
        overall = float(np.linalg.norm(ema_state) / np.sqrt(6))

        # numpy → Python float に変換
        values = {dim: round(float(ema_state[i]), 4) for i, dim in enumerate(self.DIMS)}

        # data 更新 (Tensor 基底クラスの data フィールドを同期)
        self.data = ema_state.copy()

        self._history.append(ema_state.copy())

        return FreedomPressureV2Snapshot(
            values=values,
            coherence_score=round(coherence, 4),
            raw_6d=[round(float(v), 4) for v in raw_6d],
            backend=self._backend,
            overall=round(overall, 4),
        )

    def compute(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        philosopher_perspectives: Optional[List[Dict[str, Any]]] = None,
    ) -> np.ndarray:
        """
        Tensor 基底クラスとの後退互換 API。

        compute_v2() を内部で呼び出し、numpy array を返す。
        """
        self.compute_v2(prompt)
        return self.data

    def get_pressure_summary(self) -> Dict[str, float]:
        """FreedomPressureTensor 互換: 次元名 → 値のdict を返す。"""
        if self._ema_state is not None:
            return {
                dim: round(float(self._ema_state[i]), 4)
                for i, dim in enumerate(self.DIMS)
            }
        return {dim: 0.0 for dim in self.DIMS}

    @property
    def backend(self) -> str:
        """使用中のバックエンド ('sbert' | 'keyword')。"""
        return self._backend

    # ------------------------------------------------------------------
    # 内部計算
    # ------------------------------------------------------------------

    def _compute_raw_6d(self, text: str) -> np.ndarray:
        """埋め込みまたはキーワードで 6D 生値を計算。"""
        normalized = normalize_text(text)
        language = detect_language_simple(normalized)
        if (
            self._backend == "sbert"
            and self._anchor_embeddings_en is not None
            and self._anchor_embeddings_ja is not None
        ):
            return self._compute_embedding_6d(normalized, language)
        return self._compute_keyword_6d(normalized, language)

    def _compute_embedding_6d(self, text: str, language: str) -> np.ndarray:
        """
        sentence-transformer による 6D 計算。

        アンカーフレーズとのコサイン類似度 → [0,1] 正規化。
        """
        model_id = f"sbert:{self._model_name}"
        cached = GLOBAL_EMBEDDING_CACHE.get(text, model_id)
        if cached is None:
            fresh = self._encoder.encode([text], show_progress_bar=False)[0]
            embedding = np.array(fresh, dtype=np.float64)
            GLOBAL_EMBEDDING_CACHE.put(text, model_id, embedding)
        else:
            embedding = np.array(cached, dtype=np.float64)

        def _score_against(anchors: np.ndarray) -> np.ndarray:
            score = np.zeros(6, dtype=np.float64)
            for i, anchor_vec in enumerate(anchors):
                sim = _cosine_similarity(embedding, anchor_vec)
                score[i] = (sim + 1.0) / 2.0
            return np.clip(score, 0.0, 1.0)

        score_en = _score_against(self._anchor_embeddings_en)
        score_ja = _score_against(self._anchor_embeddings_ja)

        if language == "en":
            return score_en
        if language == "ja":
            return score_ja
        return np.maximum(score_en, score_ja)

    def _compute_keyword_6d(self, text: str, language: str) -> np.ndarray:
        """キーワードベースの 6D 計算 (FreedomPressureTensor 相当のフォールバック)。"""
        raw_en = np.zeros(6, dtype=np.float64)
        raw_ja = np.zeros(6, dtype=np.float64)

        for i, keywords in enumerate(self._keyword_anchors_en):
            hits = sum(1 for kw in keywords if kw in text)
            raw_en[i] = min(hits / max(len(keywords), 1), 1.0)

        for i, keywords in enumerate(self._keyword_anchors_ja):
            hits = sum(1 for kw in keywords if kw in text)
            raw_ja[i] = min(hits / max(len(keywords), 1), 1.0)

        if language == "en":
            return raw_en
        if language == "ja":
            return raw_ja
        return np.maximum(raw_en, raw_ja)

    def _apply_calibration(self, raw_6d: np.ndarray) -> np.ndarray:
        """Optional linear calibration on raw 6D scores."""
        if self._calibration_model is None:
            return raw_6d
        return self._calibration_model.apply(raw_6d, self.DIMS)

    def _apply_correlation(self, raw_6d: np.ndarray) -> np.ndarray:
        """
        哲学的相関行列 Σ を soft blend で適用。

        final[i] = (1-blend) * raw[i] + blend * (Σ_norm[i] @ raw)

        blend=0.35 で「元の値 65% + 哲学的相互作用 35%」のバランス。
        """
        influenced = self._Σ_norm @ raw_6d  # (6,)
        blended = (1.0 - self._blend) * raw_6d + self._blend * influenced
        return np.clip(blended, 0.0, 1.0)

    def _update_ema(self, current: np.ndarray) -> np.ndarray:
        """EMA 時系列更新。alpha=0 なら即時更新なし。"""
        if self._ema_alpha <= 0.0 or self._ema_state is None:
            self._ema_state = current.copy()
        else:
            self._ema_state = (
                self._ema_alpha * current + (1.0 - self._ema_alpha) * self._ema_state
            )
        return self._ema_state.copy()

    def _check_ontological_coherence(self, state: np.ndarray) -> float:
        """
        存在論的整合性スコア (0〜1)。

        不整合パターン:
          - choice が高いのに authenticity が極端に低い
            → 自由だが不誠実 (Sartre の自欺 mauvaise foi)
          - responsibility が高いのに ethics が低い
            → 義務感があるのに倫理欠如 (Kant 的矛盾)
        """
        choice, responsibility, _, ethics, _, authenticity = state
        incoherence = 0.0

        # Sartre パターン: choice↑ + authenticity↓
        if choice > 0.65 and authenticity < 0.35:
            incoherence += (choice - authenticity) * 0.4

        # Kant パターン: responsibility↑ + ethics↓
        if responsibility > 0.65 and ethics < 0.35:
            incoherence += (responsibility - ethics) * 0.5

        return float(max(0.0, 1.0 - incoherence))

    def reset_state(self) -> None:
        """EMA 状態をリセット (テスト・新セッション開始時に使用)。"""
        self._ema_state = None
        self._history.clear()

    # ------------------------------------------------------------------
    # FreedomPressureTensor 互換メソッド
    # ------------------------------------------------------------------

    def get_dimension_value(self, dimension_name: str) -> float:
        """次元名から値を取得 (FreedomPressureTensor 互換)。"""
        if self._ema_state is None:
            return 0.0
        try:
            idx = self.DIMS.index(dimension_name)
            return float(self._ema_state[idx])
        except ValueError:
            raise ValueError(
                f"Invalid dimension: {dimension_name!r}. Valid: {self.DIMS}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """辞書表現 (拡張版)。"""
        base = super().to_dict()
        base["dimension_names"] = self.DIMS
        base["pressure_summary"] = self.get_pressure_summary()
        base["overall_pressure"] = self.norm()
        base["backend"] = self._backend
        if self._ema_state is not None:
            base["coherence_score"] = self._check_ontological_coherence(self._ema_state)
        return base

    # ------------------------------------------------------------------
    # 統計ユーティリティ
    # ------------------------------------------------------------------

    def get_history_mean(self) -> Optional[Dict[str, float]]:
        """直近履歴の次元別平均。履歴が空の場合は None。"""
        if not self._history:
            return None
        mean_state = np.mean(list(self._history), axis=0)
        return {dim: round(float(mean_state[i]), 4) for i, dim in enumerate(self.DIMS)}

    def get_drift_score(self) -> Optional[float]:
        """
        ドリフトスコア: 最初の記録と最新の記録のユークリッド距離。

        EMA状態がどれだけ変化したかを示す。
        """
        if len(self._history) < 2:
            return None
        first = self._history[0]
        last = self._history[-1]
        return float(np.linalg.norm(last - first))


def preload_model(model_name: str = "all-MiniLM-L6-v2") -> dict[str, str]:
    """Best-effort preload hook used by runtime wiring."""
    status: dict[str, str] = {"model": model_name}
    try:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        SentenceTransformer(model_name)
        status["sbert"] = "ready"
    except Exception as exc:
        status["sbert"] = f"failed: {exc}"
    return status


def create_freedom_pressure_v2(
    ema_alpha: float = 0.3,
    correlation_blend: float = 0.35,
    model_name: str = "all-MiniLM-L6-v2",
    correlation_matrix: Optional[np.ndarray] = None,
    anchor_phrases_en: Optional[List[str]] = None,
    anchor_phrases_ja: Optional[List[str]] = None,
    keyword_anchors_en: Optional[List[List[str]]] = None,
    keyword_anchors_ja: Optional[List[List[str]]] = None,
) -> FreedomPressureV2:
    """
    FreedomPressureV2 のファクトリ関数。

    engine.py から呼び出す際のエントリポイント。
    """
    return FreedomPressureV2(
        ema_alpha=ema_alpha,
        correlation_blend=correlation_blend,
        model_name=model_name,
        correlation_matrix=correlation_matrix,
        anchor_phrases_en=anchor_phrases_en,
        anchor_phrases_ja=anchor_phrases_ja,
        keyword_anchors_en=keyword_anchors_en,
        keyword_anchors_ja=keyword_anchors_ja,
    )


__all__ = [
    "FreedomPressureV2",
    "FreedomPressureV2Snapshot",
    "create_freedom_pressure_v2",
    "preload_model",
    "_DEFAULT_CORRELATION_MATRIX",
]
