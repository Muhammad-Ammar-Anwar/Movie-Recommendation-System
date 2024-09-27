# Movie Recommender System with Streamlit

This project is a movie recommendation system that uses TMDb data and content based filtering, with a simple and interactive frontend powered by **Streamlit**. It preprocesses movie data such as genres, cast, crew, and keywords, and recommends similar movies based on cosine similarity.

![Frontend Screenshot](https://github.com/Muhammad-Ammar-Anwar/Movie-Recommendation-System/blob/main/frontend%202.png)


## Features

- **Data Processing**: Extracts and processes movie metadata (genres, cast, crew, keywords).
- **Recommendation Engine**: Uses cosine similarity to find and recommend movies based on user input.
- **Streamlit Interface**: A user-friendly web interface for selecting movies and receiving recommendations.
- **Pre-trained Model**: Stores processed movie data and similarity matrix using pickle for faster load times.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Muhammad-Ammar-Anwar/Movie-Recommendation-System.git
    cd movie-recommender
    ```

2. **Install dependencies**:
    Make sure you have Python installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **API Key Setup**:
    - Create a `.env` file in the root directory.
    - Add your TMDb API key in the following format:
      ```
      api_key=YOUR_TMDB_API_KEY
      ```

4. **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

5. **Download Required Data**:
    Ensure you have the following files:
    - `movies_dict.pkl`: Contains preprocessed movie data.
    - `similarity.pkl`: Contains the similarity matrix for movie recommendations.

    If not, the app will automatically attempt to download `similarity.pkl` from Google Drive.

## How It Works

1. The app loads preprocessed movie data, including genres, cast, crew, and keywords.
2. Users select a movie title from the dropdown menu.
3. The system calculates cosine similarity between the selected movie and others.
4. The app displays the top 5 recommended movies with their respective titles.

## Dependencies

- Streamlit
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Pickle
- TMDb API

## Example Usage

1. Select a movie from the dropdown.
2. Click "Recommend" to get a list of similar movies.
3. Movie recommendations are displayed along with their titles.






---

### Author

**Muhammad Ammar Anwar**  
https://github.com/your-username](https://github.com/Muhammad-Ammar-Anwar
