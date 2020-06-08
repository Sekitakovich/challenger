import xmltodict
import json
import json5
from typing import Dict


circuit: Dict[str, any] = {
    'name': 'Fuji International Speedway',
    'kana': '富士スピードウェイ',
    'international': True,
    'age': 54,
    'km': 4.563,
    'course': ['本コース', 'ショート', 'ドリフト', 'ジムカーナ', 'カート']
}

print(circuit)

print(xmltodict.unparse({'サーキット': circuit}, pretty=True))
print(json.dumps(circuit, ensure_ascii=False, indent=4))
print(json5.dumps(circuit, ensure_ascii=False, indent=4))
