import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import csv


YOUR_CSV_FILENAME = r'C:\Users\ESI03\Downloads\query.csv'

def load_data(filename):
    """
    Loads and preprocesses the earthquake data from the CSV file.
    This function adds new columns for 'country' and time analysis.
    
    MODIFIED: This function now uses Python's built-in open()
    and csv modules to read the file.
    """
    print(f"Loading data from '{filename}'...")
    data = []
    header = []
    try:

        # Use built-in open() to read the file
        with open(filename, 'r', encoding='utf-8') as f:
            # Create a CSV reader object
            reader = csv.reader(f)
            
            # Read the first line, which is the header
            header = next(reader)
            
            # Loop through the rest of the rows and add them to our data list
            for row in reader:
                data.append(row)
        
        print(f"Read {len(data)} rows from CSV...")
        
        # Create the pandas DataFrame from the header and data
        df = pd.DataFrame(data, columns=header)
        
        # --- END NEW CODE ---
        
    except FileNotFoundError:
        print(f"\n--- ERROR ---")
        print(f"File not found: '{filename}'")
        print("Please download the CSV and place it in the same folder as this script.")
        return None
    except Exception as e:
        print(f"\nAn error occurred while loading the file: {e}")
        return None

    # --- Pre-processing Data ---
    
    # 1. Manually convert data types
    #    When loading from a list, all data is text. We must convert it.
    try:
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['mag'] = pd.to_numeric(df['mag'], errors='coerce')
        df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
    except KeyError as e:
        print(f"\n--- ERROR ---")
        print(f"A required column is missing from the CSV: {e}")
        print(f"Please check your CSV file. Expected columns: 'time', 'latitude', 'longitude', 'mag', 'depth'")
        return None

    # 2. Extract country from 'place' column.
    def extract_country(place):
        # Handle cases where the 'place' is empty (NaN) or has no comma
        if pd.isna(place) or ',' not in place:
            return 'Unknown'
        
        # Get the last part of the string after the final comma
        # .strip() removes any extra spaces
        country = place.split(',')[-1].strip()
        
        # A simple cleanup for common "of" places (e.g., "south of Fiji")
        if ' of ' in country:
            country = country.split(' of ')[-1].strip()
            
        return country

    # 'apply' runs our 'extract_country' function on every row
    df['country'] = df['place'].apply(extract_country)
    
    # 3. Create new time columns for analysis
    # .dt allows us to access datetime properties
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month_name()
    df['hour'] = df['time'].dt.hour
    
    # 4. Drop any rows where essential data is missing
    df = df.dropna(subset=['time', 'latitude', 'longitude', 'mag', 'depth'])
    
    print(f"Successfully loaded and processed {len(df)} earthquake records.")
    return df


def show_safety_info():
    """
    Displays static, text-based safety information.
    """
    print("\n" + "="*40)
    print("      EARTHQUAKE SAFETY GUIDE")
    print("="*40)
    
    # We use a dictionary to store the safety tips
    safety_info = {
        "Before": [
            "1. Create an emergency plan with your family.",
            "2. Prepare a 'Go Bag' with water, first-aid, food, and a flashlight.",
            "3. Secure heavy furniture (bookshelves, TVs) to the wall."
        ],
        "During": [
            "1. DROP, COVER, and HOLD ON.",
            "2. If indoors, stay inside. Move away from windows and falling objects.",
            "3. If outdoors, move to an open area away from buildings and power lines."
        ],
        "After": [
            "1. Check yourself and others for injuries. Provide first aid.",
            "2. Be prepared for aftershocks. Drop, cover, and hold on.",
            "3. If in a damaged building, get out. Do not use elevators."
        ]
    }

    # Loop through the dictionary and print each tip
    for category, tips in safety_info.items():
        print(f"\n--- {category.upper()} AN EARTHQUAKE ---")
        for tip in tips:
            print(f"  {tip}")
    print("="*40)


