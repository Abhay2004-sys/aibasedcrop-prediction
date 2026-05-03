# from flask import Flask, request, render_template_string
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# import numpy as np
# import matplotlib.pyplot as plt
# import requests
# import os
# import time

# app = Flask(__name__)

# # =========================
# # 🔹 DATASET
# # =========================
# df = pd.read_csv(r"C:\Users\Dushyant singh\Desktop\file\Crop_recommendation.csv")

# X = df.drop("label", axis=1)
# y = df["label"]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model = RandomForestClassifier(n_estimators=100)
# model.fit(X_train, y_train)

# # =========================
# # 🔹 WEATHER API
# # =========================
# API_KEY = "ed78f9f283ed355ac71a94f2bfe9a607"   # ← apni key yaha daalo

# def get_weather(city):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         data = requests.get(url).json()

#         if data.get("cod") != 200:
#             return None, None

#         return data["main"]["temp"], data["main"]["humidity"]

#     except:
#         return None, None

# # =========================
# # 🔹 FERTILIZER
# # =========================
# def fertilizer(crop):
#     data = {
#         "rice": "Urea + DAP",
#         "wheat": "NPK + Urea",
#         "maize": "Nitrogen rich fertilizer",
#         "cotton": "Potassium + Phosphorus"
#     }
#     return data.get(crop, "General Fertilizer")

# # =========================
# # 🔹 HTML UI
# # =========================
# html = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>AI Crop Predictor</title>

# <style>
# body {
#     font-family: 'Segoe UI';
#     background: linear-gradient(to right, #43cea2, #185a9d);
# }

# .container {
#     width: 420px;
#     margin: 40px auto;
#     background: white;
#     padding: 25px;
#     border-radius: 15px;
#     box-shadow: 0 8px 25px rgba(0,0,0,0.2);
# }

# h1 { text-align:center; color:#2e7d32; }

# input {
#     width: 100%;
#     padding: 10px;
#     margin: 6px 0;
#     border-radius: 8px;
#     border: 1px solid #ccc;
# }

# button {
#     width: 100%;
#     padding: 12px;
#     background: #2e7d32;
#     color: white;
#     border: none;
#     border-radius: 8px;
#     cursor: pointer;
# }

# .result-box {
#     margin-top: 15px;
#     padding: 15px;
#     background: #e8f5e9;
#     border-radius: 10px;
# }

# .fert-box {
#     margin-top: 10px;
#     padding: 10px;
#     background: #fff3cd;
#     border-radius: 10px;
# }

# img {
#     margin-top: 15px;
#     border-radius: 10px;
# }
# </style>
# </head>

# <body>

# <div class="container">
# <h1>🌱 AI Crop Predictor</h1>

# <form method="post">
# <input name="city" placeholder="📍 Enter City (optional)">

# <input name="N" placeholder="Nitrogen" required>
# <input name="P" placeholder="Phosphorus" required>
# <input name="K" placeholder="Potassium" required>
# <input name="temperature" placeholder="Temperature (optional)">
# <input name="humidity" placeholder="Humidity (optional)">
# <input name="ph" placeholder="pH" required>
# <input name="rainfall" placeholder="Rainfall" required>

# <button type="submit">Predict</button>
# </form>

# {% if result %}
# <div class="result-box">

# <h3>{{result|safe}}</h3>

# {% if fert %}
# <div class="fert-box">
# <b>{{fert}}</b>
# </div>
# {% endif %}

# {% if graph %}
# <h4>📊 Prediction Graph</h4>
# <img src="{{graph}}" width="100%">
# {% endif %}

# </div>
# {% endif %}

# </div>
# </body>
# </html>
# """

# # =========================
# # 🔹 ROUTE
# # =========================
# @app.route("/", methods=["GET", "POST"])
# def home():
#     result = ""
#     fert = ""
#     graph = ""

#     if request.method == "POST":
#         try:
#             city = request.form.get("city")

#             temp_api, hum_api = get_weather(city) if city else (None, None)

#             values = []

#             for key in ["N","P","K","ph","rainfall"]:
#                 val = request.form.get(key)
#                 if val == "":
#                     return render_template_string(html, result="❌ Fill required fields")
#                 values.append(float(val))

#             # auto weather OR fallback
#             temp = temp_api if temp_api else float(request.form.get("temperature") or 25)
#             hum = hum_api if hum_api else float(request.form.get("humidity") or 50)

