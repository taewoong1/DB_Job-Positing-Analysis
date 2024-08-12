import pandas as pd
from konlpy.tag import Okt
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import re
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from collections import Counter
import nltk
import os

# nltk에서 영어 불용어 리스트 다운로드
nltk.download('stopwords')
english_stop_words = set(stopwords.words('english'))

# 한국어 불용어 리스트
korean_stop_words = set(['분', '우대', '개발', '경험', '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '를', '으로', '자', '에', '와', '한', '하다', '것', '지', '에서', '더',
    '중', '데', '그', '있', '하', '되', '수', '나', '그러나', '또', '물', '같', '등', '등등', '및', '이렇', '때', '또는', '말',
    '사람', '일', '때문', '이렇다', '저렇다', '이런', '저런', '그런', '저', '그', '아니', '없는', '무엇', '어떤', '왜', '어떻게', '있다',
    '합니다', '하여', '해야', '합니다', '하며', '그리고', '입니다', '그러므로', '그래서', '하지만', '그러나', '입니다', '이기', '합니다',
    '같이', '하기', '위해', '그렇기', '때문에', '때문', '하는', '어떤', '아래', '위해', '해서', '있습니다', '위한', '가장', '그런', '하며',
    '이런', '저런', '하며', '그럼', '또한', '됩니다', '이후', '그때', '그러면', '그래서', '그리고', '그런데', '따라서', '때문에', '하여', '하고',
    '에서', '그리고', '그때', '그럼', '그러면', '이것', '저것', '저희', '따라', '모두', '우리', '너희', '거기', '여기', '한번', '다시', '한번',
    '우리', '너희', '너희들', '우리들', '너', '저', '그', '나', '우리', '저희', '당신', '너희들', '이', '그', '저', '것', '해도', '되는',
    '않다', '할', '않는', '할', '않다', '일', '있다', '하나', '한', '무엇', '이', '사람', '등', '또한', '있다', '어느', '대해', '어떤',
    '합니다', '같다', '인', '위해', '해', '위한', '같다', '같이', '된', '있는', '하시는', '한', '가진', '무엇', '자기', '하는', '대해',
    '사람', '무엇', '하는', '인해', '할', '한다면', '할', '위해', '합니다', '그것', '여러', '있어', '나의', '할', '아래', '위해', '입니다',
    '되다', '대해', '되다', '않다', '할', '하는', '한', '이', '가', '있다', '저', '저희', '이', '그', '있다', '너희', '너희들', '이', '그',
    '있다', '않다', '할', '위해', '위한', '것', '있다', '같다', '합니다', '하며', '하여', '한', '않다', '같다', '위해', '할', '있다', '한',
    '해', '위한', '하는', '한', '같다', '이', '대해', '있다', '된', '된', '할', '않다', '할', '할', '한다면', '할', '합니다', '합니다', '된', '있습니다', '있는', '경험이', '있으신', '대한', '위한', '위해', '통해', '있는', '및', '서비스', '관련', '운영', '서비스를', '기술', '이상', '시스템', '관리', 'ai', '함께', '다양한', '데이터'])

# 합친 불용어 리스트
stop_words = korean_stop_words.union(english_stop_words)

