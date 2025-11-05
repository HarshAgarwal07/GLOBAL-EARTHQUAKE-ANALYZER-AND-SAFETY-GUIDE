# GLOBAL-EARTHQUAKE-ANALYZER-AND-SAFETY-GUIDE
# OVERVIEW

This Python command-line application allows users to analyze a large global earthquake dataset (M5.0+ from 2015-2025) and access a vital earthquake safety guide. The tool uses `pandas` and `numpy` for data analysis and `matplotlib` with `geopandas` to generate a geospatial visualization of global earthquake hotspots, clearly showing the "Ring of Fire."




## Features

This tool provides a simple, menu-driven interface with the following features:

1.  **Plot Global Hotspots (Ring of Fire):** Generates a world map and plots all 17,000+ earthquakes as a scatter plot, visually identifying tectonic boundaries and high-risk zones.
2.  **Show Top 10 Strongest Earthquakes:** Lists the top 10 most powerful earthquakes from the dataset, along with their magnitude, date, and location.
3.  **Country-Specific Analysis:**
    * Lists the top 10 most seismically active countries.
    * Provides a detailed statistical report (count, mean/max magnitude, depth) for any user-specified country.
    * Offers a side-by-side comparison of statistics for any two countries.
4.  **Show Advanced Analysis (Time/Depth):**
    * Categorizes quakes into "Shallow," "Intermediate," and "Deep" to show their distribution.
    * Lists the total number of quakes per year in the dataset.
    * Analyzes whether quakes occurred more often during the "Day" or at "Night."
5.  **Show Earthquake Safety Guide:** A vital social welfare feature that provides clear, actionable precautionary measures for before, during, and after an earthquake.

---

## How to Use

### 1. Prerequisites

You must have Python 3 installed, along with the following libraries:
* `pandas`
* `numpy`
* `matplotlib`
* `geopandas`

### 2. Installation

You can install all required libraries using pip:

```bash
pip install pandas numpy matplotlib geopandas
