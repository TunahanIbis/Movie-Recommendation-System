# Movie Recommendation System

This project is a **Movie Recommendation System** that suggests movies based on user preferences. The system uses content-based filtering and machine learning to provide personalized recommendations. It is built using **Flask** for the backend, **HTML/CSS/JavaScript** for the frontend, and leverages **joblib** for loading pre-trained models.

## Features

- **Random Movie Selection**: The system selects a random set of 10 movies from the dataset.
- **Personalized Recommendations**: The app recommends 3 movies based on the 3 movies selected by the user. The system uses pre-trained models here.
- **Cosine Similarity and Content Based Filtering**: The system uses machine learning models to calculate similarities between movies based on their genre, overview, and release year.
  
## Demo

Check out the demo of the Movie Recommendation System here:

[![Demo Video on YouTube](https://img.youtube.com/vi/RQq0XiE4nj4/0.jpg)](https://www.youtube.com/watch?v=RQq0XiE4nj4)

## Installation

To get started with this project locally, follow these steps:

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Step 1: Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/TunahanIbis/Movie-Recommendation-System.git
cd movie-recommendation-system
```

### Step 2: Install dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Flask app

Start the Flask development server:

```bash
python src/app.py
```

This will start the backend server, and you can access the Movie Recommendation System locally by visiting http://127.0.0.1:5000/ in your browser.

## Folder Structure

Your project folder will look like this:

```bash
movie-recommendation-system/
├── src/
│   └── app.py                # Flask backend application
    └── ML Model.py           # ML code that dumps the pkl files
├── data/
│   └── models/               # Folder with pre-trained models (e.g., .pkl files)
│   └── json/                 # Folder with JSON movie data
├── templates/                # HTML file
    └── index.html
├── static/                   
    └── css/                  # CSS file  
        └── styles.css 
    └── images/               # Image file
    └── js/                   # JS file
        └── app.js
```
