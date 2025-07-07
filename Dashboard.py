import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from pathlib import Path

# ── 1. CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="PhonePe Data Insights", layout="wide")
LABEL_SIZE   = 12     # Axes labels, tick labels
TITLE_SIZE   = 14     # All figure titles
LEGEND_SIZE  = 10     # Legend / annotation text
plt.rcParams.update({
    "font.size": LABEL_SIZE,
    "axes.labelsize": LABEL_SIZE,
    "xtick.labelsize": LABEL_SIZE,
    "ytick.labelsize": LABEL_SIZE,
    "axes.titlesize": TITLE_SIZE,
    "legend.fontsize": LEGEND_SIZE,
})

def _style_plotly(fig):
    """Apply consistent font sizes to Plotly figures."""
    fig.update_layout(
        title_font_size=TITLE_SIZE,
        legend_font_size=LEGEND_SIZE,
        xaxis_title_font_size=LABEL_SIZE,
        yaxis_title_font_size=LABEL_SIZE,
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(title=None),
    )
    return fig

# ── 2. DATA LOAD ───────────────────────────────────────────────────────────────
data_dir = Path(__file__).parent      # Change if CSVs are elsewhere
df1 = pd.read_csv(data_dir / "Decoding Transaction Dynamics on PhonePe.csv")       # state/year totals
df2 = pd.read_csv(data_dir / "Device Dominance and User Engagement Analysis.csv")  # device stats
df3 = pd.read_csv(data_dir / "Insurance Penetration and Growth Potential Analysis.csv")
df4 = pd.read_csv(data_dir / "Transaction Analysis for Market Expansion.csv")      # growth
df5 = pd.read_csv(data_dir / "User Engagement and Growth Strategy.csv")            # app‑opens
df_cat = pd.read_csv(data_dir / "agg_Trans.csv")                                   # category trends

# ── 3. SIDEBAR FILTERS ──────────────────────────────────────────────────────────
# Clean and combine state names from multiple dataframes
all_states = sorted(
    set(df1['state_name'].dropna().astype(str).unique()) |
    set(df3['state_name'].dropna().astype(str).unique()) |
    set(df4['state_name'].dropna().astype(str).unique()) |
    set(df5['state_name'].dropna().astype(str).unique())
)

# Sidebar multiselect filter for states
selected_states = st.sidebar.multiselect(
    "Filter by State(s)", all_states, default=all_states
)


all_categories = sorted(df_cat.category_name.unique())
selected_cats = st.sidebar.multiselect(
    "Filter by Category(s)", all_categories, default=all_categories
)

# Filter helper
def _f(df, col="state_name"):
    return df[df[col].isin(selected_states)] if col in df.columns else df

df1_f, df3_f, df4_f, df5_f = map(_f, [df1, df3, df4, df5])
df_cat_f = df_cat[df_cat.category_name.isin(selected_cats)]

# ── 4. LAYOUT – TABS ───────────────────────────────────────────────────────────
tabs = st.tabs([
    "📈 Transactions", "📂 Categories", "📱 Devices",
    "🛡 Insurance", "🚀 Growth", "👥 Engagement"
])

# ————————————————————————————————————————————————————————————————
with tabs[0]:
    st.header("Transactions")
    col1, col2 = st.columns(2)
    
    # 4.1 Yearly total transaction amount
    with col1:
        st.subheader("Total Transaction Amount by State (Yearly)")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df1_f, x="year", y="total_amount",
                     hue="state_name", marker="o", ax=ax)
        ax.set_ylabel("Total Amount (₹)")
        ax.set_xlabel("Year")
        ax.legend(title="State", bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig)

    # 4.2 Quarterly total_transactions
    with col2:
        st.subheader("Quarterly Transaction Count by State")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=df1_f, x="quarter", y="total_transactions",
                     hue="state_name", ax=ax)
        ax.set_ylabel("Total Transactions")
        ax.set_xlabel("Quarter")
        ax.legend(title="State", bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig)

    # 4.3 Heatmap
    st.subheader("Heatmap – Transactions per Quarter & State")
    pivot = df1_f.pivot_table(index="state_name", columns="quarter",
                              values="total_transactions", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, cmap="Blues", annot=True, fmt=".0f",
                annot_kws={"size": LEGEND_SIZE}, linewidths=.4, ax=ax)
    ax.set_xlabel("Quarter"); ax.set_ylabel("State")
    st.pyplot(fig)

    # 4.4 Stacked bar – total amount per quarter
    st.subheader("Stacked Bar – Transaction Amount per Quarter")
    fig = plt.figure(figsize=(10, 5))
    df_stacked = df1_f.groupby(["quarter", "state_name"])["total_amount"]\
                      .sum().unstack(fill_value=0)
    df_stacked.plot(kind="bar", stacked=True, ax=plt.gca())
    plt.xlabel("Quarter"); plt.ylabel("Transaction Amount (₹)")
    plt.legend(title="State", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)

# ————————————————————————————————————————————————————————————————
with tabs[1]:
    st.header("Category Trends")
    st.subheader("Transaction Amount Trend by Category")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_cat_f, x="year", y="amount",
                 hue="category_name", marker="o", ax=ax)
    ax.set_xlabel("Year"); ax.set_ylabel("Transaction Amount (₹)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Category")
    st.pyplot(fig)

