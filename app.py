import streamlit as st
import pandas as pd

# Load recipes CSV
df = pd.read_csv("recipe.csv")

# Convert ingredients to list
df['ingredients'] = df['ingredients'].apply(lambda x: [i.strip().lower() for i in x.split(';')])

# App title
st.title("Recipe Generator 🍳")
st.write("Enter ingredients you have and find recipes you can make!")

# User input
user_input = st.text_input("Enter ingredients (comma separated):")
user_ingredients = [i.strip().lower() for i in user_input.split(",")] if user_input else []

# Function to find matching recipes
def find_recipes(user_ingredients):
    matches = []
    for _, row in df.iterrows():
        common = set(user_ingredients) & set(row['ingredients'])
        if common:
            matches.append({
                "name": row['recipe_name'],
                "instructions": row['instructions'],
                "matched": list(common),
                "match_count": len(common)
            })
    matches.sort(key=lambda x: x['match_count'], reverse=True)
    return matches

# Display results
if user_ingredients:
    recipes = find_recipes(user_ingredients)
    if recipes:
        st.subheader("Recipes you can make:")
        for r in recipes:
            st.markdown(f"{r['name']}** (Matches: {r['match_count']})")
            st.markdown(f"*Matched Ingredients:* {', '.join(r['matched'])}")
            st.markdown(f"*Instructions:* {r['instructions']}")
            st.write("---")
    else:
        st.write("No matching recipes found.")