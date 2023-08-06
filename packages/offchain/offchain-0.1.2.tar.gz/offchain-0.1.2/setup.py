# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offchain',
 'offchain.base',
 'offchain.constants',
 'offchain.logger',
 'offchain.metadata',
 'offchain.metadata.adapters',
 'offchain.metadata.constants',
 'offchain.metadata.fetchers',
 'offchain.metadata.models',
 'offchain.metadata.parsers',
 'offchain.metadata.parsers.catchall',
 'offchain.metadata.parsers.collection',
 'offchain.metadata.parsers.schema',
 'offchain.metadata.pipelines',
 'offchain.metadata.registries',
 'offchain.web3']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0',
 'python-json-logger>=2.0.4,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'urllib3>=1.26.11,<2.0.0',
 'web3>=5.30.0,<6.0.0']

setup_kwargs = {
    'name': 'offchain',
    'version': '0.1.2',
    'description': 'Open source metadata processing framework',
    'long_description': '# offchain\n\n[Documentation](https://ourzora.github.io/offchain/) | [Zora API](https://api.zora.co)\n\n---\n\n`offchain` is a library for parsing NFT metadata. It\'s used by Zora\'s indexer & API.\nIt can handle metadata of many standards (OpenSea, ZORA, Nouns), hosted in many places (ipfs, http, dataURIs),\nand normalize them into a consistent format.\n\nOur goal with this project is to democratize access to NFT metadata.\n\n```shell\npip install offchain\n```\n\n```python\nfrom offchain import MetadataPipeline, Token\n\npipeline = MetadataPipeline()\ntoken = Token(\n    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",\n    token_id=9559\n)\nmetadata = pipeline.run([token])[0]\n\nmetadata.name               # -> \'antares the improbable\'\nmetadata.description        # -> \'You are a WITCH who bathes in the tears of...\'\nmetadata.standard           # -> OPENSEA_STANDARD\nmetadata.attributes         # -> [Attribute(trait_type=\'Skin Tone\', ...]\nmetadata.image              # -> MediaDetails(size=2139693, sha256=None, uri=\'https://cryptocoven.s3.amazonaws.com/2048b255aa1d02045eef13cdd7100479.png\', mime_type=\'image/png\')\nmetadata.additional_fields  # -> [MetadataField(...), ...]\n```\n\nSee [documentation](https://ourzora.github.io/offchain/) for more examples and tutorials.\n\n## Contributing\n\nWe welcome contributions that add support for new metadata standards, new ways of retreiving metadata, and ways of normalizing them to a consistent form.\nWe are commited to integrating contributions to our indexer and making the results available in our API.\n\nYou should be able to contribute a new standard for metadata, and have NFTs that adhere to that metadata standard\nbe returned correctly from queries to `api.zora.co`. We hope this helps to foster innovation in how\nNFTs are represented, where metadata is stored, and what is expressed in that metadata.\n\n## Features\n\n- Multiple metadata standards: represent metadata any way you wish\n- Multiple transport protocols: store metadata where you want\n- Composible for custom applications: only parse the standards you care about\n- Future proof: extensible to new formats, locations, etc. The more gigabrain the better.\n\n## Development\n\nThis project is developed using Python 3.9. Here\'s a recommended setup:\n\n### Poetry\n\nThis project uses `poetry` for dependency management and packaging. Install poetry:\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\n### Setup\n\n```bash\npoetry install\n```\n\n### Pre-commit\n\nPre-commit runs checks to enforce coding standards on every commit\n\n```\npip install pre-commit  # into global python path\npre-commit install\n```\n\n### Testing\n\n```bash\npoetry run python -m pytest tests/\n```\n\n### Documentation\n\nThis project uses `mkdocs` and `mkdocs-material` for documentation.\n\n```bash\npoetry run mkdocs serve\n```\n',
    'author': 'Zora eng',
    'author_email': 'eng@zora.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
