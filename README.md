# NLP

https://store.steampowered.com/ 에서 Metadata 및 Review 정보를 scrapping 하여 게임 유저에게  Recommendation System을 제공하는 것.

# 구성
1) scrapping_review.py - Selenium, BeatuifulSoup 를 이용한 Dynamic scrapping, Top scroll(x)
Steam내 게임의 Review를 scrapping , review 와 label을 concatenate하여 write , review의 scroll 내린 만큼 volume을 가져옴

2) scrapping_review_2.py - Selenium, BeatuifulSoup를 이용한 Dynamic scrapping, Top scroll(o)
Steam내 게임의 Review를 scrapping , review 와 label을 concatenate하여 write , Top scroll을 활용하여 최대한 scroll down을 하여 review를 가져옴

3) glove_steam_review.py - scikitlearn(feature_extraction; countVectorizer), glove, scipy(Cosine similarity)
1. Steam Review Text를 활용하여 glove을 활용한 Word preprocessing 진행
2. input : Abbreviation processing, Lemmatization된 Text
3. output : vectors size - 100 인 Wordvectors

4) Text_preprocessing.ipynb - NLTK
1. Scrapping Text를 Abbreviation Processing, Lemmatization, 여러가지 preprocessing 진행
2. input : Scrapping한 Steam Reviews Raw data
3. output : Preprocessig된 Steam Review text data
