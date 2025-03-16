def get_app_details(app_id):
    url = "https://store.steampowered.com/api/appdetails/"
    params = {"appids": app_id, "l": "english"}
    
    while True:
        if app_id is None:
            print_log("App ID is None.")
            return {}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            appdetails = data.get(str(app_id), {})
            if appdetails.get("success", False):
                print_log(f"App ID: {app_id} : Success")
                game_info = {
                    "type": appdetails.get("data", {}).get("type", None),
                    "name": appdetails.get("data", {}).get("name", None),
                    "steam_appid": app_id,
                    "is_free": appdetails.get("data", {}).get("is_free", None),
                    "supported_languages": appdetails.get("data", {}).get("supported_languages", None),
                    "developers": appdetails.get("data", {}).get("developers", None),
                    "publishers": appdetails.get("data", {}).get("publishers", None),
                    "price_overview": appdetails.get("data", {}).get("price_overview", {}).get("final_formatted", None),
                    "original_price": appdetails.get("data", {}).get("price_overview", {}).get("initial_formatted", None),
                    "discounted_price": appdetails.get("data", {}).get("price_overview", {}).get("final_formatted", None),
                    "platforms": appdetails.get("data", {}).get("platforms", None),
                    "genres": [genre.get("description") for genre in appdetails.get("data", {}).get("genres", [])],
                    "achievements": appdetails.get("data", {}).get("achievements", {}).get("total", None),
                }
                return game_info
            else:
                print_log(f"App ID: {app_id} - No details found or 'success' is FALSE.")
                break
        elif response.status_code == 429:
            print_log("Too many requests. Sleep for 10sec")
            time.sleep(10)
            continue
        elif response.status_code == 403:
            print_log("Forbidden access. Sleep for 5min.")
            time.sleep(5 * 60)
            continue
        else:
            print_log(f"ERROR: status code {response.status_code}")
            print_log(f"Error in App ID: {app_id}.")
            break
    return {}

def get_review_summary(app_id):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    response = requests.get(url)
    if response.status_code != 200:
        print_log(f"Failed to fetch review summary for App ID {app_id}, Status Code: {response.status_code}")
        return {}
    try:
        data = response.json()
    except Exception as e:
        print_log(f"Failed to parse review summary for App ID {app_id}: {e}")
        return {}
    if data.get("success", 0) != 1:
        print_log(f"Error fetching review summary for App ID {app_id}: {data.get('error')}")
        return {}
    query_summary = data.get("query_summary", {})
    summary = {
        "num_reviews": query_summary.get("num_reviews"),
        "review_score": query_summary.get("review_score"),
        "review_score_desc": query_summary.get("review_score_desc"),
        "total_positive": query_summary.get("total_positive"),
        "total_negative": query_summary.get("total_negative"),
        "total_reviews": query_summary.get("total_reviews")
    }
    return summary

execute_datetime = datetime.now()
search_result_folder_path = Path(f"search_results_{execute_datetime.strftime('%Y%m%d')}")
if not search_result_folder_path.exists():
    search_result_folder_path.mkdir()

params_list = [
    {"filter": "globaltopsellers"},
]
page_list = list(range(1, 9))  ## ADJUST THE PAGE RANGE
params_sr_default = {
    "category1": 998,
    "ndl": 1,
    "filter": "globaltopsellers",
    "page": 1,
    "json": 1
}

all_data = []
seen_appids = set() 

for update_param in params_list:
    items_all = []
    if update_param["filter"]:
        filename = f"{update_param['filter']}_{execute_datetime.strftime('%Y%m%d')}.pkl"
    else:
        filename = f"specials_{execute_datetime.strftime('%Y%m%d')}.pkl"
    if (search_result_folder_path / filename).exists():
        print_log(f"File {filename} exists. Skip.")
        continue
    for page_no in page_list:
        param = params_sr_default.copy()
        param.update(update_param)
        param["page"] = page_no

        search_results = get_search_results(param)
        if not search_results:
            continue
        items = search_results.get("items", [])

        for item in items:
            try:
                item["appid"] = re.search(r"steam/\w+/(\d+)", item["logo"]).group(1)
            except Exception as e:
                print_log(f"Failed to extract appid: {e}")
                item["appid"] = None

        for item in items:
            appid = item["appid"]
            if appid is None or appid in seen_appids:  
                continue
            seen_appids.add(appid) 

            appdetails = get_app_details(appid)
            if appdetails:
                item.update(appdetails)

            review_summary = get_review_summary(appid)
            if review_summary:
                item.update(review_summary)

        items_all.extend(items)

    all_data.extend(items_all)

if all_data:  
    df = pd.DataFrame(all_data)
    df.drop_duplicates(subset=['steam_appid'], inplace=True)  
    if update_param["filter"]:
        csv_filename = f"{update_param['filter']}_{execute_datetime.strftime('%Y%m%d')}.csv"
    else:
        csv_filename = f"specials_{execute_datetime.strftime('%Y%m%d')}.csv"
    csv_path = search_result_folder_path / csv_filename
    df.to_csv(csv_path, index=False)

    print_log(f"CSV file saved to {csv_path}")

