combined_reviews.describe() ## SUMMARY STATISTICS

## FINDING NA VALUES
missing_counts = combined_reviews.isna().sum()
print(missing_counts)

## CALCULATE TOTAL POSITIVE AND NEGATIVE REVIEWS
positive_total = combined_reviews['total_positive'].sum()
negative_total = combined_reviews['total_negative'].sum()

## CREATING DATASET FOR THE PLOT
review_types = ['Positive', 'Negative']
counts = [positive_total, negative_total]

## CREATING THE BARCHART
plt.figure(figsize=(8, 6))
bars = plt.bar(review_types, counts, color=['green', 'red'])

plt.title("Total Positive vs. Negative Reviews")
plt.xlabel("Review Type")
plt.ylabel("Total Reviews")

## ANNOTATING BARS
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{int(yval)}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig("total_positive_negative_reviews.jpg", format="jpg", dpi=300)
plt.show()

## CALCULATING THE FREQUENCY OF EACH REVIEW SCORE AND SORT BY SCORE
score_counts = combined_reviews['review_score'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
ax = score_counts.plot(kind='bar', color='orange', edgecolor='black')
plt.title("Distribution of Review Scores")
plt.xlabel("Review Score")
plt.ylabel("Frequency")
plt.xticks(rotation=0)
plt.tight_layout()

## ANNOTATING BARS
for i, count in enumerate(score_counts):
    plt.text(i, count, f'{count}', ha='center', va='bottom')

plt.savefig("review_score_distribution_annotated.jpg", format="jpg", dpi=300)
plt.show()

## HELPER FUNCTION TO PARSE A STRING INTO A LIST
def parse_genres(genre_str):
    if pd.isnull(genre_str):
        return [] 
    try:
        return ast.literal_eval(genre_str)
    except:
        ## IF PARSING FAILS, RETURN ORIGINAL STRING IN A LIST
        return [genre_str]

## CONVERT GENRES FROM STRING TO LIST
combined_reviews['genres_list'] = combined_reviews['genres'].apply(parse_genres)

## EXPLODE THE `GENRES_LIST` SO EACH GENRE IS ON ITS OWN ROW
df_exploded = combined_reviews.explode('genres_list')

## CLEAN UP WHITESPACE
df_exploded['genres_list'] = df_exploded['genres_list'].str.strip()

## COUNT GENRES LIST
genre_counts = df_exploded['genres_list'].value_counts()

## CREATING A BARCHART
plt.figure(figsize=(10, 6))
ax = genre_counts.plot(kind='bar', color='skyblue')
plt.title("Distribution of Game Genres")
plt.xlabel("Genres")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

## ANNOTATING BARS
for i, count in enumerate(genre_counts):
    plt.text(i, count, str(count), ha='center', va='bottom')

plt.savefig("distribution_of_game_genres.jpg", format="jpg", dpi=300)
plt.show()

## GROUP BY EXTRACTION DATE AND CALCULATE MEAN FOR THE REVIEW VARIABLES
mean_reviews = combined_reviews.groupby('extraction_date_y')[['total_positive', 'total_negative', 'total_reviews']].mean().reset_index()

plt.figure(figsize=(10, 6))

## PLOT MEAN POSITIVE, NEGATIVE, AND TOTAL REVIEWS OVER TIME WITH MARKERS
plt.plot(mean_reviews['extraction_date_y'], mean_reviews['total_positive'], label='Avg Positive Reviews', marker='o')
plt.plot(mean_reviews['extraction_date_y'], mean_reviews['total_negative'], label='Avg Negative Reviews', marker='o')
plt.plot(mean_reviews['extraction_date_y'], mean_reviews['total_reviews'], label='Avg Total Reviews', marker='o')


## ANNOTATING EACH POINT FOR POSITIVE, NEGATIVE, AND TOTAL REVIEWS
for idx, row in mean_reviews.iterrows():
    plt.annotate(f'{row["total_positive"]:.1f}', 
                 (row['extraction_date_y'], row['total_positive']), 
                 textcoords="offset points", 
                 xytext=(0,5), 
                 ha='center')
for idx, row in mean_reviews.iterrows():
    plt.annotate(f'{row["total_negative"]:.1f}', 
                 (row['extraction_date_y'], row['total_negative']), 
                 textcoords="offset points", 
                 xytext=(0,-10), 
                 ha='center')
for idx, row in mean_reviews.iterrows():
    plt.annotate(f'{row["total_reviews"]:.1f}', 
                 (row['extraction_date_y'], row['total_reviews']), 
                 textcoords="offset points", 
                 xytext=(0,5), 
                 ha='center')

plt.xlabel('Extraction Date')
plt.ylabel('Average Number of Reviews')
plt.title('Change in the Average Number of Positive, Negative, and Total Reviews Over Time')
plt.legend()
plt.savefig("mean_reviews.png", dpi=300, bbox_inches="tight")
plt.show()

def parse_genres(genre_str):
    if pd.isnull(genre_str):
        return []
    try:
        return ast.literal_eval(genre_str)
    except:
        return [genre_str]

## CONVERT EXTRACTION_DATE_Y TO DATETIME
df_exploded['extraction_date_y'] = pd.to_datetime(df_exploded['extraction_date_y'])

## CREATE `DATE` COLUMN
df_exploded['date'] = df_exploded['extraction_date_y'].dt.date

## GROUP BY DATE AND THE SINGLE GENRE IN EACH ROW THEN COMPUTE AVG PLAYTIME
grouped = df_exploded.groupby(['date', 'genres_list'])['playtime_at_review'].mean().reset_index()

## PIVOT SO EACH GENRE BECOMES A SEPARATE COLUMN
pivoted = grouped.pivot(index='date', columns='genres_list', values='playtime_at_review')

## PLOT GENRE AS ITS OWN LINE
plt.figure(figsize=(10, 6))
for genre in pivoted.columns:
    plt.plot(pivoted.index, pivoted[genre], marker='o', label=genre)

plt.title("Change in Average Playtime at Review by Genre Over Time")
plt.xlabel("Extraction Date")
plt.ylabel("Average Playtime at Review (minutes)")
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("avg_playtime_genre.png", dpi=300, bbox_inches="tight")
plt.show()