def plot_ring_of_fire(df):
    """
    Generates a scatter plot map showing global earthquake hotspots.
    NOW INCLUDES A WORLD MAP BACKGROUND.
    """
    print("\nGenerating 'Ring of Fire' map...")
    try:
        # --- MODIFIED CODE ---
        # Load a world map from a reliable online GeoJSON file
        world_map_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
        print("Loading world map from online source...")
        world = gpd.read_file(world_map_url)
        
        # Start a new plot
        # 'fig' is the whole window, 'ax' is the plot itself
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Draw the world map (the continents) as the base layer
        world.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.5)
        # --- END MODIFIED CODE ---

        # Create a scatter plot on the *same axes* (ax)
        ax.scatter(
            df['longitude'],  # X-axis
            df['latitude'],   # Y-axis
            c='red',          # Dot color
            alpha=0.3,        # Transparency (to show density)
            s=df['mag'] * 1.5, # Size dots by magnitude
            label="Earthquakes (M5.0+)" # Add a label
        )
        
        # Set map boundaries
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        
        # Add labels and title
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title(f"Global Earthquake Hotspots (M{df['mag'].min()}+)\nShowing the 'Ring of Fire'")
        ax.grid(True)
        ax.legend()
        
        print("Showing plot in a new window. Close the plot window to continue.")
        # This command opens the plot window
        plt.show()
        
    except Exception as e:
        print(f"An error occurred while plotting: {e}")
        print("Could not display graph. Make sure matplotlib & geopandas are installed.")


def show_top_10_strongest(df):
    """
    Finds and prints the 10 strongest earthquakes in the dataset.
    """
    print("\n" + "="*40)
    print("   TOP 10 STRONGEST EARTHQUAKES")
    print("="*40)
    
    # Sort the entire DataFrame by 'mag' in descending order and take the top 10
    top_10 = df.sort_values(by='mag', ascending=False).head(10)
    
    # Format the output for readability
    for index, row in top_10.iterrows():
        print(f"\nMagnitude: {row['mag']:.1f}")
        print(f"     Time: {row['time'].date()}")
        print(f"    Place: {row['place']}")
        print(f"    Depth: {row['depth']:.1f} km")
    print("="*40)


def analyze_countries(df):
    """
    Provides a sub-menu for country-specific analysis.
    """
    # This loop keeps the country menu running until the user chooses '4'
    while True:
        print("\n" + "="*40)
        print("      Country-Specific Analysis")
        print("="*40)
        print("1. Show Top 10 Most Active Countries")
        print("2. Show Report for a Specific Country")
        print("3. Compare Two Countries")
        print("4. Return to Main Menu")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # --- Top 10 Active Countries ---
            print("\n--- Top 10 Most Active Countries (by M5.0+ quake count) ---")
            # We filter out 'Unknown' countries for a cleaner list
            # .value_counts() is a fast way to count unique items
            top_countries = df[df['country'] != 'Unknown']['country'].value_counts().head(10)
            print(top_countries)
            
        elif choice == '2':
            # --- Single Country Report ---
            country_name = input("Enter country name (e.g., Japan, Indonesia, USA): ").strip()
            # Filter the DataFrame to only rows where the country matches
            # .str.lower() makes the comparison case-insensitive
            country_df = df[df['country'].str.lower() == country_name.lower()]
            
            if country_df.empty:
                print(f"No data found for '{country_name}'. Check spelling or try another.")
            else:
                print(f"\n--- Analysis Report for {country_name} ---")
                print(f"Total Quakes (M5.0+): {len(country_df)}")
                # .describe() gives a quick statistical summary
                print(country_df[['mag', 'depth']].describe())

        elif choice == '3':
            # --- Compare Two Countries ---
            c1_name = input("Enter first country name: ").strip()
            c2_name = input("Enter second country name: ").strip()
            
            c1_df = df[df['country'].str.lower() == c1_name.lower()]
            c2_df = df[df['country'].str.lower() == c2_name.lower()]
            
            if c1_df.empty or c2_df.empty:
                print("Could not find data for one or both countries. Please check spelling.")
            else:
                # Simplified print statements for easier reading
                print("\n" + "="*40)
                print(f"--- Comparison: {c1_name} vs. {c2_name} ---")
                print(f"Total Quakes: \t{c1_name} = {len(c1_df)}, \t{c2_name} = {len(c2_df)}")
                print(f"Avg. Magnitude: \t{c1_name} = {c1_df['mag'].mean():.2f}, \t{c2_name} = {c2_df['mag'].mean():.2f}")
                print(f"Max. Magnitude: \t{c1_name} = {c1_df['mag'].max():.2f}, \t{c2_name} = {c2_df['mag'].max():.2f}")
                print(f"Avg. Depth (km): \t{c1_name} = {c1_df['depth'].mean():.1f}, \t{c2_name} = {c2_df['depth'].mean():.1f}")
                print("="*40)
        
        elif choice == '4':
            break # Exit the 'while True' loop
        else:
            print("Invalid choice, please try again.")
        
        if choice in ['1', '2', '3']:
            input("\nPress Enter to return to the Country Menu...")

