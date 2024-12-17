import sqlalchemy as sa
import sqlalchemy.orm as so
from PatrickWilliamsWebsite import create_app, db
from PatrickWilliamsWebsite.models import Bees, Boxes

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Bees': Bees, 'Boxes': Boxes}