#             values.insert(3, temp)
#             values.insert(4, hum)

#             probs = model.predict_proba([values])[0]
#             classes = model.classes_

#             top3 = np.argsort(probs)[-3:][::-1]

#             result = "🌾 Top Crops:<br>"
#             for i in top3:
#                 result += f"{classes[i]} → {round(probs[i]*100,2)}%<br>"

#             if temp_api:
#                 result += f"<br>🌦️ Auto Weather: {temp_api}°C, {hum_api}%"

#             fert = "🌱 Fertilizer: " + fertilizer(classes[top3[0]])

#             # GRAPH
#             if not os.path.exists("static"):
#                 os.makedirs("static")

#             plt.figure()
#             labels = [classes[i] for i in top3]
#             values_graph = [probs[i]*100 for i in top3]

#             plt.bar(labels, values_graph)
#             plt.xlabel("Crops")
#             plt.ylabel("Confidence %")
#             plt.title("Top Crop Predictions")

#             filename = f"static/graph_{int(time.time())}.png"
#             plt.savefig(filename)
#             plt.close()

#             graph = "/" + filename

#         except Exception as e:
#             result = "Error: " + str(e)

#     return render_template_string(html, result=result, fert=fert, graph=graph)

# # =========================
# # 🔹 RUN
# # =========================
# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, request, render_template_string
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.model_selection import train_test_split
# import numpy as np
# import matplotlib.pyplot as plt
# import requests
# import os
# import time

# app = Flask(__name__)

# # =========================
# # 🔹 DATASET
# # =========================
# df = pd.read_csv(r"C:\Users\Dushyant singh\Desktop\file\Crop_recommendation.csv")

# # Classification
# X = df.drop("label", axis=1)
# y = df["label"]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model = RandomForestClassifier(n_estimators=100)
# model.fit(X_train, y_train)

# # =========================
# # 🔹 YIELD MODEL (approx)
# # =========================
# df["yield"] = (df["N"]*0.2 + df["P"]*0.1 + df["K"]*0.15 +
#                df["temperature"]*0.3 + df["humidity"]*0.2)

# X_y = df.drop(["label","yield"], axis=1)
# y_y = df["yield"]

# yield_model = RandomForestRegressor(n_estimators=100)
# yield_model.fit(X_y, y_y)

# # =========================
# # 🔹 WEATHER API
# # =========================
# API_KEY = "ed78f9f283ed355ac71a94f2bfe9a607"

# def get_weather(city):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#         data = requests.get(url).json()
#         if data.get("cod") != 200:
#             return None, None
#         return data["main"]["temp"], data["main"]["humidity"]
#     except:
#         return None, None

# # =========================
# # 🔹 PROFIT
# # =========================
# def calculate_profit(yield_value, price, cost):
#     return (yield_value * price) - cost

# # =========================
# # 🔹 FERTILIZER
# # =========================
# def fertilizer(crop):
#     data = {
#         "rice": "Urea + DAP",
#         "wheat": "NPK + Urea",
#         "maize": "Nitrogen rich fertilizer",
#         "cotton": "Potassium + Phosphorus"
#     }
#     return data.get(crop, "General Fertilizer")

# # =========================
# # 🔹 HTML UI
# # =========================
# html = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>AI Crop Predictor PRO</title>

# <style>
# body {
#     font-family: 'Segoe UI';
#     background: linear-gradient(to right, #43cea2, #185a9d);
# }

# .container {
#     width: 430px;
#     margin: 40px auto;
#     background: white;
#     padding: 25px;
#     border-radius: 15px;
#     box-shadow: 0 8px 25px rgba(0,0,0,0.2);
# }

# h1 { text-align:center; color:#2e7d32; }

# input {
#     width: 100%;
#     padding: 10px;
#     margin: 6px 0;
#     border-radius: 8px;
#     border: 1px solid #ccc;
# }

# button {
#     width: 100%;
#     padding: 12px;
#     background: #2e7d32;
#     color: white;
#     border: none;
#     border-radius: 8px;
#     cursor: pointer;
# }

# .result-box {
#     margin-top: 15px;
#     padding: 15px;
#     background: #e8f5e9;
#     border-radius: 10px;
# }

# .fert-box {
#     margin-top: 10px;
#     padding: 10px;
#     background: #fff3cd;
#     border-radius: 10px;
# }

# img {
#     margin-top: 15px;
#     border-radius: 10px;
# }
# </style>
# </head>

