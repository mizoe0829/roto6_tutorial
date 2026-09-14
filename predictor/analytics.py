import pandas as pd
import numpy as np

from .logic import load_draws, NUMBER_RANGE


def build_dataframe() -> pd.DataFrame:
    """draws.jsonをDataFrame化(1行=1回の抽選)"""
    draws = load_draws()
    df = pd.DataFrame(draws)
    df["draw_date"] = pd.to_datetime(df["draw_date"])
    return df


def number_frequency(df: pd.DataFrame) -> pd.Series:
    """各数字(1〜43)の出現回数"""
    all_numbers = pd.Series(
        [n for numbers in df["numbers"] for n in numbers]
    )
    freq = all_numbers.value_counts().reindex(NUMBER_RANGE, fill_value=0)
    return freq.sort_index()


def bonus_frequency(df: pd.DataFrame) -> pd.Series:
    """ボーナス数字の出現回数"""
    freq = df["bonus_number"].value_counts().reindex(NUMBER_RANGE, fill_value=0)
    return freq.sort_index()


def recent_trend(df: pd.DataFrame, window: int = 10) -> pd.Series:
    """直近N回だけの出現頻度(トレンド分析用)"""
    recent = df.sort_values("draw_date").tail(window)
    all_numbers = pd.Series(
        [n for numbers in recent["numbers"] for n in numbers]
    )
    return all_numbers.value_counts().reindex(NUMBER_RANGE, fill_value=0).sort_index()


def summary_stats(df: pd.DataFrame) -> dict:
    """統計サマリー(numpyで簡単な集計)"""
    all_numbers = np.array(
        [n for numbers in df["numbers"] for n in numbers]
    )
    return {
        "total_draws": len(df),
        "mean": round(float(np.mean(all_numbers)), 2),
        "std": round(float(np.std(all_numbers)), 2),
        "most_common": int(pd.Series(all_numbers).mode()[0]),
        "date_range": (
            df["draw_date"].min().strftime("%Y-%m-%d"),
            df["draw_date"].max().strftime("%Y-%m-%d"),
        ) if len(df) > 0 else (None, None),
    }