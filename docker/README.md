# Docker Configuration for [patrick-williams.com](https://patrick-williams.com)

The `docker` directory contains a `Dockerfile`, an `entrypoint` script, and a `requirements.txt` file used to create a container image of my website.

The `Dockerfile` for this project does the following:

1. Creates the `/app/data` directory, which I eventually bind mount to the SQLite database.  
2. Copies the entrypoint script, `boot.sh` and `requirements.txt` from the `docker` directory into the image.  
3. Installs the dependencies listed in `requirements.txt` using `pip`.  
4. Copies the Flask application code, a dictionary file, the configuration file, and the `migrations` directory for the database into the image.  
5. Exposes the necessary port for the application.  
6. Sets the `entrypoint` script to run as the container starts.  

To build the container, I run:  

```bash
docker build -t image_name:tag --no-cache -f docker/Dockerfile .
```
replacing `image_name` with the name for the image and `tag` with a version number. I can then run the image by passing it relevant environment variables and bind mounting /app/data to the directory containing the SQLite database file.