# <body>

# <div class="container">
# <h1>🌱 AI Crop Predictor PRO</h1>

# <form method="post">
# <input name="city" placeholder="📍 City (optional)">

# <input name="N" placeholder="Nitrogen" required>
# <input name="P" placeholder="Phosphorus" required>
# <input name="K" placeholder="Potassium" required>

# <input name="temperature" placeholder="Temperature (optional)">
# <input name="humidity" placeholder="Humidity (optional)">

# <input name="ph" placeholder="pH" required>
# <input name="rainfall" placeholder="Rainfall" required>

# <input name="price" placeholder="💰 Price (₹)">
# <input name="cost" placeholder="💸 Cost (₹)">

# <button type="submit">🚀 Predict</button>
# </form>

# {% if result %}
# <div class="result-box">

# <h3>{{result|safe}}</h3>

# {% if fert %}
# <div class="fert-box"><b>{{fert}}</b></div>
# {% endif %}

# {% if extra %}
# <div class="fert-box"><b>{{extra|safe}}</b></div>
# {% endif %}

# {% if graph %}
# <h4>📊 Prediction Graph</h4>
# <img src="{{graph}}" width="100%">
# {% endif %}

# </div>
# {% endif %}

# </div>
# </body>
# </html>
# """

# # =========================
# # 🔹 ROUTE
# # =========================
# @app.route("/", methods=["GET","POST"])
# def home():
#     result = ""
#     fert = ""
#     extra = ""
#     graph = ""

#     if request.method == "POST":
#         try:
#             city = request.form.get("city")
#             temp_api, hum_api = get_weather(city) if city else (None, None)

#             values = []
#             for key in ["N","P","K","ph","rainfall"]:
#                 val = request.form.get(key)
#                 if val == "":
#                     return render_template_string(html, result="❌ Fill required fields")
#                 values.append(float(val))

#             temp = temp_api if temp_api else float(request.form.get("temperature") or 25)
#             hum = hum_api if hum_api else float(request.form.get("humidity") or 50)

#             values.insert(3, temp)
#             values.insert(4, hum)

#             probs = model.predict_proba([values])[0]
#             classes = model.classes_
#             top3 = np.argsort(probs)[-3:][::-1]

#             result = "🌾 Top Crops:<br>"
#             for i in top3:
#                 result += f"{classes[i]} → {round(probs[i]*100,2)}%<br>"

#             if temp_api:
#                 result += f"<br>🌦️ Weather: {temp_api}°C, {hum_api}%"

#             fert = "🌱 Fertilizer: " + fertilizer(classes[top3[0]])

#             # Yield + Profit
#             yield_value = yield_model.predict([values])[0]
#             price = float(request.form.get("price") or 0)
#             cost = float(request.form.get("cost") or 0)
#             profit = calculate_profit(yield_value, price, cost)

#             extra = f"""
# 📈 Yield: {round(yield_value,2)} units<br>
# 💰 Profit: ₹{round(profit,2)}
# """

#             # Graph
#             if not os.path.exists("static"):
#                 os.makedirs("static")

#             plt.figure()
#             labels = [classes[i] for i in top3]
#             vals = [probs[i]*100 for i in top3]

#             plt.bar(labels, vals)
#             plt.xlabel("Crops")
#             plt.ylabel("Confidence %")
#             plt.title("Top Crop Predictions")

#             filename = f"static/graph_{int(time.time())}.png"
#             plt.savefig(filename)
#             plt.close()

#             graph = "/" + filename

#         except Exception as e:
#             result = "Error: " + str(e)

#     return render_template_string(html, result=result, fert=fert, extra=extra, graph=graph)

# # =========================
# # 🔹 RUN
# # =========================
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import requests

app = Flask(__name__)

# =========================
# 🔹 LOAD DATASET (FIXED PATH)
# =========================
df = pd.read_csv("Crop_recommendation.csv")

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# =========================
# 🔹 WEATHER API
# =========================
API_KEY = "ed78f9f283ed355ac71a94f2bfe9a607"

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return None, None

        return data["main"]["temp"], data["main"]["humidity"]
    except:
        return None, None

# =========================
# 🔹 LOGIC FUNCTIONS
# =========================

def soil_type(ph):
    if ph < 5.5:
        return "Acidic Soil"
    elif 5.5 <= ph <= 7.5:
        return "Neutral Soil"
    else:
        return "Alkaline Soil"

