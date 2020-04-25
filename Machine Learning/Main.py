import requests
import Get_Todays_Picks
import json

# Puts each rating into a general predicted position
def get_position(rating):
    if rating <= -5:
        if rating <= -10:
            return "Strongly Sell"
        return "Sell"
    if rating >= 5:
        if rating >= 10:
            return "Strongly Buy"
        return "Buy"
    return "Hold"

# Enter your API here
url = 'API_HERE'

data = Get_Todays_Picks.todays_stock_data()
inputs = {}
# Every stock to an input dictionary
for i in range(data.shape[0]):
    row = data.iloc[i]
    ticker = row.pop('ticker')
    inputs[ticker] = row.to_csv(header=None, index=False, line_terminator=',').rsplit(',', 1)[0]

outputs = {}
# Gets the output from our model
for stock in inputs:
    resp = None
    while resp is None or "Internal" in resp.text:
        load = {'data': inputs[stock]}
        resp = requests.post(url, json=load)
        print(resp.text)
    rating = resp.json().get("data")
    entry = {
        'Rating': rating,
        'Predicted Position': get_position(rating)
    }
    outputs[stock] = entry

with open('today_calls.json', 'w') as outfile:
    json.dump(outputs, outfile)