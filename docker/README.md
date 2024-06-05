# Docker configuration for [patrick-williams.com](https://patrick-williams.com).

The Dockerfile takes the wheel file from the Flask directory and installs it in a container. It also places a directory (not included in this  repository) containing, a configuration file holding secrets and the word list (for the spelling bee solver) in a location where Flask can reach it. To build the container I run: 
```bash
docker build -t image_name:tag .
```
replacing image_name with the name for the image and tag with a version number. To run the image and make it accessible on port 8024 I run:
```bash
docker run -d -p 8024:8041 image_name:tag
```
I can then access it at 127.0.0.1:8024 on a web browser.
