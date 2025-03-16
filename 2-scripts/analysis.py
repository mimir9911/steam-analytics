df_vif = combined_reviews[
    [
        'num_games_owned', 'num_reviews_author', 'playtime_forever',
        'playtime_last_two_weeks', 'playtime_at_review', 'deck_playtime_at_review',
        'last_played', 'weighted_vote_score', 'voted_up_binary',
        'weighted_positive', 'original_price_numeric', 'discounted_price_numeric',
        'price_overview_numeric', 'discount_ratio', 'log_price'
    ]
].select_dtypes(include=[np.number]).dropna()

vif_data = pd.DataFrame({
    "Feature": df_vif.columns,
    "VIF": [variance_inflation_factor(df_vif.values, i) for i in range(df_vif.shape[1])]
})

print(vif_data)

df_vif_reduced = df_vif.drop(columns=[
    'last_played', 'weighted_positive', 'weighted_vote_score',
    'discounted_price_numeric', 'original_price_numeric'
], errors='ignore')

# Recalculate VIF after feature selection
vif_data_reduced = pd.DataFrame({
    "Feature": df_vif_reduced.columns,
    "VIF": [variance_inflation_factor(df_vif_reduced.values, i) for i in range(df_vif_reduced.shape[1])]
})

print(vif_data_reduced)

## DEFINE INDEPENDENT AND DEPENDENT VARIABLES
X_price = combined_reviews[['price_overview_numeric', 'discount_ratio']].copy()
y = combined_reviews['voted_up_binary'] 

## MEAN-CENTER PRICE 
X_price['price_centered'] = (X_price['price_overview_numeric'] - X_price['price_overview_numeric'].mean()) / X_price['price_overview_numeric'].std()

## CREATING AN INTERACTION TERM
X_price['price_discount_interaction'] = X_price['price_centered'] * X_price['discount_ratio']

## DROP ORIGINAL `PRICE_OVERVIEW_NUMERIC` TO AVOID REDUNDANCY
X_price = X_price.drop(columns=['price_overview_numeric'])

## DROP NA AND INF VALUES
X_price = X_price.replace([np.inf, -np.inf], np.nan).dropna()
y = y.loc[X_price.index]

## ADD CONSTANT
X_price = sm.add_constant(X_price)

## LOGISTIC REGRESSION MODEL 
logit_model_price = sm.Logit(y, X_price).fit(maxiter=100)
print(logit_model_price.summary())

## DEFINE INDEPENDENT AND DEPENDENT VARIABLES
X_playtime = combined_reviews[['playtime_forever', 'playtime_at_review']].copy() 
y = combined_reviews['voted_up_binary']

## CREATING AN INTERACTION TERM
X_playtime['playtime_interaction'] = X_playtime['playtime_forever'] * X_playtime['playtime_at_review']

## DROP NA AND INF VALUES
X_playtime = X_playtime.replace([np.inf, -np.inf], np.nan).dropna()
y = y.loc[X_playtime.index] 

## ADD CONSTANT
X_playtime = sm.add_constant(X_playtime)

## LOGISTIC REGRESSION MODEL 
logit_model_playtime = sm.Logit(y, X_playtime).fit()
print(logit_model_playtime.summary())

## DEFINE INDEPENDENT AND DEPENDENT VARIABLES
X_own = combined_reviews[['num_games_owned']]
y = combined_reviews['voted_up_binary']

## DROP NA AND INF VALUES
X_own = X_own.replace([np.inf, -np.inf], np.nan).dropna()
y = y.loc[X_own.index]  

## ADD CONSTANT
X_own = sm.add_constant(X_own)

## LOGISTIC REGRESSION MODEL 
logit_model_games_owned = sm.Logit(y, X_own).fit()
print(logit_model_games_owned.summary())

