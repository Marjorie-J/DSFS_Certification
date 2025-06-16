# Portfolio de projets - Certification Data Science

Ce repository contient l’ensemble des projets réalisés dans le cadre de la certification RNCP35288 - Niveau 6 - Concepteur développeur en science des données.


## Liste des projets

Bloc 1 : Construction et alimentation d'une infrastructure de gestion de données
- Projet Kayak (Data Collection & Management Project)

Bloc 2 : Analyse exploratoire, descriptive et inférentielle de données
- Projet Speed dating (Exploratory Data Analysis Project)
- Projet Steam (Big Data Project)

Bloc 3 : Analyse prédictive de données structurées par l'intelligence artificielle
- Projet Walmart Sales (Supervised Machine Learning)
- Projet Conversion rate challenge (Supervised Machine Learning)
- Projet The North Face ecommerce (Unsupervised Machine Learning)

Bloc 4 : Analyse prédictive de données non-structurées par l'intelligence artificielle
- Projet AT&T (Deep Learning Project)

Bloc 5 : Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision
- Projet Getaround (Deployment Project)

Bloc 6 : Direction de projets de gestion de données
- Projet Anime Recommendation Engine (Final Project - NLP et systèmes de recommendation)


## Installation

1. Cloner le repository

```bash
git clone https://github.com/Marjorie-J/DSFS_Certification.git
cd DSFS_Certification
```

2. Créer un environnement

```bash
python -m venv dsfs_env
source dsfs_env/bin/activate
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```


## Précisions

Bloc 2 Steam : Projet réalisé sur Databricks avec PySpark

Bloc 4 AT&T : Projet réalisé sur Google Colab / Lightning AI afin d'entraîner des modèles de deep learning


## Structure du Repository

```
.
├── Bloc_1_Kayak/
│   ├── datas/
│   ├── maps/
│   ├── screenshots/
│   ├── src/
│   └── README.md
├── Bloc_2_Speed_Dating/
│   ├── datas/
│   ├── src/
│   └── README.md
├── Bloc_2_Steam/
│   ├── src/
│   └── README.md
├── Bloc_3_Conversion_Rate_Challenge/
│   ├── datas/
│   ├── src/
│   └── README.md
├── Bloc_3_The_North_Face/
│   ├── datas/
│   ├── src/
│   └── README.md
├── Bloc_3_Walmart/
│   ├── datas/
│   ├── src/
│   └── README.md
├── Bloc_4_AT&T/
│   ├── datas/
│   ├── src/
│   └── README.md
├── Bloc_5_GetAround/
│   ├── getaround-api/
│   ├── getaround-dashboard/
│   ├── getaround-mlflow/
│   ├── getaround-train-model/
│   └── README.md
├── Bloc_6_FinalProject/
│   ├── datas/
│   ├── notebook/
│   ├── pages/
│   ├── utils/
│   ├── app.py
│   ├── README.md
│   └── run.sh
├── README.md
└── requirements.txt