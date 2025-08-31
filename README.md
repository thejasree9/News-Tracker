# News Tracker  

## Project Overview 
**News Tracker** is a Streamlit-based application that allows users to fetch, explore, and analyze the latest news articles using the **GNews API**.  
It provides an interactive interface to filter news by **categories, keywords, and country**, and presents the data in a user-friendly way.  
The project was built to simplify access to real-time news and offer insights into trends with visualization support.  

---

## Features  
- Fetch real-time news from **GNews API**.  
- Filter news by:
  - **Category** (Business, Sports, Technology, Health, Entertainment, etc.)  
  - **Country** (e.g., US, IN, UK, etc.)  
  - **Custom Keywords** (search anything).  
- Clean and responsive **Streamlit interface**.  
- Data displayed in **tabular format with clickable links**.  
- Error handling for invalid inputs or empty results.  
- Easy to extend for analytics, NLP, or sentiment analysis.  

---

## Project Structure  
```
news_app/
│── app.py
│── style.css
│── .streamlit/
│   └── secrets.toml
├── auth/
├── news/
├── nlp/
└── ui/
```

---

## Technologies Used  
- **Python 3.13.0**  
- **Streamlit** → for building the web interface.  
- **Requests** → for making API calls to GNews.  
- **Pandas** → for handling and displaying data.  
- **Plotly/Matplotlib** (optional) → for data visualization.  

---

## Project workflow  
1. Designed the app structure with **Streamlit** for rapid development.  
2. Integrated the **GNews API** to fetch real-time articles.  
3. Added filtering logic for category, country, and keyword search.  
4. Displayed results in an interactive table with article titles, descriptions, and links.  
5. Implemented error handling for API issues, missing API key, or empty search results.  
6. (Optional) Added **visualizations** such as word frequency and category-wise counts.  

---

## Algorithms & Important Libraries  
- **Requests** → to call the GNews API and parse JSON results.  
- **Pandas DataFrame** → to structure results (title, description, source, published date, URL).  
- **Counter from collections** → for word frequency analysis.  
- **Scikit-learn (optional)** → to filter stop words and analyze keywords.  
- **Plotly Express** → to visualize data (bar/pie charts).  

No heavy ML algorithm is used in this version, but the modular design allows easy integration of:  
- **NLP sentiment analysis**  
- **Topic modeling**  
- **Recommendation systems**  

---
## Usage
- Open the app, create account and then login 
- Select news categories, enter keywords, and choose a country.
- Click Fetch News to display the latest articles.
- Scroll through the list for news analysis and visualizations.


## Setup Guide 
1. **Clone the repository:**<br>
    ```
    git clone https://github.com/yourusername/news-tracker.git
    cd news-tracker
    ```
3. **Install dependencies globally:**<br>
    ```
   pip install -r requirements.txt
    ```
5. **Get your GNews API key:**
    Sign up at https://gnews.io/ and copy your API key.
6. **Create secrets.toml in the root directory:**<br>
    [api_keys]
    GNEWS_API_KEY = "YOUR_API_KEY_HERE"
7. **Run the app:**<br>
    ```
   streamlit run app.py
    ```
9.  Open your browser at:<br>
    http://localhost:8501



## Contributing
Contributions are welcome!
1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Description of changes"`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request





