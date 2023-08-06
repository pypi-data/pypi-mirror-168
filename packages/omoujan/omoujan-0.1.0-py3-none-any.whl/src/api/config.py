import copy
import json
import os

setting: dict = {
    "programming_learning_level": {
        "en": "programming_learning_level",
        "ja": "プログラミング習熟度",
        "level_ja": {
            0: "授業などで触れたことがある程度",
            1: "調べれば任意の処理が書ける",
            2: "調べなくても任意の処理が書ける",
            3: "言語を使うだけでなく、その言語のライブラリを作ったり、フレームワークを作ることもできる",
            4: "拡張ライブラリを記述できるだけでなく、言語の内部仕様、処理系の実装等についても明るい",
        },
    },
    "python_learning_level": {
        "en": "python_learning_level",
        "ja": "Python習熟度",
        "level_ja": {
            0: "授業などで触れたことがある程度",
            1: "調べれば任意の処理が書ける",
            2: "調べなくても任意の処理が書ける",
            3: "言語を使うだけでなく、その言語のライブラリを作ったり、フレームワークを作ることもできる",
            4: "拡張ライブラリを記述できるだけでなく、言語の内部仕様、処理系の実装等についても明るい",
        },
    },
    "nlp_theory_level": {
        "en": "nlp_theory_level",
        "ja": "自然言語処理・概念",
        "level_ja": {
            0: "さっぱりわからん",
            1: "概念はわかる",
            2: "理論レベルで理解してる",
            3: "派生手法や改良手法を理解している",
        },
    },
    "nlp_skill_level": {
        "en": "nlp_skill_level",
        "ja": "自然言語処理・技術",
        "level_ja": {
            0: "実際に使用したことはない",
            1: "GUIツールを用いて分析したことがある",
            2: "ライブラリを用いて実装したことがある",
            3: "アルゴリズムをフルスクラッチで実装したことがある",
        },
    },
    "ip_theory_level": {
        "en": "ip_theory_level",
        "ja": "画像処理・概念",
        "level_ja": {
            0: "さっぱりわからん",
            1: "概念はわかる",
            2: "理論レベルで理解してる",
            3: "派生手法や改良手法を理解している",
        },
    },
    "ip_skill_level": {
        "en": "ip_skill_level",
        "ja": "画像処理・技術",
        "level_ja": {
            0: "実際に使用したことはない",
            1: "GUIツールを用いて分析したことがある",
            2: "ライブラリを用いて実装したことがある",
            3: "アルゴリズムをフルスクラッチで実装したことがある",
        },
    },
    "sp_theory_level": {
        "en": "sp_theory_level",
        "ja": "音声処理・概念",
        "level_ja": {
            0: "さっぱりわからん",
            1: "概念はわかる",
            2: "理論レベルで理解してる",
            3: "派生手法や改良手法を理解している",
        },
    },
    "sp_skill_level": {
        "en": "sp_skill_level",
        "ja": "音声処理・技術",
        "level_ja": {
            0: "実際に使用したことはない",
            1: "GUIツールを用いて分析したことがある",
            2: "ライブラリを用いて実装したことがある",
            3: "アルゴリズムをフルスクラッチで実装したことがある",
        },
    },
    "ml_theory_level": {
        "en": "ml_theory_level",
        "ja": "機械学習・概念",
        "level_ja": {
            0: "さっぱりわからん",
            1: "概念はわかる",
            2: "理論レベルで理解してる",
            3: "派生手法や改良手法を理解している",
        },
    },
    "ml_skill_level": {
        "en": "ml_skill_level",
        "ja": "機械学習・技術",
        "level_ja": {
            0: "実際に使用したことはない",
            1: "GUIツールを用いて分析したことがある",
            2: "ライブラリを用いて実装したことがある",
            3: "アルゴリズムをフルスクラッチで実装したことがある",
        },
    },
    "db_theory_level": {
        "en": "db_theory_level",
        "ja": "データベース・概念",
        "level_ja": {
            0: "さっぱりわからん",
            1: "概念はわかる",
            2: "理論レベルで理解してる",
            3: "派生手法や改良手法を理解している",
        },
    },
    "db_skill_level": {
        "en": "db_skill_level",
        "ja": "データベース・技術",
        "level_ja": {
            0: "実際に使用したことはない",
            1: "GUIツールを用いて分析したことがある",
            2: "ライブラリを用いて実装したことがある",
            3: "アルゴリズムをフルスクラッチで実装したことがある",
        },
    },
    "atcoder_rate": {
        "en": "atcoder_rate",
        "ja": "競プロのレート",
        "level_ja": {
            0: "赤",
            1: "橙",
            2: "黄",
            3: "青",
            4: "水",
            5: "緑",
            6: "茶",
            7: "灰",
            8: "黒",
        },
    },
    "english_reading_level": {
        "en": "english_reading_level",
        "ja": "英語の習熟度",
        "level_ja": {0: "読めない", 1: "調べながら読める", 2: "スラスラ読める"},
    },
    "english_resistance_level": {
        "en": "english_resistance_level",
        "ja": "英語の耐性",
        "level_ja": {0: "抵抗がある、、", 1: "必要であれば読む", 2: "抵抗はない"},
    },
    "translation_resistance": {
        "en": "translation_resistance",
        "ja": "翻訳された英語のサイトへの抵抗",
        "level_ja": {0: False, 1: True},
    },
    "learning_directivity": {
        "en": "translation_resistance",
        "ja": "学びの指向性",
        "level_ja": {0: "概念理解", 1: "実装重視"},
    },
}


class Config:
    def __init__(self) -> None:
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        filedir = "config"
        filename = "user_config.json"
        self.config_filepath: str = os.path.join(CURRENT_DIR, "../", filedir, filename)

        self.config: dict = {
            "user_id": "00000",
            "programming_learning_level": 0,
            "python_learning_level": 0,
            "nlp_theory_level": 0,
            "nlp_skill_level": 0,
            "ip_theory_level": 0,
            "ip_skill_level": 0,
            "sp_theory_level": 0,
            "sp_skill_level": 0,
            "ml_theory_level": 0,
            "ml_skill_level": 0,
            "db_theory_level": 0,
            "db_skill_level": 0,
            "atcoder_rate": 0,
            "english_reading_level": 0,
            "english_resistance_level": 0,
            "translation_resistance": False,
            "learning_directivity": 0,
        }

    def create(self) -> bool:
        try:
            sentence: str = "該当の数字を半角で入力してください。"
            # input(sentence)
            print(sentence)
            for key, values in setting.items():
                ja, level_ja = values["ja"], values["level_ja"]
                value = self._input(ja, level_ja)
                self.config[key] = copy.deepcopy(value)
            self._write()
            return True
        except Exception as e:
            return False

    def update(self) -> bool:
        pass

    def _input(self, lang: str, level: dict) -> int:
        keys: list = list(level.keys())
        prompt: str = f"{lang}\n"
        for key, value in level.items():
            prompt += f"{key}: {value}\n"
        while True:
            value = input(prompt)
            try:
                value = int(value)
                if value in keys:
                    return value
                else:
                    print("該当範囲の半角数字を入力してください。")
            except Exception as e:
                print("半角数字を入力してください。")

    def _write(self) -> bool:
        with open(self.config_filepath, "w", encoding="utf-8") as f:
            json.dump(self.config, f)


if __name__ == "__main__":
    config = Config()
    config.create()
