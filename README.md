# Syaripatul Aini E-Commerce Dashboard ✨

Welcome to the **Syaripatul Aini Dashboard** project! This dashboard provides an interactive interface to analyze e-commerce data using **Streamlit**, **Pandas**, **Seaborn**, and **Matplotlib**. It includes features like daily order metrics, customer demographics, and geolocation analysis.

## Setup Environment - Anaconda

For those using **Anaconda** to set up the project environment, follow the steps below:

1. Create and activate a new Conda environment:
    ```bash
    conda create --name syaripatul-dashboard python=3.9
    conda activate syaripatul-dashboard
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup Environment - Shell/Terminal (using **Pipenv**)

If you prefer **Pipenv** for managing your virtual environment, follow these steps:

1. Create and navigate to the project directory:
    ```bash
    mkdir proyek_analisis_data
    cd proyek_analisis_data
    ```

2. Install **Pipenv** and activate the environment:
    ```bash
    pipenv install
    pipenv shell
    ```

3. Install the dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```


4.  To access the application, you need to upload the dataset as a zip file and the logo PNG file on the dashboard first. After that, you 
       ```can access the application directly.

    Instructions:
    Upload the zip file containing your dataset.
    Upload the gcl PNG file on the dashboard.
    Once the files are uploaded, the application will automatically process them and allow you to view the results.
    ```


## requirements.txt

The `requirements.txt` file includes all the necessary libraries for the project. Here are the contents of the file:

```
babel
numpy
matplotlib
pandas
seaborn
streamlit
folium
streamlit-folium

```

If you need additional libraries, you can add them to this file.

## Run Streamlit App

To run the **Streamlit** app, execute the following command in your terminal:

```bash
streamlit run Dashboard.py
```

Make sure to replace `dashboard.py` with the actual filename of your Streamlit app if it differs.

## Project Structure

Your project folder should have the following structure:

```
proyek_analisis_data/
│
├── dashboard.py            # Streamlit application file
├── requirements.txt        # List of project dependencies
├── main_data.csv           # Main dataset
├── geolocation_dataset.csv # Geolocation dataset
├── gcl.png                 # Image for the sidebar logo
```


