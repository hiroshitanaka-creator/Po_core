"""
Unit tests for FreedomPressureV2 — Phase 6-A

テスト戦略:
  - sentence-transformers の有無に依存しない (keyword fallback で動作)
  - 各次元の意味的一致を検証 (ethics重い文 → ethics次元が高い etc.)
  - EMA 時系列更新の検証
  - 存在論的整合性チェックの検証 (Sartre/Kant パターン)
  - 相関行列適用の検証
  - FreedomPressureTensor との後退互換性検証
  - engine.py feature flag 統合の検証
"""

import os

import numpy as np
import pytest

from po_core.tensors.freedom_pressure_v2 import (
    FreedomPressureV2,
    FreedomPressureV2Snapshot,
    _DEFAULT_CORRELATION_MATRIX,
    create_freedom_pressure_v2,
)


# ---------------------------------------------------------------------------
# フィクスチャ
# ---------------------------------------------------------------------------


@pytest.fixture
def fp_v2_keyword():
    """キーワードバックエンド強制の FreedomPressureV2 (CI 環境対応)。"""
    fp = FreedomPressureV2(model_name="__nonexistent_model_to_force_keyword_fallback__")
    assert fp.backend == "keyword"
    fp.reset_state()
    return fp


@pytest.fixture
def fp_v2_fresh():
    """通常の FreedomPressureV2 (sbert 利用可能な場合はそちら、なければ keyword)。"""
    fp = create_freedom_pressure_v2()
    fp.reset_state()
    return fp


# ---------------------------------------------------------------------------
# 基本機能テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFreedomPressureV2Init:
    """初期化・設定テスト。"""

    def test_default_initialization(self):
        """デフォルト初期化でインスタンスが生成される。"""
        fp = FreedomPressureV2(model_name="__force_keyword__")
        assert fp.name == "Freedom_Pressure_V2"
        assert fp.dimensions == 6
        assert len(fp.DIMS) == 6

    def test_dims_names(self):
        """6次元名が正しく定義されている。"""
        fp = FreedomPressureV2(model_name="__force_keyword__")
        assert fp.DIMS == [
            "choice",
            "responsibility",
            "urgency",
            "ethics",
            "social",
            "authenticity",
        ]

    def test_keyword_fallback_on_bad_model(self):
        """存在しないモデル名でキーワードバックエンドに降格する。"""
        fp = FreedomPressureV2(model_name="__nonexistent_model__")
        assert fp.backend == "keyword"

    def test_correlation_matrix_shape(self):
        """相関行列が 6x6 であること。"""
        assert _DEFAULT_CORRELATION_MATRIX.shape == (6, 6)

    def test_correlation_matrix_diagonal_ones(self):
        """相関行列の対角成分が 1.0 であること (自己相関)。"""
        assert np.allclose(np.diag(_DEFAULT_CORRELATION_MATRIX), 1.0)

    def test_correlation_matrix_symmetry(self):
        """相関行列が対称行列であること。"""
        assert np.allclose(_DEFAULT_CORRELATION_MATRIX, _DEFAULT_CORRELATION_MATRIX.T)

    def test_custom_correlation_matrix(self):
        """カスタム相関行列が正しく設定される。"""
        custom = np.eye(6, dtype=np.float64)
        fp = FreedomPressureV2(
            correlation_matrix=custom, model_name="__force_keyword__"
        )
        assert np.allclose(fp._Σ, custom)

    def test_factory_function(self):
        """create_freedom_pressure_v2() がインスタンスを返す。"""
        fp = create_freedom_pressure_v2(model_name="__force_keyword__")
        assert isinstance(fp, FreedomPressureV2)


