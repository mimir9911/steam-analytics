# Steam Analytics Project

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
│   ├── merging_and_cleaning.ipynb
├── 2-data
│   ├── search_results_20250302
│   ├── search_results_20250303
│   ├── search_results_20250304
│   ├── search_results_20250305
│   ├── search_results_20250306
│   ├── search_results_20250307
│   ├── search_results_20250308
├── 3-visuals
│   ├── avg_playtime_genre.png
│   ├── genre.jpg
│   ├── mean_reviews.png
│   ├── numgames.jpg
│   ├── playtime.png
│   ├── reviews.jpg
│   ├── reviewscore.jpg
```

---

## Data Collection
- **Data Source:** Steam API
- **Endpoints Used:**
  - `/search/results/` → Fetches top-selling game IDs
  - `/api/appdetails/` → Extracts game metadata (price, genre, platform)
  - `/appreviews/` → Retrieves user reviews, playtime, and sentiment
- **Sampling Approach:** 200 top-selling games over seven days (March 2-8, 2025)

---

## Preprocessing & Cleaning
- Removed missing values (e.g., free games with no price)  
- Calculated additional features like discount ratio and log price  
- Merged datasets by date for trend analysis  
- Filtered out non-English reviews for consistency  

---

## Key Findings
### 1. Price and Review Sentiment
- Higher-priced games receive slightly fewer positive reviews.
- Discounts mitigate this effect, making higher-priced games more favorable.

### 2. Playtime and Review Sentiment
- Users who spend more time in a game tend to leave positive reviews.
- Players who review early in their play experience tend to be more critical.

### 3. Game Ownership and Review Sentiment
- Users with larger game libraries tend to be more critical.
- More experienced gamers have higher expectations, leading to lower positivity rates.

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
Step 1: `libraries_and_functions.ipynb` - Defines helper functions.
Step 2: `get_app_details.ipynb` - Extracts metadata from the Steam API.
Step 3: `get_app_reviews.ipynb` - Retrieves user reviews.
Step 4: `merging_and_cleaning.ipynb` - Prepares and cleans the dataset.
Step 5: `analysis.ipynb` - Performs data analysis.
Step 6: `plots.ipynb` - Generates visualizations.

