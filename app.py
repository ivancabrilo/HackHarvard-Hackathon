
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

app = Flask(__name__)
CORS(app)



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



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
    print(bot_response)

    with open("conversation_logs.txt", "a") as file:
        file.write(f"User Input: {user_message}\n")
        file.write(f"Bot Output: {bot_response}\n")
        file.write(f"Feedback: {feedback}\n\n")

    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run()
