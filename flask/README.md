# Flask Code for [patrick-williams.com](https://patrick-williams.com)

The `flask` directory contains the core Flask application code and supporting files for my website. It uses Python and Jinja templates to build and serve dynamic content, with `waitress` as the WSGI server.

### Key Components:
- **Flask Application Code**: Located in the `PatrickWilliamsWebsite` directory, it includes the views, templates, and utilities such as the New York Times Letter Boxed helper ([`lbHelper.py`](../../blob/main/flask/PatrickWilliamsWebsite/app/lbHelper.py)).  
- **SQLAlchemy/Alembic Migrations**: The `migrations` directory contains database migration scripts for SQLAlchemy.  
- **Configuration**: A configuration file defines settings for the Flask app.  

### Deployment:
The application runs inside a Docker container to isolate it from the host environment. It is served behind an Nginx load balancer for added security and scalability. 