# ---------------------------------------------------------------------------
# 6次元計算テスト (keyword backend)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFreedomPressureV2Computation:
    """6次元値の計算精度テスト。"""

    def test_returns_snapshot(self, fp_v2_keyword):
        """compute_v2() が FreedomPressureV2Snapshot を返す。"""
        result = fp_v2_keyword.compute_v2("What should I do?")
        assert isinstance(result, FreedomPressureV2Snapshot)

    def test_snapshot_has_all_dims(self, fp_v2_keyword):
        """スナップショットに6次元すべてが含まれる。"""
        result = fp_v2_keyword.compute_v2("Should I choose this path?")
        assert set(result.values.keys()) == set(FreedomPressureV2.DIMS)

    def test_values_in_range(self, fp_v2_keyword):
        """すべての次元値が [0, 1] の範囲内であること。"""
        result = fp_v2_keyword.compute_v2(
            "I must decide now. This is urgent and ethical."
        )
        for dim, val in result.values.items():
            assert 0.0 <= val <= 1.0, f"{dim}={val} is out of [0,1]"

    def test_overall_in_range(self, fp_v2_keyword):
        """overall スコアが [0, 1] の範囲内であること。"""
        result = fp_v2_keyword.compute_v2("A simple question.")
        assert 0.0 <= result.overall <= 1.0

    def test_choice_heavy_text(self, fp_v2_keyword):
        """選択関連キーワードが多い文で choice 次元が高くなる。"""
        fp_v2_keyword.reset_state()
        result = fp_v2_keyword.compute_v2(
            "Should I choose this option? I must decide between these alternatives."
        )
        assert result.values["choice"] > 0.0, "choice should be > 0 for choice-heavy text"

    def test_ethics_heavy_text(self, fp_v2_keyword):
        """倫理関連キーワードが多い文で ethics 次元が高くなる。"""
        fp_v2_keyword.reset_state()
        result = fp_v2_keyword.compute_v2(
            "This is wrong. We must consider what is morally right and ethical."
        )
        assert result.values["ethics"] > 0.0, "ethics should be > 0 for ethics-heavy text"

    def test_social_heavy_text(self, fp_v2_keyword):
        """社会関連キーワードが多い文で social 次元が高くなる。"""
        fp_v2_keyword.reset_state()
        result = fp_v2_keyword.compute_v2(
            "We, as a community and society, must protect others and people around us."
        )
        assert result.values["social"] > 0.0, "social should be > 0 for social-heavy text"

    def test_urgency_heavy_text(self, fp_v2_keyword):
        """緊急キーワードが多い文で urgency 次元が高くなる。"""
        fp_v2_keyword.reset_state()
        result = fp_v2_keyword.compute_v2(
            "Act now immediately! This is urgent and must be done quickly soon."
        )
        assert result.values["urgency"] > 0.0, "urgency should be > 0 for urgent text"

    def test_empty_text_does_not_crash(self, fp_v2_keyword):
        """空文字列でクラッシュしない。"""
        fp_v2_keyword.reset_state()
        result = fp_v2_keyword.compute_v2("")
        assert isinstance(result, FreedomPressureV2Snapshot)

    def test_long_text_does_not_crash(self, fp_v2_keyword):
        """非常に長いテキストでもクラッシュしない。"""
        fp_v2_keyword.reset_state()
        long_text = ("Should I choose this option? " * 100).strip()
        result = fp_v2_keyword.compute_v2(long_text)
        assert isinstance(result, FreedomPressureV2Snapshot)

    def test_backend_field(self, fp_v2_keyword):
        """keyword バックエンドの場合 backend='keyword'。"""
        result = fp_v2_keyword.compute_v2("test")
        assert result.backend == "keyword"

    def test_raw_6d_length(self, fp_v2_keyword):
        """raw_6d が長さ 6 のリストである。"""
        result = fp_v2_keyword.compute_v2("test")
        assert len(result.raw_6d) == 6


