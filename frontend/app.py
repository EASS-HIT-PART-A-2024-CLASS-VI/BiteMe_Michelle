import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="🍔 BiteMe - Food Ordering", page_icon="🍕", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #ff5733;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #c70039;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Title & Header ---
st.title("🍔 Welcome to BiteMe - Your Favorite Food Ordering App!")

# --- Fetch Data for Dropdowns ---
try:
    cities_response = requests.get("http://localhost:8000/restaurant/get-cities")
    dishes_response = requests.get("http://localhost:8000/restaurant/get-dishes")
    restaurants_response = requests.get("http://localhost:8000/restaurant/get-restaurants")

    cities = cities_response.json().get("cities", []) if cities_response.status_code == 200 else []
    dishes = dishes_response.json().get("dishes", []) if dishes_response.status_code == 200 else []
    restaurants = restaurants_response.json().get("restaurants", []) if restaurants_response.status_code == 200 else []
except Exception as e:
    cities, dishes, restaurants = [], [], []
    st.error(f"⚠️ Failed to fetch data for dropdowns: {e}")

# --- Search Section ---
st.subheader("🔍 Search for Food")

# --- Dropdown Fields ---
search_type = st.selectbox("Search by", ["City", "Dish", "Restaurant"])

if search_type == "City":
    search_query = st.selectbox("Select a city", cities)
elif search_type == "Dish":
    search_query = st.selectbox("Select a dish", dishes)
elif search_type == "Restaurant":
    search_query = st.selectbox("Select a restaurant", restaurants)
else:
    search_query = None

if st.button("Search 🔍"):
    if not search_query:
        st.error("Please select a value from the dropdown.")
    else:
        try:
            # Map search types to API endpoints
            endpoint_map = {
                "City": "get-by-city",
                "Dish": "get-by-dish",
                "Restaurant": "get-by-name"
            }
            endpoint = endpoint_map[search_type]
            response = requests.get(f"http://localhost:8000/restaurant/{endpoint}?query={search_query}")

            # Process the response
            if response.status_code == 200:
                data = response.json()
                results = data.get("restaurants", []) if search_type != "Restaurant" else [data.get("restaurant", {})]
                if results:
                    st.success(f"Found {len(results)} result(s) for {search_type.lower()} '{search_query}':")
                    for r in results:
                        st.write(f"✅ **{r.get('name', 'N/A')}** - 📍 {r.get('city', 'N/A')}")
                else:
                    st.warning(f"No results found for {search_type.lower()} '{search_query}'.")
            else:
                st.error("Failed to fetch results from the server.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Footer ---
st.markdown("### ❤️ Built with Streamlit for a delightful ordering experience!")
