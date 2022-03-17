from flask import (
    render_template,  # render_template: To render html page
    jsonify,  # jsonify: To render json data
    request,  # request: To get data from front
    redirect,  # redirect: To redirect to another endpoint
)


def routes_browser(app):
    """
    Routes for the browser to navigate.
    """

    @app.route("/", methods=["GET", "POST"])  # Methods ["GET", "POST", ...so on]
    def home():
        if request.method == "GET":
            return render_template("index.html")

        else:
            # request.form => from form-data,  request.json => from json (raw)
            message = request.form.get("message") or request.json.get("message")

            if not message:
                return (
                    jsonify({"error": "No << message >> key found in the request"}),
                    400)

            return jsonify({"message": f"Your message is {message}"}), 200


    @app.route('/csv')
    def get_user_origin_as_csv_file():
        return redirect("static/output/users.csv", code=302)
