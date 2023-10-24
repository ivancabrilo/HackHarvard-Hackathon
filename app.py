
# from flask import Flask, render_template, request, jsonify
# import openai
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)


# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/get_bot_response", methods=["POST"])
# def get_bot_response():
#     data = request.json
#     user_message = data.get("message")

#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": user_message},
#         ]
#     )

#     bot_response = completion.choices[0].message["content"]
#     return jsonify({"content": bot_response})

# @app.route("/log_conversation", methods=["POST"])
# def log_conversation():
#     data = request.json
#     user_message = data.get("message")
#     bot_response = data.get("bot_response")
#     feedback = data.get("feedback")
#     print(bot_response)

#     with open("conversation_logs.txt", "a") as file:
#         file.write(f"User Input: {user_message}\n")
#         file.write(f"Bot Output: {bot_response}\n")
#         file.write(f"Feedback: {feedback}\n\n")

#     return jsonify({"status": "OK"})

# if __name__ == '__main__':
#     app.run()


from flask import Flask, render_template, request, jsonify
import openai
from flask_cors import CORS
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor


app = Flask(__name__)
CORS(app)

openai.api_key = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ['DATABASE_URL']


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_bot_response", methods=["POST"])
def get_bot_response():
    data = request.json
    user_message = data.get("message")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message},
        ]
    )

    bot_response = completion.choices[0].message["content"]
    return jsonify({"content": bot_response})


@app.route("/log_conversation", methods=["POST"])
def log_conversation():
    data = request.json
    user_message = data.get("message")
    bot_response = data.get("bot_response")
    feedback = data.get("feedback")

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor(cursor_factory=DictCursor)

    try:
        cursor.execute(
            "INSERT INTO conversation_logs (user_message, bot_response, feedback) VALUES (%s, %s, %s)",
            (user_message, bot_response, feedback)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run()
