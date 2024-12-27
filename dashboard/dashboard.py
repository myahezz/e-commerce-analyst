import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="order_purchase_timestamp").agg(
        {"order_id": "nunique", "price": "sum"}
    )
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(
        columns={"order_id": "order_count", "price": "revenue"}, inplace=True
    )

    return daily_orders_df


def create_sum_order_items_df(df):
    sum_order_items_df = (
        df.groupby("product_category_name_english")
        .order_item_id.sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return sum_order_items_df

def create_bypayment_df(df):
    bypayment_df = df.groupby(by="payment_type").customer_id.nunique().reset_index()
    bypayment_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return bypayment_df

def create_byreview_df(df):
    byreview_df = df.groupby(by="review_score").customer_id.nunique().reset_index()
    byreview_df.rename(columns={"customer_id": "customer_count"}, inplace=True)

    return byreview_df

main_data_df = pd.read_csv("main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_estimated_delivery_date"]
main_data_df.sort_values(by="order_purchase_timestamp", inplace=True)
main_data_df.reset_index(inplace=True)

for column in datetime_columns:
    main_data_df[column] = pd.to_datetime(main_data_df[column])

# Filter data
min_date = main_data_df["order_purchase_timestamp"].min()
max_date = main_data_df["order_purchase_timestamp"].max()



start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )


main_df = main_data_df[
    (main_data_df["order_purchase_timestamp"] >= str(start_date))
    & (main_data_df["order_purchase_timestamp"] <= str(end_date))
]


daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bypayment_df = create_bypayment_df(main_df)
byreview_df = create_byreview_df(main_df)

# plot number of daily orders (2021)
st.header("Dashboard E-Commerce Public Dataset ")
st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(
        daily_orders_df.revenue.sum(), "USD", locale="es_CO"
    )
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15, rotation=45)

st.pyplot(fig)


# Product performance
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="order_item_id",
    y="product_category_name_english",
    data=sum_order_items_df.head(5),
    palette=colors,
    ax=ax[0],
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

sns.barplot(
    x="order_item_id",
    y="product_category_name_english",
    data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5),
    palette=colors,
    ax=ax[1],
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)

st.pyplot(fig)