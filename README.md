Here’s an updated, more structured version of your instructions in English, with a bit of elaboration to make it feel less like an AI-generated response:

---

# 🚲 **Bike Sharing Dashboard Setup** ✨

## **Environment Setup - Anaconda**

If you prefer using Anaconda for your environment setup, follow these steps:

```bash
conda create --name bike-sharing-env python=3.9
conda activate bike-sharing-env
pip install -r requirements.txt
```

This will create a new environment called `bike-sharing-env` and install all the required dependencies listed in `requirements.txt`.

## **Environment Setup - Shell/Terminal**

For those comfortable with the command line interface, here’s how you can set up your project:

```bash
mkdir bike_sharing_project
cd bike_sharing_project
pipenv install
pipenv shell
pip install -r requirements.txt
```

This will create the project directory, install the necessary virtual environment with `pipenv`, and then install the required packages.

## **Running the Streamlit App**

To start the pre-configured Streamlit app, simply run the following command in your terminal:

```bash
streamlit run app/dashboard.py
```

Make sure to replace `app/dashboard.py` with the correct path if your dashboard file is located elsewhere.

---

