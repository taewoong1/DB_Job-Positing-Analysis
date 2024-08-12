from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import os
from crawler import crawling_all
from visualization import create_visualization

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

                # 데이터프레임으로 변환
                df = pd.DataFrame(list_sheet, columns=['공고이름', '기업이름', '포지션설명', '주요업무', '자격요건', '우대사항', '복지'])

                # 디렉토리 확인 및 생성
                directory = r'mnt/data'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                # CSV 파일로 저장
                csv_file_path = os.path.join(directory, 'job_postings.csv')
                try:
                    df.to_csv(csv_file_path, encoding='utf-8-sig', index=False)
                    print(f"CSV file saved to: {csv_file_path}")
                except Exception as e:
                    print(f"Error saving CSV file: {e}")
                    return jsonify({'error': 'Failed to save CSV file'}), 500
                
                # CSV 파일 경로를 시각화 모듈에 전달하여 시각화 이미지 생성
                image_path = create_visualization(csv_file_path, directory)
                
                if image_path and os.path.exists(image_path):
                    # 시각화 이미지 반환
                    print(f"Sending image file: {image_path}")
                    return send_file(image_path, mimetype='image/png'), 200
                else:
                    print("Image file not found.")
                    return jsonify({'error': 'Image file not found'}), 500
            else:
                print("No data crawled.")
                return 'Crawled data is empty', 204  # No Content
        except Exception as e:
            print(f"Error during crawling or visualization: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return 'No URL provided', 400

if __name__ == '__main__':
    app.run(debug=True)
