from flask import Flask, request
from flask_cors import CORS
from visualization import crawling_all

app = Flask(__name__)
CORS(app)

@app.route('/send_url', methods=['POST', 'OPTIONS'])
def receive_url():
    if request.method == 'OPTIONS':
        return {}, 200  # OPTIONS 요청에 대해 200 OK 응답

    data = request.json
    if 'url' in data:
        received_url = data['url']
        print("Received URL:", received_url)
        try:
            list_sheet = crawling_all(received_url)
            if list_sheet:  # 데이터가 실제로 존재하는지 확인
                print("Crawled Data:", list_sheet)
                return 'URL received and data crawled successfully', 200
            else:
                print("No data crawled.")
                return 'Crawled data is empty', 204  # No Content
        except Exception as e:
            print("Error during crawling:", e)
            return 'Error in data crawling', 500
    else:
        return 'No URL provided', 400

if __name__ == '__main__':
    app.run(debug=True)
