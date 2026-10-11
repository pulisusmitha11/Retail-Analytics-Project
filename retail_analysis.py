
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset
df = pd.read_excel("Online Retail.xlsx")

print("===== RETAIL ANALYTICS PROJECT =====")
print("Original dataset shape:", df.shape)

# 2. Data cleaning
df = df.drop_duplicates()
df = df.dropna(subset=["Description", "CustomerID"])

# Remove cancelled invoices and invalid sales records
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Convert invoice date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Calculate sales
df["Sales"] = df["Quantity"] * df["UnitPrice"]

print("\n===== DATA CLEANING =====")
print("Cleaned dataset shape:", df.shape)
print("Missing values after cleaning:")
print(df.isnull().sum())

# 3. Total sales
total_sales = df["Sales"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()

print("\n===== SALES SUMMARY =====")
print(f"Total Sales: £{total_sales:,.2f}")
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)

# 4. Top 10 products by sales
top_products = (
    df.groupby("Description")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PRODUCTS =====")
print(top_products)

# 5. Sales by country
country_sales = (
    df.groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 COUNTRIES =====")
print(country_sales)

# 6. Monthly sales
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Sales"].sum()

# 7. Create visualizations
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))
top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales (£)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("top_products.png")
plt.show()

plt.figure(figsize=(12, 6))
country_sales.sort_values().plot(kind="barh")
plt.title("Top 10 Countries by Sales")
plt.xlabel("Sales (£)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("country_sales.png")
plt.show()

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.show()

# 8. Save cleaned data
df.to_csv("cleaned_retail_data.csv", index=False)

print("\nProject completed successfully!")
print("Saved: cleaned_retail_data.csv")
print("Saved: top_products.png, country_sales.png, monthly_sales.png")
