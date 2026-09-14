import json
import random
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "draws.json"
NUMBER_RANGE = range(1, 44)  # ロト6は1〜43


def load_draws() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _flatten_numbers(draws: list[dict]) -> list[int]:
    return [n for d in draws for n in d["numbers"]]


def predict_by_frequency(draws: list[dict], count: int = 6) -> list[int]:
    """よく出ている数字を優先"""
    freq = Counter(_flatten_numbers(draws))
    top = [n for n, _ in freq.most_common(count)]
    return sorted(top)


def predict_by_absence(draws: list[dict], count: int = 6) -> list[int]:
    """出現頻度が低い(スランプ)数字を優先"""
    freq = Counter(_flatten_numbers(draws))
    ranked = sorted(NUMBER_RANGE, key=lambda n: freq.get(n, 0))
    return sorted(ranked[:count])


def predict_random_weighted(draws: list[dict], count: int = 6) -> list[int]:
    """出現頻度で重み付けしたランダム抽選(重複除去)"""
    freq = Counter(_flatten_numbers(draws))
    weights = [freq.get(n, 1) for n in NUMBER_RANGE]
    picked: set[int] = set()
    while len(picked) < count:
        picked.add(random.choices(list(NUMBER_RANGE), weights=weights, k=1)[0])
    return sorted(picked)


def generate_predictions(count: int = 6) -> dict[str, list[int]]:
    draws = load_draws()
    return {
        "頻出パターン": predict_by_frequency(draws, count),
        "スランプ数字パターン": predict_by_absence(draws, count),
        "重み付けランダム": predict_random_weighted(draws, count),
    }
    
def append_draw(new_draw: dict) -> None:
    """新しい抽選結果をdraws.jsonに追記する(アトミック書き込み)"""
    import tempfile, os

    draws = load_draws()
    draws.append(new_draw)
    with tempfile.NamedTemporaryFile(
        "w", dir=DATA_PATH.parent, delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(draws, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, DATA_PATH)