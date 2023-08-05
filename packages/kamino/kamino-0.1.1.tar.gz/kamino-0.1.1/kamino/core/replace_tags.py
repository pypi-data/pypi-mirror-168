import re
from typing import Dict
def replace_tags(content: str, patterns: Dict) -> str:
  result = content
  for pattern, pattern_value in patterns.items():
    regex = fr"\${pattern}\$"
    regex = re.compile(regex)
    result = re.sub(regex, pattern_value, result)
  return result
