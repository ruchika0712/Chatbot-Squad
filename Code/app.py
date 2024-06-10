from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = "static"

import json
import re
import string
import random
import torch
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering


def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_squad_dataset(squad_data):
    knowledge_base = []

    for article in squad_data["data"]:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]
            context = preprocess_text(context)

            for qa in paragraph["qas"]:
                question = qa["question"]
                question = preprocess_text(question)

                if "plausible_answers" in qa:
                    if len(qa["plausible_answers"]) == 0:
                        continue
                    answer_text = qa["plausible_answers"][0]["text"]
                else:
                    answer_text = qa["answers"][0]["text"]

                answer_text = preprocess_text(answer_text)

                knowledge_base.append(
                    {
                        "question": question,
                        "answer": answer_text,
                        "context": context,
                    }
                )

    return knowledge_base


file_url_train = "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json"
file_url_dev = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json"

response_train = requests.get(file_url_train)
response_dev = requests.get(file_url_dev)

squad_train_data = response_train.json()
squad_dev_data = response_dev.json()

# Combine train and dev data
squad_train_data["data"].extend(squad_dev_data["data"])

# Preprocess the SQuAD dataset and create a knowledge base
knowledge_base = preprocess_squad_dataset(squad_train_data)

# Create a TF-IDF vectorizer and matrix for the knowledge base
questions = [qa["question"] for qa in knowledge_base]
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(questions)


def retrieve_answer(user_question, faq_database, similarity_threshold=0.6):
    for faq in faq_database:
        if user_question.lower() in faq["question"].lower():
            return faq["answer"]

    user_question_tfidf = tfidf_vectorizer.transform([preprocess_text(user_question)])
    similarity_scores = tfidf_matrix.dot(user_question_tfidf.T).toarray().flatten()
    most_similar_index = similarity_scores.argmax()

    print(f"User Question: {user_question}")
    print(f"Similarity Scores: {similarity_scores}")
    print(f"Most Similar Index: {most_similar_index}")

    if similarity_scores[most_similar_index] > similarity_threshold:
        return knowledge_base[most_similar_index]["answer"]
    else:
        return "I'm sorry, I don't have a specific answer to that question."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["user_question"]
    answer = retrieve_answer(user_question, knowledge_base)

    return render_template("answer.html", question=user_question, answer=answer)


@app.route("/get", methods=["GET"])
def get_response():
    user_question = request.args.get("msg")
    answer = retrieve_answer(user_question, knowledge_base)
    return answer


if __name__ == "__main__":
    app.run(debug=True)
