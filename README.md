# DB_Job-Positing-Analysis
원티드 채용 공고 및 트렌드 분석

## 1. 프로젝트 소개
직무별 채용 공고 내 키워드, 트렌드를 분석하여 인사이트를 도출 및 직무별로 필요한 역량을 그래프로 시각화하여 보여주는 크롬 익스텐션

## 2. 팀원
|<img src="https://avatars.githubusercontent.com/u/70475010?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/160251659?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/143946995?v=4" width="150" height="150"/>|
|:-:|:-:|:-:|
|Mina Kim<br/>[@eulneul](https://github.com/eulneul)|[@hwankatarinabluu](https://github.com/hwankatarinabluu)|[@Kimchaey](https://github.com/Kimchaey)|

|<img src="https://avatars.githubusercontent.com/u/122276734?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/83753041?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/158314564?v=4" width="150" height="150"/>|
|:-:|:-:|:-:|
|ahram_bae<br/>[@BARAM1NG](https://github.com/BARAM1NG)|Taewoong Lee<br/>[@taewoong1](https://github.com/taewoong1)|goodnanju<br/>[@NanjuJung](https://github.com/NanjuJung)|
## 3. 문제 정의
- 트렌드가 빠르게 변화하는 IT직군, 원하는 직무에 필요한 스킬과 부족한 역량 확인 필요
- 스킬이 직무에 잘 맞을 때, 직무 만족도가 높아질 것이라 기대
- 최신 기술을 트렌드에 맞춰 배운다 새로운 업무 환경에 빠르게 적응 가능
=>  채용 공고를 기반으로 키워드에 따라 직무별 요구되는 역량을 시각화하고, 크롬 익스텐션을 활용하여 사용자들에게 인사이트를 제공하기로 결정

## 4. 데이터 수집
![image](https://github.com/khuda-5th/DB_Job-Positing-Analysis/assets/70475010/32f0c811-ed33-4262-89c9-f7e894f6d0e3)

['원티드 - 일하는 사람들의 가능성'](https://www.wanted.co.kr/) 채용공고 크롤링 <br/>
- 31개 직군, 대략 1700개 채용 공고 수집 <br/>
[ 기업 이름, 포지션 상세, 주요 업무,자격 요건, 우대 사항, 복지]=>   총 5개의 Column 추출 

## 5. 데이터 분석
[1] TF-IDF를 통한 채용공고별 인사이트 도출 <br/>
![image](https://github.com/khuda-5th/DB_Job-Positing-Analysis/assets/70475010/da01ecc7-b8bc-4b54-90d9-50e6433f19a2)
![image](https://github.com/khuda-5th/DB_Job-Positing-Analysis/assets/70475010/8b8b54ce-3ecf-41cf-9922-b9e3800d2984)

[2] K-Means 클러스터링을 통한 개발 직군 역량 카테고리화
![image](https://github.com/khuda-5th/DB_Job-Positing-Analysis/assets/70475010/f6f3ffd6-035f-4b2e-b703-b8674f70478a)

## 6. 크롬 익스텐션
### 아키텍쳐
![KakaoTalk_20240526_025042171](https://github.com/khuda-5th/DB_Job-Positing-Analysis/assets/70475010/ce376dd4-2e94-40db-b307-370017333071)
### 데모 영상
[![Video Label](http://img.youtube.com/vi/ptW6cazMzdI/0.jpg)](https://youtu.be/ptW6cazMzdI)

