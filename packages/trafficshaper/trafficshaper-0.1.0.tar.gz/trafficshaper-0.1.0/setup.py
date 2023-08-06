# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trafficshaper']
install_requires = \
['tomli>=1.0.1']

entry_points = \
{'console_scripts': ['htb = trafficshaper:main']}

setup_kwargs = {
    'name': 'trafficshaper',
    'version': '0.1.0',
    'description': 'Easily configure your network behavior on Linux (generates tc rules from a config)',
    'long_description': '# Intro\n\nTired of dealing with major & minor numbers? You like the TOML format (kind of "ini" on steroids)?\nAlways wanted to play with traffic shaping on linux but it turned too complex or confusing?\nThis alpha tool aims at simplifying the learning curve for traffic control on ip route 2.\n\nThe format started quite close to the original command-line and progressively adds more support and shorter or easier notations.\n\nForget about `classid`, `flowid`.\nConsider `parent` sometimes handle for `complex` scenarios only!\n\nCheck the *examples* folder to dive into the syntax.\n\n# Supported features\n\n- hosts aliases\n- network interfaces aliases\n- speeds aliases\n- automatic generation of major & minor mumbers (all of them!) when possible\n- visual representation of the setup\n\n## Trafic control coverage\n\n- sfq : makes a more fair traffic\n- netem : simulate network problems\n- htb : control traffic rate using categories\n- tbf : very basic shaping\n\n## TODO:\n\n- relative speeds (percents)\n- templates (for repeated attributes)\n\n## QDiscs\n\n- sfq\n- netem\n- htb\n- tbf\n\n## Classes (categories uses by some QDiscs)\n\n- htb\n\n## Filters (assign traffic)\n\n- fw\n- u32\n  - ip (src, dst, sport, dport)\n- action\n\n',
    'author': 'fdev31',
    'author_email': 'fdev31@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
