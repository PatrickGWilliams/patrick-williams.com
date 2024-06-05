from flask import Blueprint, flash, render_template, request
from flask_mailman import BadHeaderError, EmailMessage
from email_validator import validate_email, EmailNotValidError

bp = Blueprint("index", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        error=None
        message =request.form["Message"] 
        name = request.form["Name"]
        email =request.form["Email"] 
        info = message+" --"+name

        try:
            validate_email(email)
        except EmailNotValidError as e:
            error = str(e)
        else:
            msg = EmailMessage(
                email,
                info,
                "contact.Patrick.Williams@gmail.com",
                ["contact.Patrick.Williams@gmail.com"]
            )


        if error is None: 
            try:
                msg.send(fail_silently=False)
                error = "Thank you for contacting me"
            except BadHeaderError:
                error="Please enter only one valid email adress"

        else:
            flash(error)

        
    return render_template("index.html")
