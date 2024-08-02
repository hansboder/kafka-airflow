from flask import Flask, request, jsonify
import config
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'))
app.logger.addHandler(console_handler)

settings = config.Settings()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    app.logger.info(f'Received request with body: {data}')

    issue_title = data.get('title')
    issue_body = data.get('commonAnnotations').get('description')

    url = settings.github_url
    pat = settings.github_pat

    response = requests.post(url, headers={'Authorization': f'token {pat}'}, json={
        'title': issue_title,
        'body': issue_body,
    })


    if response.status_code != 201:
        app.logger.error(f'Failed to create issue. Status code: {response.status_code}, Response: {response.text}')
        return jsonify({'status': 'Failed to create issue'}), response.status_code
    else:
        return jsonify({'status': 'Issue created successfully'}), 201


if __name__ == '__main__':
    app.logger.info("starting alert proxy")
    app.run(port=5000)