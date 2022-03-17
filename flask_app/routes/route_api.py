from flask import request, jsonify  # jsonify: To render json (API REST)


from ..logic.papybot import PapyBot


def routes_api(app):
    """
    Routes to consumn the api.
    """

    @app.route("/api", methods=["GET"])
    def papybot():
        question = request.args.get("question")
        if not question:
            return (jsonify({"message": "Il faut me poser une question"}), 400)

        user_ip_address = request.remote_addr
        response_from_papybot, status = PapyBot.start(question, user_ip_address)

        return jsonify({"message": response_from_papybot}), status
