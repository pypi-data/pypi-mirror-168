# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfgman', 'cfgman.loaders']

package_data = \
{'': ['*']}

install_requires = \
['apischema>=0.17.5,<0.18.0', 'pytest>=7.1.3,<8.0.0']

extras_require = \
{'all': ['PyYAML>=6.0,<7.0', 'tomli>=2.0.1,<3.0.0'],
 'toml': ['tomli>=2.0.1,<3.0.0'],
 'yaml': ['PyYAML>=6.0,<7.0']}

setup_kwargs = {
    'name': 'cfgman',
    'version': '0.1.0a0',
    'description': 'Configuration manager made easy.',
    'long_description': '# cfgman\n\nA configuration manager for Python application.\n\n## Features\n\n- Configure from files (yaml, toml, json).\n- Environment variables.\n- Custom variables (e.g. command line arguments).\n- Type annotations.\n\n## Usage\n\n```python\nfrom cfgman import (\n    configclass,\n    load_config,\n    get_default_config,\n    env_loader,\n    file_loader,\n    MISSING,\n)\nfrom apischema.metadata import conversion\n\n\ndef from_isoformat(s: str) -> datetime:\n    return datetime.fromisoformat(s)\n\n\ndef to_isoformat(d: datetime) -> str:\n    return d.isoformat()\n\n\n@configclass\nclass WebServerConfig:\n    host: str = "localhost"\n    port: int = 80\n    timeout: int = 30\n\n\n@configclass\nclass Config:\n    web: WebServerConfig  # nest configs\n    start: datetime = field(\n        default_factory=lambda: datetime.now(datetime.utc),\n        metadata=conversion(from_isoformat, to_isoformat),\n    )\n\n\nargparser = ArgumentParser(Config)\nargparser.add_argument(\n    "-c",\n    "--config",\n    dest="config_files",\n    metavar="FILENAME",\n    action="append",\n    default=["~/.config/myapp/config.yaml"],\n)\nargparser.add_argument("--host", metavar="HOSTNAME", default=MISSING)\nargparser.add_argument("-p", "--port", metavar="PORT", type=int, default=MISSING)\nargparser.add_argument("-s", "--start", metavar="ISODATETIME", default=MISSING)\nargs = argparser.parse_args()\n\nconfig = load_config(\n    Config,\n    file_loader(\n        files=args.config_files, supported_formats=(FileFormat.YAML, FileFormat.TOML)\n    ),\n    env_loader(\n        prefix="APP_",\n        mapping={"HOST": "web.host", "PORT": "web.port"},\n    ),\n    {\n        "web": {\n            "host": args.host,\n            "port": args.port,\n        },\n        "start": args.start,\n    },\n)\n\ntime.sleep((datetime.now(datetime.utc) - config.start).total_seconds)\n\n\nasync def run_server():\n    # you can retrieve your module specific config without depending on the rest of the configuration\n    webconfig = get_default_config(WebServerConfig)\n    server = start_server(webconfig.host, webconfig.port)\n    await server.serve_forever()\n\n\nasync def request_handler(request):\n    experiment = select_experiment()\n    with replace_default(WebServerConfig, changes=experiment.changes):\n        webconfig = get_default_config(WebServerConfig)\n        response = await prepare_response(\n            headers={"X-Experiment-Name": webconfig.experiment}\n        )\n```\n',
    'author': 'Maurizio Sambati',
    'author_email': 'maurizio@skicelab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://duilio.github.io/cfgman/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
