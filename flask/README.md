# Flask code for [patrick-williams.com](https://patrick-williams.com).

This directory contains the Flask code I wrote for my website. It ueses Python and Jinja templates to configure the website, and waitress to serve it. In order to not expose root, I put all of this inside a docker container and behind an nginx load balancer. To make the project installable I run: 
```bash
python3 -m build
```
this puts the wheel file in the newly created `dist` directory. I then move the wheel file to the docker directory to build the image.

The New York Times Spelling Bee Solver is [PatrickWilliamsWebsite/spellingbeesolver.py](/../../blob/main/patwillsite/flask/PatrickWilliamsWebsite/spellingbeesolver.py).
