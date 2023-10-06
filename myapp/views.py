import json
import os
import joblib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from .forms import PricePredictionForm, SignupForm
from django.shortcuts import render, HttpResponse, redirect
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

csv_file_path = os.path.join(os.path.dirname(__file__), "data", "noOutlierDta.csv")
json_file_path = os.path.join(os.path.dirname(__file__), "data", "data.json")
df = pd.read_csv(csv_file_path)
jdf = pd.read_json(json_file_path)


@login_required(login_url="login")
def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def chart1_view(request):
    url = "https://www.worldometers.info/gdp/gdp-by-country/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        rows = rows[1:]

        gdp = {"Country": [], "Gdp": []}

        for row in rows:
            columns = row.find_all("td")
            country = columns[1].text
            gdp_value = columns[2].text
            gdp["Country"].append(country)
            gdp["Gdp"].append(int(gdp_value[1:].replace(",", "")))

        df = pd.DataFrame(gdp)

        df_pie = df.copy()
        df_pie.loc[df_pie["Gdp"] <= 2010430000000, "Country"] = "Other"
        df_pie = df_pie.groupby("Country")["Gdp"].sum().reset_index()
        df_pie = df_pie.sort_values(["Gdp"], ascending=[False])
        df_pie.reset_index(drop=True, inplace=True)

        chart_data = {
            "labels": df_pie["Country"].tolist(),
            "data": df_pie["Gdp"].tolist(),
            "backgroundColor": [
                "#e91e63",
                "#00e676",
                "#ff5722",
                "#1e88e5",
                "#ffd600",
            ],
        }

        # Create a JSON representation of the data for the doughnut chart
        doughnut_data = {
            "labels": df_pie["Country"].tolist(),
            "data": df_pie["Gdp"].tolist(),
            "backgroundColor": [
                "#e91e63",
                "#00e676",
                "#ff5722",
                "#1e88e5",
                "#ffd600",
            ],
        }

        chart_data_json = json.dumps(chart_data)
        doughnut_data_json = json.dumps(doughnut_data)

        # Render both the pie chart and doughnut chart in the template
        return render(
            request,
            "chart1.html",
            {
                "chart_data_json": chart_data_json,
                "doughnut_data_json": doughnut_data_json,
            },
        )


@login_required(login_url="login")
def chart2_view(request):
    # Your web scraping code to fetch population data
    r = requests.get(
        "https://www.worldometers.info/world-population/population-by-country/"
    )
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    rows = rows[1:]

    population = {"Country": [], "Population": []}

    for row in rows:
        columns = row.find_all("td")
        country = columns[1].text
        population_value = columns[2].text.replace(",", "")
        population["Country"].append(country)
        population["Population"].append(int(population_value))

    # Create a DataFrame for further processing
    df = pd.DataFrame(population)

    # Filter and aggregate data for the pie chart
    df_pie = df.copy()
    df_pie.loc[df_pie["Population"] <= 128455567, "Country"] = "Other"
    df_pie = df_pie.groupby("Country")["Population"].sum().reset_index()
    df_pie = df_pie.sort_values(["Population"], ascending=[False])
    df_pie.reset_index(drop=True, inplace=True)

    # Create a JSON representation of the data
    chart_data = {
        "labels": df_pie["Country"].tolist(),
        "data": df_pie["Population"].tolist(),
        "backgroundColor": [
            "#e91e63",
            "#00e676",
            "#ff5722",
            "#1e88e5",
            "#ffd600",
        ],
    }

    chart_data_json = json.dumps(chart_data)

    return render(request, "chart2.html", {"chart_data_json": chart_data_json})


@login_required(login_url="login")
def chart3_view(request):
    # Web scraping CO2 emissions data
    url = "https://www.worldometers.info/co2-emissions/co2-emissions-by-country/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        rows = rows[1:]

        population = {"Country": [], "CO2 EMISSIONS": []}

        for row in rows:
            columns = row.find_all("td")
            country = columns[1].text
            population_value = columns[2].text

            if isinstance(population_value, str):
                population_value = int(population_value.replace(",", ""))
            else:
                population_value = int(population_value)

            population["Country"].append(country)
            population["CO2 EMISSIONS"].append(population_value)

        df = pd.DataFrame(population)

        df_pie = df.copy()

        df_pie.loc[df_pie["CO2 EMISSIONS"] <= 530035650, "Country"] = "Other"
        df_pie = df_pie.groupby("Country")["CO2 EMISSIONS"].sum().reset_index()
        df_pie = df_pie.sort_values(["CO2 EMISSIONS"], ascending=[False])
        df_pie.reset_index(drop=True, inplace=True)

        labels = [i for i in df_pie["Country"]]

        chart_data = {
            "labels": labels,
            "data": df_pie["CO2 EMISSIONS"].tolist(),
            "backgroundColor": [
                "#e91e63",
                "#00e676",
                "#ff5722",
                "#1e88e5",
                "#ffd600",
            ],
        }

        chart_data_json = json.dumps(chart_data)

        return render(request, "chart3.html", {"chart_data_json": chart_data_json})


