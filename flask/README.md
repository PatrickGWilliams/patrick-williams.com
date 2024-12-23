# Flask code for [patrick-williams.com](https://patrick-williams.com).

This directory contains the Flask code I wrote for my website. It ueses Python and Jinja templates to configure the website, and waitress to serve it. In order to not expose root, I put all of this inside a docker container and behind an nginx load balancer. 

The New York Times Letter Boxed helper is [Letter Box Helper](/../../blob/main/flask/PatrickWilliamsWebsite/app/lbHelper.py).