# ————————————————————————————————————————————————————————————————
with tabs[2]:
    st.header("Device Metrics")

    c1, c2 = st.columns(2)
    # 2.1 Total registered users bar
    with c1:
        st.subheader("Total Registered Users by Brand")
        fig, ax = plt.subplots(figsize=(6, 4))
        df2.sort_values("total_registered_users", ascending=False).plot(
            x="brand", y="total_registered_users", kind="bar",
            color="mediumslateblue", ax=ax, legend=False)
        ax.set_xlabel("Brand"); ax.set_ylabel("Users")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 2.2 Average usage bar
    with c2:
        st.subheader("Average Usage Percentage by Brand")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=df2, x="brand", y="avg_percentage_usage",
                    palette="coolwarm", ax=ax)
        ax.set_xlabel("Brand"); ax.set_ylabel("Usage %")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 2.3 Pie share
    st.subheader("Share of Registered Users (Pie)")
    sizes = df2["total_registered_users"]; labels = df2["brand"]
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, _, _ = ax.pie(sizes, autopct="%1.1f%%", startangle=140,
                          pctdistance=0.75, textprops={"fontsize": LEGEND_SIZE})
    ax.legend(wedges, labels, title="Brands",
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.axis("equal")
    st.pyplot(fig)

    # 2.4 Sunburst (plotly)
    st.subheader("Usage Tier & Device Brand Distribution (Sunburst)")
    df2_sb = df2.copy()
    df2_sb["usage_tier"] = pd.cut(df2_sb["avg_percentage_usage"],
                                  bins=[0, .1, .2, .3],
                                  labels=["Low", "Medium", "High"]).astype(str)
    fig = px.sunburst(df2_sb, path=["usage_tier", "brand"],
                      values="total_registered_users",
                      title="Usage Tier and Device Brand Distribution")
    st.plotly_chart(_style_plotly(fig), use_container_width=True)

# ————————————————————————————————————————————————————————————————
with tabs[3]:
    st.header("Insurance")

    col1, col2 = st.columns(2)
    # 3.1 Policies sold over time
    with col1:
        st.subheader("Policies Sold – Yearly")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=df3_f, x="year", y="total_policies_sold",
                     hue="state_name", marker="o", ax=ax)
        ax.set_xlabel("Year"); ax.set_ylabel("Policies Sold")
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="State")
        st.pyplot(fig)

    # 3.2 Insurance value yearly
    with col2:
        st.subheader("Total Insurance Value – Yearly")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=df3_f, x="year", y="total_value",
                     hue="state_name", marker="o", ax=ax)
        ax.set_xlabel("Year"); ax.set_ylabel("Value (₹)")
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="State")
        st.pyplot(fig)

    # 3.3 Policies sold quarterly
    st.subheader("Policies Sold – Quarterly")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df3_f, x="quarter", y="total_policies_sold",
                 hue="state_name", marker="o", ax=ax)
    ax.set_xlabel("Quarter"); ax.set_ylabel("Policies Sold")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="State")
    st.pyplot(fig)

    # 3.4 Area chart insurance value growth
    st.subheader("Cumulative Insurance Value Growth (Area)")
    df_area = df3_f.copy()
    df_area["time"] = df_area["year"].astype(str) + "-Q" + df_area["quarter"].astype(str)
    df_area = df_area.sort_values(["state_name", "year", "quarter"])
    pivot_val = df_area.pivot(index="time", columns="state_name", values="total_value")
    fig = plt.figure(figsize=(10, 5))
    pivot_val.plot(kind="area", stacked=True, ax=plt.gca(), colormap="Accent")
    plt.xlabel("Year–Quarter"); plt.ylabel("Total Value (₹)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="State")
    st.pyplot(fig)

    # 3.5 Plotly bar – policies per quarter
    st.subheader("Policies per Quarter (Plotly)")
    fig = px.bar(df3_f, x="quarter", y="total_policies_sold",
                 color="state_name", text="total_policies_sold",
                 barmode="group", title="Insurance Policies Sold per Quarter")
    st.plotly_chart(_style_plotly(fig), use_container_width=True)

# ————————————————————————————————————————————————————————————————
with tabs[4]:
    st.header("Transaction Growth")

    # 4.1 Growth percent bar
    st.subheader("Growth Percentage by State")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df4_f.sort_values("growth_percent", ascending=False),
                x="growth_percent", y="state_name", palette="viridis", ax=ax)
    ax.set_xlabel("Growth (%)"); ax.set_ylabel("State")
    st.pyplot(fig)

    # 4.2 Bubble scatter – growth vs previous
    st.subheader("Growth vs Previous Transactions (Bubble)")
    fig = px.scatter(df4_f, x="previous_tx", y="growth",
                     size="current_tx", color="state_name",
                     hover_name="state_name", size_max=60,
                     title="Transaction Growth vs Previous Transactions")
    st.plotly_chart(_style_plotly(fig), use_container_width=True)

# ————————————————————————————————————————————————————————————————
with tabs[5]:
    st.header("User Engagement")

    # 5.1 Scatter – app opens vs users
    st.subheader("Registered Users vs App Opens")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df5_f, x="total_registered_users",
                    y="total_app_opens", hue="state_name",
                    size="total_registered_users", ax=ax, legend=False)
    ax.set_xlabel("Registered Users"); ax.set_ylabel("App Opens")
    for _, row in df5_f.iterrows():
        ax.text(row.total_registered_users, row.total_app_opens,
                row.state_name, fontsize=LEGEND_SIZE - 2)
    st.pyplot(fig)

    # 5.2 Plotly scatter – bubble
    st.subheader("Bubble – User Base vs App Opens")
    fig = px.scatter(df5_f, x="total_registered_users",
                     y="total_app_opens", size="total_registered_users",
                     color="state_name", hover_name="state_name",
                     size_max=60, title="User Base vs App Opens by State")
    st.plotly_chart(_style_plotly(fig), use_container_width=True)

# ── 5. FOOTER ─────────────────────────────────────────────────────────────────
st.success("✅ Dashboard loaded successfully!")