@login_required(login_url="login")
def details(req):
    # This context data shoud be dynamic
    context = {
        "price": "₹85.0 Lac",
        "EMI": 38,
        "Sqft": 1845,
        "location": "Vaishnodevi Circle, Ahmedabad",
        "BHK": 3,
        "Baths": 3,
        "Furnished Status": "Unfurnished",
        "basic_info_1": [
            {
                "key": "Beds",
                "value": 3,
            },
            {
                "key": "Baths",
                "value": 3,
            },
            {
                "key": "",
                "value": "Unfurnished",
            },
        ],
        "basic_info_2": [
            {"key": "Super Built-Up Area", "value": "1845 sqft"},
            {"key": "Developer", "value": "Satya Sankalp Group"},
            {"key": "Project", "value": "Satya Sankalp Sky"},
            {"key": "Transaction Type", "value": "New Property"},
            {"key": "Status", "value": "Ready to Move"},
            {"key": "Lifts", "value": 2},
            {"key": "Furnished Status", "value": "Unfurnished"},
        ],
        "Contact_builder": "",
        "Download_brochure": "",
        "Why_buy_in_this_project": [
            "Single tower",
            "Only 50 Luxurious Flat",
            "1 Flat having 2 Seating Balconies",
            "Common plot with G+2 Club House",
            "Nearby S P Ring Road",
            "Nearby Shaligram Lake View",
            "Nearby Auda Garden",
            "Nearby SSPCT Sankul",
            "Nearby SG Highway",
            "Nearby Nirma University",
            "Nearby Zydus Corporate Park",
        ],
        "More_Details": [
            {"key": "Price Breakup", "value": "₹85 Lac"},
            {"key": "Booking Amount", "value": "₹100000"},
            {
                "key": "RERA ID",
                "value": "PR/GJ/AHMEDABAD/AHMEDABAD CITY/AUDA/MAA08643/180621",
            },
            {
                "key": "Address",
                "value": "Vaishnodevi Circle, Ahmedabad - North, Gujarat",
            },
            {"key": "Furnishing", "value": "Unfurnished"},
            {"key": "Loan Offered", "value": "Estimated EMI: ₹38336"},
            {"key": "Water Availability", "value": "24 Hours Available"},
            {"key": "Status of Electricity", "value": "No/Rare Powercut"},
            {"key": "Floors allowed for construction", "value": 12},
            {"key": "Lift", "value": 2},
        ],
        "Amenities": [
            "Lift",
            "Rain Water Harvesting",
            "Club House",
            "Gymnasium",
            "Reserved Parking",
            "Security",
            "Private Terrace/Garden",
            "Vaastu Compliant",
            "Intercom Facility",
            "Maintenance Staff",
            "Waste Disposal",
            "Cafeteria/Food Court",
            "Outdoor Tennis Courts",
            "Mini Cinema Theatre",
            "Grand Entrance lobby",
            "Multipurpose Hall",
            "CCTV Camera",
            "Kids play area",
            "Fire Fighting Equipment",
            "Sewage treatment plant",
            "Community Hall",
        ],
    }
    return render(req, "Details.html", context)


@login_required(login_url="login")
def card(request):
    jdf_dict = jdf.to_dict(orient="records")
    context = {"json_data": jdf_dict}
    return render(request, "card.html", context)


@login_required(login_url="login")
def search(request):
    return render(request, "search.html")


def userlogin(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username or Password is incorrect!!!")
                # return HttpResponse("Username or Password is incorrect!!!")

        return render(request, "login.html")


def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = SignupForm()
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("home")
                # return HttpResponse(user , "User Created Successfully!!!")

        context = {"form": form}
        return render(request, "signup.html", context)
    

@login_required(login_url="login")
def predict_price(request):
    if request.method == "POST":
        form = PricePredictionForm(request.POST)
        if form.is_valid():
            model_path = os.path.join(
                os.path.dirname(__file__), "models", "rfr4model.pkl"
            )
            model = joblib.load(model_path)

            new_data = np.array(list(form.cleaned_data.values())).reshape(1, -1)

            predicted_price = model.predict(new_data)[0]

            context = {
                "form": form,
                "predicted_price": round(predicted_price, 2),
            }
            return render(request, "prediction.html", context)
    else:
        form = PricePredictionForm()

    context = {"form": form}
    return render(request, "prediction.html", context)


@login_required(login_url="login")
def data(request):
    jdf_dict = jdf.to_dict(orient="records")
    context = {"json_data": jdf_dict}
    return render(request, "card.html", context)
