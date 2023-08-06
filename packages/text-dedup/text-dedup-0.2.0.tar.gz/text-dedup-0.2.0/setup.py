# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup',
 'text_dedup.base',
 'text_dedup.exact_dedup',
 'text_dedup.exact_dedup.suffix_array',
 'text_dedup.near_dedup',
 'text_dedup.near_dedup.minhash',
 'text_dedup.near_dedup.simhash',
 'text_dedup.postprocess',
 'text_dedup.preprocess',
 'text_dedup.semantic_dedup',
 'text_dedup.utils',
 'text_dedup.utils.hf_datasets',
 'text_dedup.utils.storage']

package_data = \
{'': ['*']}

install_requires = \
['annoy>=1.17.1,<2.0.0',
 'datasets>=2.4.0,<3.0.0',
 'datasketch>=1.5.8,<2.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'mpire>=2.6.0,<3.0.0',
 'numpy>=1.23.2,<2.0.0',
 'redis>=4.3.4,<5.0.0',
 'rich>=12.5.1,<13.0.0',
 'scipy==1.9.1',
 'sentence-transformers>=2.2.2,<3.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'torch>=1.12.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.21.2,<5.0.0',
 'xxhash>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.2.0',
    'description': 'All-in-one text deduplication',
    'long_description': '# text-dedup\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/cc66178e49d24908ac1fb2b2dbe4e5b3)](https://www.codacy.com/gh/ChenghaoMou/text-dedup/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/text-dedup&utm_campaign=Badge_Coverage) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc66178e49d24908ac1fb2b2dbe4e5b3)](https://www.codacy.com/gh/ChenghaoMou/text-dedup/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/text-dedup&utm_campaign=Badge_Grade)\n\n\n## Features\n\n-   Hash-based methods such as [SimHash](https://www.cs.princeton.edu/courses/archive/spring04/cos598B/bib/CharikarEstim.pdf), [MinHash](https://web.archive.org/web/20150131043133/http://gatekeeper.dec.com/ftp/pub/dec/SRC/publications/broder/positano-final-wpnums.pdf) + [LSH](http://infolab.stanford.edu/~ullman/mmds.html) for near deduplication.\n-   [SuffixArray](http://dl.acm.org/citation.cfm?id=320176.320218)-based method from [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499) for substring exact deduplication.\n-   In-memory or [Redis](https://redis.io)/[KeyDB](https://docs.keydb.dev)-cached index to handle larger than memory datasets.\n\n## Documentation\n\n[Github Pages](https://chenghaomou.github.io/text-dedup/index.html)\n\n## Todos\n-   [ ] Memory benchmark for streaming processing\n-   [ ] Speed benchmark for in-memory processing\n-   [ ] Inter-dataset deduplication\n-   [ ] Rewrite suffix array in Python\n\n## Thanks\n\n-   [seomoz/simhash-cpp](https://github.com/seomoz/simhash-cpp)\n-   [datasketch](http://ekzhu.com/datasketch/index.html)\n-   [google-research/deduplicate-text-datasets](https://github.com/google-research/deduplicate-text-datasets)\n-   Developed with OSS license from [JetBrains](https://jb.gg/OpenSourceSupport)\n-   This project is heavily influenced by the deduplication work at BigScience workshop. The original code can be found at [bigscience-workshop/data-preparation](https://github.com/bigscience-workshop/data-preparation/tree/main/preprocessing/filtering/deduplicate).\n',
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
