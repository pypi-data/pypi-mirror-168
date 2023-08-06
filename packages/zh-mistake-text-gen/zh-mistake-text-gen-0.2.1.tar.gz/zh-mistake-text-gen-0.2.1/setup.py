# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zh_mistake_text_gen']

package_data = \
{'': ['*']}

install_requires = \
['OpenCC>=1.1.4,<2.0.0',
 'jieba>=0.42.1,<0.43.0',
 'loguru>=0.6.0,<0.7.0',
 'py-chinese-pronounce>=0.1.5,<0.2.0',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'zh-mistake-text-gen',
    'version': '0.2.1',
    'description': '中文錯誤類型文字增量',
    'long_description': '# 錯誤類型中文語料生成\n## 安裝\n```bash\npip install zh-mistake-text-gen\n```\n## 使用 (Pipeline)\n```python\nfrom zh_mistake_text_gen import Pipeline\nimport random\n\nrandom.seed(7)\npipeline = Pipeline()\naugs = pipeline("中文語料生成",k=8)\nfor aug in augs:\n    print(aug)\n```\n```\ntype=\'MissingWordMaker\' correct=\'中文語料生成\' incorrect=\'中文料生成\' incorrect_start_at=2 incorrect_end_at=2 span=\'語\'\ntype=\'MissingVocabMaker\' correct=\'中文語料生成\' incorrect=\'語料生成\' incorrect_start_at=0 incorrect_end_at=2 span=\'中文\'\ntype=\'PronounceSimilarWordMaker\' correct=\'中文語料生成\' incorrect=\'中文語尥生成\' incorrect_start_at=3 incorrect_end_at=3 span=\'尥\'\ntype=\'PronounceSameWordMaker\' correct=\'中文語料生成\' incorrect=\'諥文語料生成\' incorrect_start_at=0 incorrect_end_at=0 span=\'諥\'\ntype=\'PronounceSimilarVocabMaker\' correct=\'中文語料生成\' incorrect=\'鍾文語料生成\' incorrect_start_at=0 incorrect_end_at=2 span=\'鍾文\'\ntype=\'PronounceSameVocabMaker\' correct=\'中文語料生成\' incorrect=\'中文预料生成\' incorrect_start_at=2 incorrect_end_at=4 span=\'预料\'\ntype=\'RedundantWordMaker\' correct=\'中文語料生成\' incorrect=\'成中文語料生成\' incorrect_start_at=0 incorrect_end_at=0 span=\'成\'\ntype=\'MistakWordMaker\' correct=\'中文語料生成\' incorrect=\'谁文語料生成\' incorrect_start_at=0 incorrect_end_at=0 span=\'谁\'\n```\n\n## 文檔\n### `Pipeline`\n- `__init__`\n    - `makers` = None : maker實例，可選\n    - `maker_weight` = None : maker被抽中的機率，可選\n\n- `__call__`\n    - `x` : 輸入句(str)，必需\n    - `k`=1 : 期待最多返回多少結果，可選\n    - `verbose`=True : debug 訊息，可選\n\n## 可用方法\n```python\nfrom zh_mistake_text_gen.data_maker import *\n```\n|Data Maker|Description|\n|---|---|\n|MissingWordMaker|隨機缺字|\n|MissingVocabMaker|隨機缺詞|\n|PronounceSimilarWordMaker|隨機相似字替換|\n|PronounceSimilarWordPlusMaker|編輯距離找發音相似並且用高頻字替換|\n|PronounceSimilarVocabMaker|發音相似詞替換|\n|PronounceSameWordMaker|發音相同字替換|\n|PronounceSameVocabMaker|發音相同詞替換|\n|RedundantWordMaker|隨機複製旁邊一個字作為沆於字|\n|RandomInsertVacabMaker|隨機插入詞彙|\n|MistakWordMaker|隨機替換字|\n|MistakeWordHighFreqMaker|隨機替換高頻字|\n|MissingWordHighFreqMaker|隨機刪除高頻字|',
    'author': 'Philip Huang',
    'author_email': 'p208p2002@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/p208p2002/zh-mistake-text-gen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
