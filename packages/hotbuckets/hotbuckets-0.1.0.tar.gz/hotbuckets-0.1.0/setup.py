# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hotbuckets']
install_requires = \
['tomli>=1.0.1']

entry_points = \
{'console_scripts': ['htb = hotbuckets:main']}

setup_kwargs = {
    'name': 'hotbuckets',
    'version': '0.1.0',
    'description': 'Easily configure your network behavior on Linux (generates tc rules from a config)',
    'long_description': '# Intro\n\nTired of dealing with major & minor numbers? You like the TOML format (kind of "ini" on steroids)?\nAlways wanted to play with traffic shaping on linux but it turned too complex or confusing?\nThis alpha tool aims at simplifying the learning curve for traffic control on ip route 2.\n\nThe format started quite close to the original command-line and progressively adds more support and shorter or easier notations.\n\nForget about `classid`, `flowid`.\nConsider `parent` sometimes handle for `complex` scenarios only!\n\nCheck the *examples* folder to dive into the syntax.\n\n# Supported features\n\n- hosts aliases\n- network interfaces aliases\n- speeds aliases\n- automatic generation of major & minor mumbers (all of them!) when possible\n- visual representation of the setup\n\n## Trafic control coverage\n\n- sfq : makes a more fair traffic\n- netem : simulate network problems\n- htb : control traffic rate using categories\n- tbf : very basic shaping\n\n## QDiscs\n\n- sfq\n- netem\n- htb\n- tbf\n\n## Classes (categories uses by some QDiscs)\n\n- htb\n\n## Filters (assign traffic)\n\n- fw\n- u32\n  - ip (src, dst, sport, dport)\n- action\n\n# Installation\n\n    pip install hotbuckets\n\nYou can also directly download [the file](https://github.com/fdev31/hotbuckets/raw/main/hotbuckets.py), mark it executable adn run it.\n\nYou can optionally install `graphviz` to enable the `--show` action.\n\n# Usage\n\nCheck the [examples](https://github.com/fdev31/hotbuckets/tree/main/examples) for more usages.\n\nGiven the file:\n\n```ini\n[speeds]\nfull = "32mbit"\nhalf = "15mbit"\n\n[interfaces.nic]\ndev = "wlo1"\n\n[shape.base]\ndev = "nic"\ndefault = "baseline"\nceil = "full"\n\n[class.unlimited]\nparent = "base"\nrate = "full"\n\n[class."baseline"]\nparent = "unlimited"\nrate = "half"\nceil = "full"\n\n[shape.fairness]\nparent = "baseline"\ntype = "sfq"\nperturb = 10\n\n[class."web"]\nparent = "unlimited"\nrate = "half"\nceil = "full"\n\n[shape.fairness-web]\nparent = "web"\ntype = "sfq"\nperturb = 10\n\n[match.filtHttp]\nprotocol = "ip"\nparent = "base"\nfilters = "web"\nip = {dport="80"}\n\n[match.filtHttps]\nprotocol = "ip"\nparent = "base"\nfilters = "web"\nip = {dport="443"}\n```\n\nYou can use the command `htb configuration.toml` to get the following output:\n\n    #!/bin/bash\n    # Cleanup:\n    tc qdisc del dev wlo1 root\n    set -ex\n    # Rules:\n    tc qdisc add dev wlo1 root handle 1: htb default 2 # base\n    tc class add dev wlo1 parent 1: classid 1:1 htb rate 32mbit # unlimited\n    tc class add dev wlo1 parent 1:1 classid 1:2 htb rate 15mbit ceil 32mbit # baseline\n    tc class add dev wlo1 parent 1:1 classid 1:3 htb rate 15mbit ceil 32mbit # web\n    tc qdisc add dev wlo1 parent 1:2 handle 2: sfq perturb 10 # fairness\n    tc qdisc add dev wlo1 parent 1:3 handle 3: sfq perturb 10 # fairness-web\n    tc filter add dev wlo1 protocol ip parent 1: u32 match ip dport 80 0xffff flowid 1:3 # filtHttp\n    tc filter add dev wlo1 protocol ip parent 1: u32 match ip dport 443 0xffff flowid 1:3 # filtHttps\n\n\nYou can also use the `--show` parameter to get a representation like this:\n\n![graph](https://github.com/fdev31/hotbuckets/raw/main/examples/graph.png)\n\n## Misc notes\n\n- shapes are qdiscs, the "main" type of traffic control object, some can use classes\n- classes are used by some shapes to divide the traffic\n- match allows sending network traffic matching the rule to some shape\n- try to avoid using the same names in match and class, some cases are ambiguous\n\n# TODO\n\n- relative speeds (percents)\n- templates (for repeated attributes)\n\n',
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