def create_visualization(csv_file_path, output_directory):
    try:
        # CSV 파일 읽기
        print("Reading CSV file...")
        df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
        print("CSV file read successfully")

        # 불필요 열 제거 및 텍스트 합치기
        df['combined_text'] = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        print("Text combined")

        # 문장 분리 과정
        sentences = []
        for text in df['combined_text']:
            sentences.extend(re.split(r'\n|[.!?]', text))

        print("Sentences split:", len(sentences))

        # 형태소 분석기를 사용하여 명사 추출
        try:
            okt = Okt()
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            processed_sentences = [' '.join([word for word in okt.nouns(sentence) if word not in stop_words]) for sentence in sentences]
            print("Processed sentences:", len(processed_sentences))
        except Exception as e:
            print("Error with Okt processing:", e)
            return None

        # 문장 벡터화
        model = SentenceTransformer('jhgan/ko-sroberta-multitask')
        sentence_embeddings = model.encode(processed_sentences)
        print("Sentence embeddings created")

        # K-means 클러스터링
        kmeans = KMeans(n_clusters=7, random_state=42)
        kmeans_labels = kmeans.fit_predict(sentence_embeddings)
        print("K-means clustering done")

        # 클러스터 라벨링
        cluster_labels = {
            0: 'Software',
            1: 'Development',
            2: 'Problem Solving',
            3: 'Management',
            4: 'Business',
            5: 'Architecture/Network',
            6: 'Social'
        }

        df_sentences = pd.DataFrame({'Sentence': processed_sentences, 'Cluster': kmeans_labels})
        df_sentences['Category'] = df_sentences['Cluster'].map(cluster_labels)

        # 추가로 3개 라벨링
        category_mapping = {
            'Development': 'System Skill',
            'Problem Solving': 'System Skill',
            'Social': 'Business Skill',
            'Business': 'Business Skill',
            'Management': 'Business Skill',
            'Software': 'Technical Skill',
            'Architecture/Network': 'Technical Skill'
        }

        df_sentences['Final Category'] = df_sentences['Category'].map(category_mapping)
        print("Category mapping done")

        # 노이즈 제거 (클러스터 분류 안된 값)
        filtered_df = df_sentences[df_sentences['Final Category'] != 'Other']
        filtered_embeddings = sentence_embeddings[filtered_df.index]

        # 실루엣 점수 계산 (클러스터 정확성 파악)
        silhouette_avg = silhouette_score(filtered_embeddings, filtered_df['Final Category'].astype('category').cat.codes)
        print(f'Silhouette Score for filtered data: {silhouette_avg}')

        # 최종 계산 
        final_category_counts = filtered_df['Final Category'].value_counts()
        total_count = len(filtered_df)
        final_category_ratios = (final_category_counts / total_count) * 100
        print("Filtered Category Ratios:")
        print(final_category_ratios)

        # 점검용 - 각 클러스터의 주요 키워드 및 문장 확인
        for cluster_num in range(7):
            cluster_sentences = df_sentences[df_sentences['Cluster'] == cluster_num]['Sentence']
            cluster_terms = ' '.join(cluster_sentences).split()
            most_common_terms = Counter(cluster_terms).most_common(10)
            print(f"Cluster {cluster_num} most common terms: {most_common_terms}")
            print(f"Example sentences from cluster {cluster_num}:")
            print(cluster_sentences.sample(3).values)
            print()
        print("final_category_ratios: ",final_category_ratios)
        
        labels = ['Technical Skill', 'System Skill', 'Business Skill']

        # 해당 기업 비율 계산된거 받아오는 거 
        current_data = [
            round(final_category_ratios.get('Technical Skill', 0), 1),
            round(final_category_ratios.get('System Skill', 0), 1),
            round(final_category_ratios.get('Business Skill', 0), 1)
        ]
        all_data = [38.8, 32.8, 28.4]  # 데사 전체(얘는 임의로 수정해줘야 함)

        x = np.arange(len(labels))  # 라벨의 위치
        width = 0.22  

        fig, ax = plt.subplots(figsize=(12, 8))

        # 위치 조정
        rects1 = ax.bar(x - width/1.5, all_data, width, label='Data Scientist_All', edgecolor='black', color='lightgreen', linewidth=1.5)
        rects2 = ax.bar(x + width/1.5, current_data, width, label='Current Corporate', color='red', edgecolor='black', linewidth=1.5)

        # 퍼센트 표시
        for rect in rects1:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=12)

        for rect in rects2:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=12, color='black')

        # 그래프 라벨과 제목 설정
        ax.set_xlabel('<Class>')
        ax.set_ylabel('<Percentage>')
        ax.set_title('Class Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(fontsize =14)


        # 이미지 파일 저장 경로 설정 및 생성
        image_path = os.path.join(output_directory, 'visualization.png')
        print(f"Saving image to: {image_path}")
        plt.savefig(image_path)
        plt.close()

        if os.path.exists(image_path):
            print(f"Image successfully saved to: {image_path}")
        else:
            print("Failed to save image.")

        return image_path

    except Exception as e:
        print("Error during visualization:", e)
        return None