print("WELCOME! Please wait while the program loads...")
def show_advanced_analysis(df):
    """
    Shows time-based and depth-based analysis.
    """
    print("\n" + "="*40)
    print("        Advanced Analysis")
    print("="*40)
    
    # --- 1. Depth Analysis ---
    print("\n--- Analysis by Depth ---")
    # pd.cut creates categories. We define the 'bins' (edges)
    # Using 9999 as a stand-in for infinity
    bins = [-9999, 70, 300, 9999]
    labels = ['Shallow (0-70km)', 'Intermediate (70-300km)', 'Deep (300km+)']
    df['depth_category'] = pd.cut(df['depth'], bins=bins, labels=labels, right=False)
    
    print("Quake Count by Depth:")
    print(df['depth_category'].value_counts())
    print("\n(Note: Shallow quakes are often the most destructive.)")

    # --- 2. Time Analysis (Year) ---
    print("\n--- Analysis by Year ---")
    print("Total Quakes per Year in this Dataset:")
    # .sort_index() sorts the result by year instead of by count
    print(df['year'].value_counts().sort_index())
    
    # --- 3. Time Analysis (Day vs. Night) ---
    print("\n--- Analysis by Time of Day ---")
    # We define hour 7 (7am) to 18 (6pm) as 'Day'
    bins = [-1, 6, 18, 24] # Bins are 0-6, 7-18, 19-23
    labels = ['Night (00:00 - 06:59)', 'Day (07:00 - 18:59)', 'Night (19:00 - 23:59)']
    df['day_night'] = pd.cut(df['hour'], bins=bins, labels=labels, right=True)
    
    print("Quake Count by Time of Day:")
    print(df['day_night'].value_counts())
    print("="*40)


def show_menu():
    print("\n" + "*"*50)
    print("    GLOBAL EARTHQUAKE ANALYZER & SAFETY GUIDE")
    print("*"*50)
    print("1. Plot Global Hotspots (Ring of Fire)")
    print("2. Show Top 10 Strongest Earthquakes")
    print("3. Country-Specific Analysis")
    print("4. Show Advanced Analysis (Time/Depth)")
    print("5. Show Earthquake Safety Guide")
    print("6. Exit")
    print("*"*50)


# --- Run the main program ---
# This code is now at the "top level" of the script.
# It will run as soon as Python reads the file.

# Load and process the data once at the start
earthquake_data = load_data(YOUR_CSV_FILENAME)

# If data loading fails, exit the program
if earthquake_data is None:
    input("Press Enter to exit.")
else:
    # This 'while True' loop creates the main menu.
    # It will keep running until the user selects '6'.
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            plot_ring_of_fire(earthquake_data)
        
        elif choice == '2':
            show_top_10_strongest(earthquake_data)
        
        elif choice == '3':
            analyze_countries(earthquake_data)
            
        elif choice == '4':
            show_advanced_analysis(earthquake_data)
            
        elif choice == '5':
            show_safety_info()
            
        elif choice == '6':
            print("Exiting program. Stay safe!")
            break # This is what exits the 'while True' loop
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        # Pause the program so the user can read the output
        # We don't pause after plotting, as the plot window
        # already pauses the code.
        if choice in ['2', '4', '5']:
            input("\nPress Enter to return to the main menu...")

