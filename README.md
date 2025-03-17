# Steam Analytics: Analyzing Price, Playtime, Game Ownership, and Reviews
![steam](https://store.cloudflare.steamstatic.com/public/shared/images/responsive/steam_share_image.jpg)

## Overview
This project analyzes how price, playtime, and game ownership influence the likelihood of leaving a positive review on Steam. Using data extracted from the Steam API, we examine consumer behavior, trends in gaming preferences, and review sentiment.

This research was conducted as part of the Marketing Analytics Master's Program at Tilburg University.

---

## Research Questions
1. Does higher price lead to more positive reviews?  
2. Does longer playtime result in more positive reviews?  
3. Do users who own more games tend to leave more critical reviews?  

---

## Repository Structure
```
├── README.md
├── .gitignore
├── 1-notebooks
│   ├── analysis.ipynb
│   ├── get_app_details.ipynb
│   ├── get_app_reviews.ipynb
│   ├── libraries_and_function.ipynb
│   ├── merging_and_cleaning.ipynb
│   ├── plots.ipynb
│
├── 2-data
│   ├── search_results_20250302/
│   │   ├── globaltopsellers_20250302.csv
│   │   ├── globaltopsellers_reviews_20250302.csv
│   │
│   ├── search_results_20250303/
│   │   ├── globaltopsellers_20250303.csv
│   │   ├── globaltopsellers_reviews_20250303.csv
│   │
│   ├── search_results_20250304/
│   │   ├── globaltopsellers_20250304.csv
│   │   ├── globaltopsellers_reviews_20250304.csv
│   │
│   ├── search_results_20250305/
│   │   ├── globaltopsellers_20250305.csv
│   │   ├── globaltopsellers_reviews_20250305.csv
│   │
│   ├── search_results_20250306/
│   │   ├── globaltopsellers_20250306.csv
│   │   ├── globaltopsellers_reviews_20250306.csv
│   │
│   ├── search_results_20250307/
│   │   ├── globaltopsellers_20250307.csv
│   │   ├── globaltopsellers_reviews_20250307.csv
│   │
│   ├── search_results_20250308/
│       ├── globaltopsellers_20250308.csv
│       ├── globaltopsellers_reviews_20250308.csv
│
├── 3-visuals
│   ├── avg_playtime_genre.png   # average playtime per genre
│   ├── genre.jpg                # distribution of games by genre
│   ├── mean_reviews.png         # average number of reviews per game
│   ├── numgames.jpg             # number of games owned vs. review sentiment
│   ├── playtime.png             # correlation between playtime and review positivity
│   ├── reviews.jpg              # total number of reviews per game
│   ├── reviewscore.jpg          # distribution of review scores

```

---

## Data Collection & Methodology
### **1. Data Source**
We used the **Steam API** to extract data because of its **extensive coverage** of PC gaming trends and publicly available review metrics.

**Endpoints Used:**
- `/search/results/` → Fetches top-selling game IDs
- `/api/appdetails/` → Extracts game metadata (price, genre, platform)
- `/appreviews/` → Retrieves user reviews, playtime, and sentiment

**Sampling Approach:**
- **200 top-selling games** were tracked over **seven days (March 2-8, 2025)**
- We collected **game details & reviews** daily to track short-term review trends

### **2. Data Preprocessing & Cleaning**
- **Handling Missing Values**: Free games with missing price data were assigned **zero**.
- **New Variables Created**:
  - **Discount Ratio**: `% discount applied` to adjust for price perception
  - **Log Price**: Log-transformed price for variability handling
  - **Weighted Positivity Score**: Calculated based on review helpfulness scores
- **Filtering English Reviews**: Ensured **consistent sentiment analysis** across users.
- **Joining Daily Data**: Merged game metadata & reviews per **daily snapshot** before combining datasets.

---

## Key Findings
### 1. **Price and Review Sentiment**
- Higher-priced games receive **slightly fewer positive reviews**.
- **Discounts mitigate this effect**, making higher-priced games more favorable.

### 2. **Playtime and Review Sentiment**
- Players with **longer playtime tend to leave positive reviews**.
- **Early reviews are more critical**, possibly due to first impressions.

### 3. **Game Ownership and Review Sentiment**
- Users with **larger game libraries tend to be more critical**.
- More experienced gamers have **higher expectations**, leading to lower positivity rates.

---

## Visualizations
The `3-visuals/` folder contains:
- **Review Score Distribution** – Majority of reviews are positive (7-9 range).
- **Playtime Analysis** – Players spend more time on Action and RPG games before reviewing.
- **Positive vs. Negative Reviews Over Time** – Sentiment trends across seven days.

---

## How to Use This Repository
### 1. Clone the Repository
```bash
git clone https://github.com/mimir9911/steam-analytics.git
cd steam-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Notebooks
Navigate to `1-notebooks/` and run the relevant Jupyter notebooks in order:
```bash
jupyter notebook
```
1. `libraries_and_functions.ipynb` - Defines helper functions.
2. `get_app_details.ipynb` - Extracts metadata from the Steam API.
3. `get_app_reviews.ipynb` - Retrieves user reviews.
4. `merging_and_cleaning.ipynb` - Prepares and cleans the dataset.
5. `analysis.ipynb` - Performs data analysis.
6. `plots.ipynb` - Generates visualizations based on analysis results.

