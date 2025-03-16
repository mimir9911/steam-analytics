def get_steam_reviews(app_id):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    review_rows = []
    cursor = "*"
    reviews_fetched = 0
    api_call_counter = 0
    start_time = time.time()
    
    while reviews_fetched < 1000 and api_call_counter < 10:
        params = {"json": 1, "cursor": cursor, "num_per_page": 100}
        api_call_counter += 1
        
        req_start = time.time()
        response = requests.get(url, params=params)
        req_duration = time.time() - req_start
        if req_duration > 5:
            print_log(f"Warning: Request for App ID {app_id} took {req_duration:.2f} seconds.")
        if response.status_code != 200:
            print_log(f"Failed to fetch reviews for App ID {app_id}, Status Code: {response.status_code}")
            break
        data = response.json()
        if data.get('success', 0) != 1:
            print_log(f"Error fetching reviews for App ID {app_id}: {data.get('error')}")
            break
        
        reviews = data.get('reviews', [])
        if not reviews:
            print_log(f"No new reviews for App ID {app_id}. Ending fetch.")
            break 
            
        for review in reviews:
            review_row = {
                "appid": app_id,
                "recommendationid": review.get("recommendationid"),
                "steamid": review.get("author", {}).get("steamid"),
                "num_games_owned": review.get("author", {}).get("num_games_owned"),
                "num_reviews_author": review.get("author", {}).get("num_reviews"),
                "playtime_forever": review.get("author", {}).get("playtime_forever"),
                "playtime_last_two_weeks": review.get("author", {}).get("playtime_last_two_weeks"),
                "playtime_at_review": review.get("author", {}).get("playtime_at_review"),
                "deck_playtime_at_review": review.get("author", {}).get("deck_playtime_at_review"),
                "last_played": review.get("author", {}).get("last_played"),
                "timestamp_created": review.get("timestamp_created"),
                "timestamp_updated": review.get("timestamp_updated"),
                "voted_up": review.get("voted_up"),
                "weighted_vote_score": review.get("weighted_vote_score"),
                "steam_purchase": review.get("steam_purchase"),
                "received_for_free": review.get("received_for_free")
            }
            review_rows.append(review_row)
            reviews_fetched += 1
            if reviews_fetched >= 1000:
                break
        
        if reviews_fetched >= 1000:
            break
        
        new_cursor = data.get('cursor')
        if not new_cursor or new_cursor == cursor:
            print_log(f"No new cursor for App ID {app_id}. Ending fetch.")
            break
        cursor = new_cursor
        time.sleep(1)
    
    total_time = time.time() - start_time
    print_log(f"Total time for App ID {app_id}: {total_time:.2f} sec, API calls: {api_call_counter}, Reviews fetched: {reviews_fetched}")
    return review_rows

execute_datetime = datetime.now()
params_list = [
    {"filter": "globaltopsellers"},
]
page_list = list(range(1, 9))
params_sr_default = {
    "category1": 998,
    "ndl": 1,
    "filter": "globaltopsellers",
    "page": 1,
    "json": 1
}

request_counter = 0
all_reviews = []
stop_extraction = False  

for update_param in params_list:
    if stop_extraction:
        break
    for page_no in page_list:
        param = params_sr_default.copy()
        param.update(update_param)
        param["page"] = page_no

        search_results = get_search_results(param)
        print_log(f"Fetched {len(search_results.get('items', []))} items from page {page_no}.")

        if not search_results.get('items', []):
            print_log("No more items found on this page – reached the end. Stopping further page requests.")
            stop_extraction = True
            break

        items = search_results.get("items", [])
        for item in items:
            appid_match = re.search(r"steam/\w+/(\d+)", item["logo"])
            if appid_match:
                app_id = appid_match.group(1)
                print_log(f"Fetching reviews for App ID: {app_id}")
                reviews = get_steam_reviews(app_id)
                if reviews:
                    all_reviews.extend(reviews)
                    reviews_df = pd.DataFrame(all_reviews)
                    filename = search_result_folder_path / f"globaltopsellers_reviews_{execute_datetime.strftime('%Y%m%d')}.csv"
                    reviews_df.to_csv(filename, index=False)
                    print_log(f"Saved: {filename}")
            else:
                print_log("Failed to extract appid for an item.")
            
            request_counter += 1
            if request_counter >= 10:
                print_log("10 requests made, pausing for 10 seconds to comply with rate limit.")
                time.sleep(10)
                request_counter = 0

        if page_no == max(page_list):
            print_log("Reached the maximum page limit (page 8). Stopping extraction.")
            stop_extraction = True
            break

if all_reviews:
    reviews_df = pd.DataFrame(all_reviews)
    filename = search_result_folder_path / f"globaltopsellers_reviews_{execute_datetime.strftime('%Y%m%d')}.csv"
    reviews_df.to_csv(filename, index=False)
    print_log(f"Final CSV file saved to {filename}")

