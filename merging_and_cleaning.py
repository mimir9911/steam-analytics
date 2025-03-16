base_directory = Path(__file__).parent if "__file__" in globals() else Path().resolve()

num_days = 7
start_date = datetime.strptime('20250302', '%Y%m%d')

date_list = [(start_date + timedelta(days=i)).strftime('%Y%m%d') for i in range(num_days)]

games_data = {}
reviews_data = {}

for date in date_list:
    search_result_folder_path = base_directory / f"search_results_{date}"  
    games_path = search_result_folder_path / f"globaltopsellers_{date}.csv"
    review_path = search_result_folder_path / f"globaltopsellers_reviews_{date}.csv"

    if games_path.exists():
        games_data[date] = pd.read_csv(games_path)
        games_data[date]["extraction_date"] = datetime.strptime(date, "%Y%m%d")
        print(f"Loaded games data for {date}")

    if review_path.exists():
        reviews_data[date] = pd.read_csv(review_path)
        reviews_data[date]["extraction_date"] = datetime.strptime(date, "%Y%m%d")
        print(f"Loaded reviews data for {date}")

def convert_price(price):
    try:
        clean_price = ''.join([ch for ch in str(price) if ch.isdigit() or ch == '.'])
        return float(clean_price) if clean_price else None
    except Exception:
        return None

for day in date_list:
    if day in games_data:  
        games = games_data[day] 

        ## CONVERT PRICE
        games['original_price_numeric'] = games['original_price'].apply(convert_price)
        games['discounted_price_numeric'] = games['discounted_price'].apply(convert_price)
        games['price_overview_numeric'] = games['price_overview'].apply(convert_price)

        ## REPLACE MISSING VALUES WITH 0 FOR FREE GAMES
        games.loc[games['is_free'] == True, ['original_price_numeric', 'discounted_price_numeric', 'price_overview_numeric']] = 0

        ## CALCULATE DISCOUNT RATIO
        games['discount_ratio'] = np.where(
            games['original_price_numeric'] > 0,
            (games['original_price_numeric'] - games['discounted_price_numeric']) / games['original_price_numeric'],
            0  # If original price is zero, set discount ratio to 0
        )

        ## REPLACE NA VALUES WITH 0
        games['discount_ratio'] = games['discount_ratio'].fillna(0)

        ## LOG-TRANSFORM PRICE -- HANDLE PRICE VARIABILITY ##
        games['log_price'] = np.log1p(games['original_price_numeric'])  # log(price + 1) to avoid log(0)
        
        games_data[day] = games

    else:
        print(f"games_{day} does not exist!")

for day in date_list:
    if day in reviews_data:  
        review = reviews_data[day]
    
        ## CONVERT VOTED_UP TO BOOLEAN
        review['voted_up_bool'] = review['voted_up'].astype(bool)
        review['voted_up_binary'] = review['voted_up'].astype(int)  # Convert to binary (1 = Recommended, 0 = Not Recommended)

        ## CONVERT TO NUMERIC
        review['playtime_at_review'] = pd.to_numeric(review['playtime_at_review'], errors='coerce')
        review['num_games_owned'] = pd.to_numeric(review['num_games_owned'], errors='coerce')

        ## WEIGHTED POSITIVITY SCORE 
        review['weighted_positive'] = review['voted_up'] * review['weighted_vote_score']
        
        reviews_data[day] = review

    else:
        print(f"review_{day} does not exist!")

for day in date_list:
    if day in reviews_data and day in games_data:
        review = reviews_data[day]
        games = games_data[day] 

        ## MERGE ON APPID
        merged_review = review.merge(games, on='appid', how='inner')

        reviews_data[day] = merged_review

    else:
        print(f"Either review or games data for {day} does not exist!")

# COLLECT ALL REVIEWS DATA PER DATE
all_reviews = []

for day in date_list:
    if day in reviews_data:  
        all_reviews.append(reviews_data[day])
    else:
        print(f"review data for {day} not found!")

## COMBINE AND REMOVE FULL DUPLICATES 
if all_reviews:
    combined_reviews = pd.concat(all_reviews, ignore_index=True).drop_duplicates()
else:
    combined_reviews = pd.DataFrame() 
    
combined_reviews.head()

combined_reviews.to_csv("combined_reviews.csv", index=False)

review_summary = merged_review.groupby('appid').agg(
    avg_num_games_owned=('num_games_owned', 'mean'),  ## AVG NUMBER OF GAMES OWNED
    positivity_rate=('voted_up_binary', 'mean'),  ## AVG POSITIVITY RATE
    weighted_positivity_rate=('weighted_positive', 'mean'),
    avg_weighted_vote_score=('weighted_vote_score', 'mean'),
    num_reviews=('voted_up_binary', 'count'),  ## TOTAL REVIEW COUNT
    avg_review_score=('review_score', 'mean'),
    mean_playtime_at_review=('playtime_at_review', 'mean'),
    median_playtime_at_review=('playtime_at_review', 'median')
).reset_index()

review_summary = review_summary.merge(
    merged_review.drop_duplicates(subset='appid'), on='appid', how='inner'
)

review_summary = review_summary.drop(columns=['num_reviews_y']) ## DROP REDUNDANCY
review_summary = review_summary.rename(columns={'num_reviews_x': 'num_reviews'}) ## RENAME

review_summary.columns.tolist()

review_summary.to_csv("review_summary.csv", index=False)

