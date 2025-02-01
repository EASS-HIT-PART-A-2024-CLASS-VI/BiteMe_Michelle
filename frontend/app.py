import streamlit as st
import requests

# Mock API base URL
API_BASE_URL = "http://localhost:8000"  # Update to match your backend

# Fetch data functions
def fetch_all_dishes():
    """Fetch all dishes from the backend."""
    response = requests.get(f"{API_BASE_URL}/dishes")
    if response.status_code == 200:
        return response.json()
    return []

def fetch_cities():
    """Fetch all available cities from the backend."""
    response = requests.get(f"{API_BASE_URL}/cities")
    if response.status_code == 200:
        return response.json()
    return []

def fetch_restaurants_by_city(city):
    """Fetch restaurants in a specific city from the backend."""
    response = requests.get(f"{API_BASE_URL}/restaurants/city/{city}")
    if response.status_code == 200:
        return response.json()
    return []

def main():
    st.set_page_config(page_title="BiteMe", page_icon="🍔", layout="wide")

    # Display logo (ensure the file exists in the working directory)
    st.image("biteme_logo.gif", use_container_width=True)

    st.title("Welcome to BiteMe!")
    st.subheader("Where cravings meet convenience 🍔🍕")

    # Navigation options
    st.header("Navigation Options:")
    option = st.selectbox("Choose an option", ["Browse Restaurants"])

    if option == "Browse Restaurants":
        st.subheader("Find Restaurants by:")

        search_by = st.radio("Search by:", ["City", "Cuisine", "Dish"])

        if search_by == "City":
            cities = fetch_cities()
            if cities:
                city = st.selectbox("Select a city:", cities)
                if st.button("Search"):
                    results = fetch_restaurants_by_city(city)
                    if results:
                        st.write("### Restaurants in", city)
                        for restaurant in results:
                            st.write(f"- **{restaurant['name']}**: {restaurant['type']} (City: {restaurant['city']})")
                    else:
                        st.write("No restaurants found in this city.")

        elif search_by == "Cuisine":
            st.write("Cuisine search not yet implemented.")

        elif search_by == "Dish":
            dishes = fetch_all_dishes()
            if dishes:
                dish = st.selectbox("Select a dish:", dishes)
                if st.button("Search"):
                    results = fetch_restaurants_by_dish(dish)
                    if results:
                        st.write("### Restaurants offering", dish)
                        for restaurant in results:
                            st.write(f"- **{restaurant['name']}** (City: {restaurant['city']})")
                    else:
                        st.write("No restaurants found offering this dish.")

if __name__ == "__main__":
    main()
