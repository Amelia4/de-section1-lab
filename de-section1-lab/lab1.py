import pandera as pa
from pandera import Column, Check
from pathlib import Path
import pandas as pd
import duckdb


# Folder
BRONZE = Path("data/bronze")
SILVER = Path("data/silver")
GOLD = Path("data/gold")

# Membuat folder jika belum ada
for p in [BRONZE, SILVER, GOLD]:
    p.mkdir(parents=True, exist_ok=True)

# Sumber data
RAW_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

# Fungsi extract ke bronze
def extract_to_bronze():
    df = pd.read_csv(RAW_URL)

    out_path = BRONZE / "tips_raw.csv"

    df.to_csv(out_path, index=False)

    print(f"[BRONZE] berhasil menyimpan {len(df)} baris data")

    return out_path

def transform_to_silver(bronze_path: Path):

    df = pd.read_csv(bronze_path)

    # Standardisasi nama kolom
    df.columns = [
        c.strip().lower().replace(" ", "_")
        for c in df.columns
    ]

    # Membuat persentase tip
    df["tip_pct"] = (
        df["tip"] / df["total_bill"]
    ).round(4)

    # Menambahkan tanggal kunjungan
    df["visit_datetime"] = pd.date_range(
        "2024-01-01",
        periods=len(df),
        freq="h"
    )

    # Mengubah beberapa kolom menjadi kategori
    cat_cols = ["sex", "smoker", "day", "time"]

    for c in cat_cols:
        df[c] = df[c].astype("category")

    # Simpan ke Parquet
    out_path = SILVER / "tips_clean.parquet"

    df.to_parquet(
        out_path,
        index=False
    )

    print(
        f"[SILVER] berhasil menyimpan {len(df)} baris data"
    )

    return out_path

def aggregate_to_gold(silver_path: Path):

    df = pd.read_parquet(silver_path)

    summary = (
        df.groupby(
            ["sex", "smoker", "day"],
            as_index=False
        )
        .agg(
            avg_tip_pct=("tip_pct", "mean"),
            total_revenue=("total_bill", "sum"),
            rows=("tip_pct", "count")
        )
    )

    out_path = GOLD / "tips_summary.parquet"

    summary.to_parquet(
        out_path,
        index=False
    )

    print(
        f"[GOLD] berhasil menyimpan {len(summary)} baris data"
    )

    return out_path

def query_examples():

    con = duckdb.connect(database=":memory:")

    # Query Silver Layer
    q1 = con.execute("""
    SELECT
        sex,
        smoker,
        AVG(tip_pct) AS avg_tip_pct,
        SUM(total_bill) AS revenue
    FROM read_parquet('data/silver/tips_clean.parquet')
    GROUP BY 1,2
    ORDER BY avg_tip_pct DESC
    """).df()

    print("\n=== SQL on Silver ===")
    print(q1)

    # Query Gold Layer
    q2 = con.execute("""
    SELECT
        day,
        AVG(avg_tip_pct) AS avg_tip_pct
    FROM read_parquet('data/gold/tips_summary.parquet')
    GROUP BY day
    ORDER BY avg_tip_pct DESC
    """).df()

    print("\n=== SQL on Gold ===")
    print(q2)

def validate_silver(silver_path: Path):

    schema = pa.DataFrameSchema({

        "total_bill": Column(
            float,
            Check.ge(0)
        ),

        "tip": Column(
            float,
            Check.ge(0)
        ),

        "tip_pct": Column(
            float,
            Check.in_range(0, 1),
            nullable=False
        ),

        "size": Column(
            int,
            Check.ge(1)
        ),

        "visit_datetime": Column(
            pa.DateTime
        )

    }, coerce=True)

    df = pd.read_parquet(silver_path)

    schema.validate(df, lazy=True)

    print("[QUALITY] Silver passed validation!")

if __name__ == "__main__":

    bronze_file = extract_to_bronze()

    silver_file = transform_to_silver(bronze_file)

    validate_silver(silver_file)

    aggregate_to_gold(silver_file)

    query_examples()