def fertilizer(crop):
    data = {
        "rice": "Urea + DAP",
        "wheat": "NPK + Urea",
        "maize": "Nitrogen rich fertilizer",
        "cotton": "Potassium + Phosphorus"
    }
    return data.get(crop, "General Fertilizer")

def land_suggestion(crop):
    data = {
        "rice": "1 - 2 hectare",
        "wheat": "1 hectare",
        "maize": "0.5 - 1 hectare",
        "cotton": "2+ hectare"
    }
    return data.get(crop, "1 hectare recommended")

def yield_estimation(crop):
    data = {
        "rice": 2.5,
        "wheat": 3.0,
        "maize": 2.8,
        "cotton": 1.5
    }
    return data.get(crop, 2.0)

def profit_estimation(crop):
    data = {
        "rice": 40000,
        "wheat": 35000,
        "maize": 30000,
        "cotton": 50000
    }
    return data.get(crop, 30000)

# =========================
# 🔹 HTML UI
# =========================
html = """
<!DOCTYPE html>
<html>
<head>
<title>Smart Agriculture AI</title>
<style>
body {font-family: Arial; background: linear-gradient(to right,#43cea2,#185a9d);}
.container {width:420px;margin:40px auto;background:white;padding:25px;border-radius:15px;}
input,button {width:100%;padding:10px;margin:6px 0;border-radius:8px;}
button {background:green;color:white;}
.box {margin-top:10px;padding:10px;border-radius:10px;background:#e8f5e9;}
</style>
</head>
<body>
<div class="container">
<h2>🌱 Smart Agriculture AI</h2>

<form method="post">
<input name="city" placeholder="City (auto weather)">
<input name="N" placeholder="Nitrogen" required>
<input name="P" placeholder="Phosphorus" required>
<input name="K" placeholder="Potassium" required>
<input name="temperature" placeholder="Temperature">
<input name="humidity" placeholder="Humidity">
<input name="ph" placeholder="pH" required>
<input name="rainfall" placeholder="Rainfall" required>
<button type="submit">Predict</button>
</form>

{% if result %}<div class="box">{{result|safe}}</div>{% endif %}
{% if fert %}<div class="box">{{fert}}</div>{% endif %}
{% if land %}<div class="box">{{land}}</div>{% endif %}
{% if graph %}<img src="{{graph}}" width="100%">{% endif %}

</div>
</body>
</html>
"""

# =========================
# 🔹 ROUTE
# =========================
@app.route("/", methods=["GET","POST"])
def home():
    result = ""
    fert = ""
    graph = ""
    land = ""

    if request.method == "POST":
        try:
            city = request.form.get("city")
            temp_api, hum_api = get_weather(city) if city else (None, None)

            values = [
                float(request.form["N"]),
                float(request.form["P"]),
                float(request.form["K"]),
                float(temp_api if temp_api else request.form["temperature"]),
                float(hum_api if hum_api else request.form["humidity"]),
                float(request.form["ph"]),
                float(request.form["rainfall"])
            ]

            probs = model.predict_proba([values])[0]
            classes = model.classes_
            top3 = np.argsort(probs)[-3:][::-1]

            best_crop = classes[top3[0]]
            soil = soil_type(values[5])

            yield_val = yield_estimation(best_crop)
            profit_val = profit_estimation(best_crop)

            result = f"<b>Soil:</b> {soil}<br><br><b>Top Crops:</b><br>"
            for i in top3:
                result += f"{classes[i]} → {round(probs[i]*100,2)}%<br>"

            result += f"<br>🌾 Yield: {yield_val} ton/hectare<br>💰 Profit: ₹{profit_val}/hectare"

            fert = "🌱 Fertilizer: " + fertilizer(best_crop)
            land = "🌾 Land: " + land_suggestion(best_crop)

            # Graph
            if not os.path.exists("static"):
                os.makedirs("static")

            plt.figure()
            labels = [classes[i] for i in top3]
            values_graph = [probs[i]*100 for i in top3]

            plt.bar(labels, values_graph)
            plt.title("Prediction")

            filename = f"static/graph_{int(time.time())}.png"
            plt.savefig(filename)
            plt.close()

            graph = "/" + filename

        except Exception as e:
            result = "Error: " + str(e)

    return render_template_string(html, result=result, fert=fert, graph=graph, land=land)

# =========================
# 🔹 RUN (RENDER READY)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)