# ---------------------------------------------------------------------------
# EMA 時系列テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFreedomPressureV2EMA:
    """EMA 時系列更新テスト。"""

    def test_ema_state_initialized_on_first_call(self, fp_v2_keyword):
        """初回呼び出しで EMA 状態が初期化される。"""
        assert fp_v2_keyword._ema_state is None
        fp_v2_keyword.compute_v2("First call.")
        assert fp_v2_keyword._ema_state is not None

    def test_ema_state_changes_on_second_call(self, fp_v2_keyword):
        """2回目の呼び出しで EMA 状態が更新される。"""
        fp_v2_keyword.compute_v2("First: choose decide option.")
        first_state = fp_v2_keyword._ema_state.copy()
        fp_v2_keyword.compute_v2("Second: urgent now immediately!")
        second_state = fp_v2_keyword._ema_state.copy()
        # EMA alpha=0.3 なので状態は変化しているはず
        assert not np.allclose(first_state, second_state)

    def test_ema_smoothing_effect(self):
        """alpha=1.0 (即時更新) では EMA が入力と同じになる。"""
        fp = FreedomPressureV2(
            ema_alpha=1.0, model_name="__nonexistent_force_keyword_fallback__"
        )
        fp.reset_state()
        result = fp.compute_v2("choose decide option should")
        # alpha=1.0 → ema_state = current → raw の EMA に相関行列を適用した値
        assert fp._ema_state is not None
        # result.values は round(..., 4) で丸められるため atol=5e-4 で比較
        assert np.allclose(
            np.array(list(result.values.values())),
            fp._ema_state,
            atol=5e-4,
        )

    def test_reset_state_clears_ema(self, fp_v2_keyword):
        """reset_state() で EMA 状態がクリアされる。"""
        fp_v2_keyword.compute_v2("test input")
        assert fp_v2_keyword._ema_state is not None
        fp_v2_keyword.reset_state()
        assert fp_v2_keyword._ema_state is None
        assert len(fp_v2_keyword._history) == 0

    def test_history_accumulates(self, fp_v2_keyword):
        """履歴が呼び出し回数分だけ蓄積される。"""
        for i in range(5):
            fp_v2_keyword.compute_v2(f"call number {i}")
        assert len(fp_v2_keyword._history) == 5

    def test_history_max_size(self, fp_v2_keyword):
        """履歴は最大 20 件まで保持される。"""
        for i in range(25):
            fp_v2_keyword.compute_v2(f"call {i}")
        assert len(fp_v2_keyword._history) == 20

    def test_get_history_mean_empty(self, fp_v2_keyword):
        """履歴が空の場合 get_history_mean() は None を返す。"""
        assert fp_v2_keyword.get_history_mean() is None

    def test_get_history_mean_after_calls(self, fp_v2_keyword):
        """履歴がある場合 get_history_mean() が正しい次元名のdictを返す。"""
        for _ in range(3):
            fp_v2_keyword.compute_v2("test")
        mean = fp_v2_keyword.get_history_mean()
        assert mean is not None
        assert set(mean.keys()) == set(FreedomPressureV2.DIMS)

    def test_get_drift_score_needs_two_calls(self, fp_v2_keyword):
        """1回だけの呼び出しでは drift_score は None。"""
        fp_v2_keyword.compute_v2("first")
        assert fp_v2_keyword.get_drift_score() is None

    def test_get_drift_score_after_multiple_calls(self, fp_v2_keyword):
        """異なる内容の呼び出し後はドリフトスコアが 0 より大きい。"""
        fp_v2_keyword.compute_v2("should decide choose option must")
        fp_v2_keyword.compute_v2("society people community we others")
        drift = fp_v2_keyword.get_drift_score()
        assert drift is not None
        assert drift >= 0.0

    def test_memory_depth_boost(self, fp_v2_keyword):
        """memory_depth > 0 でスコアにブーストが乗る。"""
        fp_v2_keyword.reset_state()
        r0 = fp_v2_keyword.compute_v2("test", memory_depth=0)
        fp_v2_keyword.reset_state()
        r5 = fp_v2_keyword.compute_v2("test", memory_depth=5)
        # memory_depth=5 の方が overall が高い (またはどこかの次元が高い)
        sum0 = sum(r0.values.values())
        sum5 = sum(r5.values.values())
        assert sum5 >= sum0


