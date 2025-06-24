import re
from pathlib import Path

class SensitiveFilter:
    def __init__(self):
        self.word_set = self._load_words()
        self.pattern = self._build_pattern()
    
    def _load_words(self):
        words_path = Path(__file__).parent.parent / "resources/sensitive_words.txt"
        with open(words_path, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}
    
    def _build_pattern(self):
        # 使用正则优化匹配性能
        return re.compile("|".join(
            [r"\b" + re.escape(word) + r"\b" for word in self.word_set]
        ))
    
    def filter(self, text, replace_char="*"):
        """返回(是否含敏感词, 过滤后文本)"""
        found = False
        def replace(match):
            nonlocal found
            found = True
            return replace_char * len(match.group())
        
        cleaned = self.pattern.sub(replace, text)
        return found, cleaned

# 单例模式
filter_util = SensitiveFilter()