# from flask import Flask, render_template, request, jsonify
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.pipeline import make_pipeline

# app = Flask(__name__)

# TRAIN_TEXTS = [
#     "I love this product, it works great and exceeded my expectations.",
#     "Amazing service and friendly staff.",
#     "This made my day — absolutely wonderful experience!",
#     "Highly recommend to everyone.",
#     "Fantastic quality and fast delivery.",
#     "Very satisfied with the purchase.",
#     "Great value for money.",
#     "Excellent! Will buy again.",
#     "Superb performance and easy to use.",
#     "Perfect, exactly what I needed!",
#     "I hate this, it broke after one use.",
#     "Terrible experience, will never use again.",
#     "Very disappointed with the quality.",
#     "Waste of money and time.",
#     "Slow service and rude staff.",
#     "Not worth the price.",
#     "Worst purchase ever.",
#     "I will not recommend this to anyone.",
#     "Broke within a week, extremely poor build.",
#     "Awful — completely useless.",
#     "The product is okay, nothing special.",
#     "It does the job but could be better.",
#     "Average experience overall.",
#     "Not bad, not great.",
#     "It arrived on time and functions as expected.",
#     "Mixed feelings about this purchase.",
#     "The UI is fine but needs improvements.",
#     "Works as described, no extra features.",
#     "I neither liked nor disliked it.",
#     "Decent for the price."
# ]
# TRAIN_LABELS = [1]*10 + [-1]*10 + [0]*10

# model = make_pipeline(
#     TfidfVectorizer(max_features=5000, ngram_range=(1,2)),
#     LogisticRegression(solver='liblinear')
# )
# model.fit(TRAIN_TEXTS, TRAIN_LABELS)

# LABEL_MAP = {1: 'Positive', 0: 'Neutral', -1: 'Negative'}

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json() or {}
#     text = data.get('text', '')
#     if not text.strip():
#         return jsonify({'error': 'Please enter some text.'}), 400
#     pred = model.predict([text])[0]
#     label = LABEL_MAP.get(pred, 'Unknown')
#     return jsonify({'label': label})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_from_directory
from textblob import TextBlob
import os

app = Flask(__name__)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for analyzing sentiment
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    if not text.strip():
        return jsonify({'sentiment': 'Neutral'})

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = 'Positive'
    elif polarity < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return jsonify({'sentiment': sentiment})


# Route for favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

if __name__ == '__main__':
    if not os.environ.get("VERCEL"):
        app.run(debug=True)

