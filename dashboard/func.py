import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
import streamlit as st

# Class untuk analisis data
class DataAnalyzer:
  def __init__(self, df):
    self.df = df

  def generate_daily_orders_summary(self):
    daily_summary = self.df.resample(rule='D', on='order_approved_at').agg({
      "order_id": "nunique",
      "payment_value": "sum"
    }).reset_index()
    daily_summary.rename(columns={
      "order_id": "order_count",
      "payment_value": "revenue"
    }, inplace=True)
    return daily_summary

  def generate_daily_spend_summary(self):
    daily_spend = self.df.resample(rule='D', on='order_approved_at').agg({
      "payment_value": "sum"
    }).reset_index()
    daily_spend.rename(columns={"payment_value": "total_spend"}, inplace=True)
    return daily_spend

  def generate_category_item_count(self):
    category_item_count = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
    category_item_count.rename(columns={"product_id": "product_count"}, inplace=True)
    category_item_count = category_item_count.sort_values(by='product_count', ascending=False)
    return category_item_count

  def analyze_review_scores(self):
    score_distribution = self.df['review_score'].value_counts().sort_values(ascending=False)
    most_frequent_score = score_distribution.idxmax()
    return score_distribution, most_frequent_score

  def analyze_customers_by_state(self):
    customer_summary = self.df.groupby("customer_state")["customer_id"].nunique().reset_index()
    customer_summary.rename(columns={"customer_id": "customer_count"}, inplace=True)
    most_frequent_state = customer_summary.loc[customer_summary['customer_count'].idxmax(), 'customer_state']
    customer_summary = customer_summary.sort_values(by='customer_count', ascending=False)
    return customer_summary, most_frequent_state

  def analyze_order_status(self):
    order_status_distribution = self.df["order_status"].value_counts().sort_values(ascending=False)
    most_frequent_status = order_status_distribution.idxmax()
    return order_status_distribution, most_frequent_status

# Class untuk visualisasi peta Brasil
class BrazilMapPlotter:
  def __init__(self, data, plt, mpimg, urllib, st):
    self.data = data
    self.plt = plt
    self.mpimg = mpimg
    self.urllib = urllib
    self.st = st

  def display_map(self):
    # Tautan ke gambar peta Brasil
    image_url = "https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg"

    try:
      # Mengambil gambar peta dari URL
      brazil_map = self.mpimg.imread(self.urllib.request.urlopen(image_url), 'jpg')
    except urllib.error.URLError:
      print("Error downloading image. Using placeholder")
      brazil_map = None  # Handle the error gracefully

    # Create a Matplotlib figure
    fig, ax = self.plt.subplots(figsize=(10, 10))

    # Tambahkan scatter plot ke axes
    ax.scatter(self.data["geolocation_lng"], self.data["geolocation_lat"],
              alpha=0.3, s=0.3, c='maroon')

    # Tambahkan gambar peta sebagai latar belakang (jika berhasil diunduh)
    if brazil_map is not None:
      ax.imshow(brazil_map, extent=[-73.98283055, -33.8, -33.75116944, 5.4])