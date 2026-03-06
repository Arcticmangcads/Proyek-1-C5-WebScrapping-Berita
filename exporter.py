import pandas as pd

def export_to_csv(articles, filename="news.csv"):
    """
    //Menyimpan data artikel ke file CSV
    """

    df = pd.DataFrame(articles)

    df.to_csv(filename, index=False)

    print("Data berhasil disimpan ke CSV")

    def export_to_excel(articles, filename="news.xlsx"):
    """
    //Menyimpan data artikel ke file Excel
    """

    df = pd.DataFrame(articles)

    df.to_excel(filename, index=False)

    print("Data berhasil disimpan ke Excel")