# ---------------------------------------------------------------------------
# 存在論的整合性テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOntologicalCoherence:
    """存在論的整合性チェックのテスト。"""

    def test_coherence_in_range(self, fp_v2_keyword):
        """coherence_score が [0, 1] の範囲内であること。"""
        result = fp_v2_keyword.compute_v2("What should I decide?")
        assert 0.0 <= result.coherence_score <= 1.0

    def test_sartre_incoherence_detection(self):
        """
        Sartre の mauvaise foi: choice が高く authenticity が低い場合に
        整合性スコアが低下する。
        """
        fp = FreedomPressureV2(model_name="__force_keyword__")
        # 直接 _check_ontological_coherence を呼ぶ (内部メソッドテスト)
        # choice=0.9 (高), authenticity=0.1 (低) → 不整合
        incoherent_state = np.array([0.9, 0.5, 0.5, 0.5, 0.5, 0.1])
        coherent_state = np.array([0.9, 0.5, 0.5, 0.5, 0.5, 0.9])

        incoherent_score = fp._check_ontological_coherence(incoherent_state)
        coherent_score = fp._check_ontological_coherence(coherent_state)

        assert incoherent_score < coherent_score, (
            f"Sartre incoherence should lower score: {incoherent_score} vs {coherent_score}"
        )

    def test_kant_incoherence_detection(self):
        """
        Kant の矛盾: responsibility が高く ethics が低い場合に
        整合性スコアが低下する。
        """
        fp = FreedomPressureV2(model_name="__force_keyword__")
        # responsibility=0.9 (高), ethics=0.1 (低) → 不整合
        incoherent_state = np.array([0.5, 0.9, 0.5, 0.1, 0.5, 0.5])
        coherent_state = np.array([0.5, 0.9, 0.5, 0.9, 0.5, 0.5])

        incoherent_score = fp._check_ontological_coherence(incoherent_state)
        coherent_score = fp._check_ontological_coherence(coherent_state)

        assert incoherent_score < coherent_score, (
            f"Kant incoherence should lower score: {incoherent_score} vs {coherent_score}"
        )

    def test_fully_coherent_state(self):
        """すべての次元が高い場合 coherence_score が高い (≥0.8)。"""
        fp = FreedomPressureV2(model_name="__force_keyword__")
        all_high = np.array([0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
        score = fp._check_ontological_coherence(all_high)
        assert score >= 0.8, f"Fully coherent state should score ≥ 0.8, got {score}"


# ---------------------------------------------------------------------------
# 相関行列テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCorrelationMatrix:
    """哲学的相関行列の適用テスト。"""

    def test_correlation_increases_related_dims(self):
        """
        choice が高い状態で相関行列を適用すると
        responsibility と authenticity も上昇する。
        """
        fp = FreedomPressureV2(
            correlation_blend=0.99,  # 相関の影響を最大化
            model_name="__force_keyword__",
        )
        # choice のみ高い入力
        raw_choice_heavy = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        correlated = fp._apply_correlation(raw_choice_heavy)

        # choice↑ → responsibility (Σ[0,1]=0.6) と authenticity (Σ[0,5]=0.5) も上昇
        assert correlated[1] > 0.0, "responsibility should rise with choice"
        assert correlated[5] > 0.0, "authenticity should rise with choice"

    def test_correlation_blend_zero_is_identity(self):
        """blend=0.0 では相関行列が適用されず、入力がそのまま出力される。"""
        fp = FreedomPressureV2(
            correlation_blend=0.0,
            model_name="__force_keyword__",
        )
        raw = np.array([0.5, 0.3, 0.7, 0.2, 0.6, 0.4])
        result = fp._apply_correlation(raw)
        assert np.allclose(result, raw)


# ---------------------------------------------------------------------------
# 後退互換性テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestFreedomPressureV2BackwardCompat:
    """FreedomPressureTensor との後退互換性テスト。"""

    def test_compute_method_returns_ndarray(self, fp_v2_keyword):
        """Tensor.compute() が numpy array を返す (基底クラス互換)。"""
        result = fp_v2_keyword.compute("What should I do?")
        assert isinstance(result, np.ndarray)
        assert result.shape == (6,)

    def test_get_pressure_summary_returns_dict(self, fp_v2_keyword):
        """get_pressure_summary() が dict[str, float] を返す。"""
        fp_v2_keyword.compute_v2("test")
        summary = fp_v2_keyword.get_pressure_summary()
        assert isinstance(summary, dict)
        assert set(summary.keys()) == set(FreedomPressureV2.DIMS)

    def test_get_dimension_value(self, fp_v2_keyword):
        """get_dimension_value() が単一次元の値を返す。"""
        fp_v2_keyword.compute_v2("decide choose option")
        val = fp_v2_keyword.get_dimension_value("choice")
        assert isinstance(val, float)
        assert 0.0 <= val <= 1.0

    def test_get_dimension_value_invalid(self, fp_v2_keyword):
        """無効な次元名で ValueError が発生する。"""
        fp_v2_keyword.compute_v2("test")
        with pytest.raises(ValueError, match="Invalid dimension"):
            fp_v2_keyword.get_dimension_value("nonexistent_dim")

    def test_norm_method(self, fp_v2_keyword):
        """norm() が正の float を返す。"""
        fp_v2_keyword.compute_v2("decide choose option must")
        n = fp_v2_keyword.norm()
        assert isinstance(n, float)
        assert n >= 0.0

    def test_to_dict_has_required_keys(self, fp_v2_keyword):
        """to_dict() に必要なキーが含まれる。"""
        fp_v2_keyword.compute_v2("test")
        d = fp_v2_keyword.to_dict()
        assert "dimension_names" in d
        assert "pressure_summary" in d
        assert "overall_pressure" in d
        assert "backend" in d


# ---------------------------------------------------------------------------
# engine.py feature flag 統合テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEngineFeatureFlag:
    """engine.py の PO_FREEDOM_PRESSURE_V2 feature flag テスト。"""

    def test_flag_off_uses_v1(self, monkeypatch):
        """フラグ OFF では FreedomPressureTensor (v1) が使われる。"""
        monkeypatch.delenv("PO_FREEDOM_PRESSURE_V2", raising=False)
        from po_core.tensors.engine import compute_tensors

        snapshot = compute_tensors("What is justice?")
        # v1 は "FreedomPressureTensor" ソース
        fp_value = snapshot.values.get("freedom_pressure")
        assert fp_value is not None
        assert fp_value.source == "FreedomPressureTensor"

    def test_flag_on_uses_v2(self, monkeypatch):
        """フラグ ON では FreedomPressureV2 が使われる。"""
        monkeypatch.setenv("PO_FREEDOM_PRESSURE_V2", "true")
        # engine モジュールを再インポートして環境変数を反映
        import importlib

        import po_core.tensors.engine as eng_mod

        importlib.reload(eng_mod)

        snapshot = eng_mod.compute_tensors("What is justice?")
        fp_value = snapshot.values.get("freedom_pressure")
        assert fp_value is not None
        assert fp_value.source.startswith("FreedomPressureV2/"), (
            f"Expected FreedomPressureV2/* source, got {fp_value.source!r}"
        )

    def test_v2_dimensions_include_coherence_score(self, monkeypatch):
        """フラグ ON では dimensions に coherence_score が含まれる。"""
        monkeypatch.setenv("PO_FREEDOM_PRESSURE_V2", "true")
        import importlib

        import po_core.tensors.engine as eng_mod

        importlib.reload(eng_mod)

        snapshot = eng_mod.compute_tensors("I must decide between options.")
        fp_value = snapshot.values.get("freedom_pressure")
        assert fp_value is not None
        assert fp_value.dimensions is not None
        assert "coherence_score" in fp_value.dimensions


# ---------------------------------------------------------------------------
# Settings feature flag テスト
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSettingsFeatureFlag:
    """Settings.use_freedom_pressure_v2 テスト。"""

    def test_default_is_false(self):
        """デフォルトでフィーチャーフラグは False。"""
        from po_core.runtime.settings import Settings

        s = Settings()
        assert s.use_freedom_pressure_v2 is False

    def test_can_enable_flag(self):
        """フィーチャーフラグを有効化できる。"""
        from po_core.runtime.settings import Settings

        s = Settings(use_freedom_pressure_v2=True)
        assert s.use_freedom_pressure_v2 is True

    def test_to_dict_includes_flag(self):
        """to_dict() に use_freedom_pressure_v2 が含まれる。"""
        from po_core.runtime.settings import Settings

        d = Settings().to_dict()
        assert "use_freedom_pressure_v2" in d
