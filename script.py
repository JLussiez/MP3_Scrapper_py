# IMPORT ZONE ------
import requests
import json
import pandas as pd
# ------------------

url = "https://tchungle.com"
limit = "2"
page = "1"

def get_json(url, limit, page):
    url_json = url + "/products.json?limit=" + limit + '&page=' + page
    try:
        response = requests.get(url_json)
        response.raise_for_status()  # Gestion error HTTP
        text = response.text
        datas = json.loads(text)
        products = []

        for data in datas.get('products', []):
            product = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        product[f"{key}_{sub_key}"] = sub_value
                else:
                    product[key] = value
            products.append(product)
        return products

    except requests.exceptions.ConnectionError as e:
        return {'error': f"Connexion impossible: {e}"}

    except requests.exceptions.Timeout as e:
        return {'error': f"Délai dépassé: {e}"}

    except requests.exceptions.RequestException as e:
        return {'error': f"Erreur: {e}"}

products = get_json(url, limit, page)


def json_to_df(products):
    try:
        # Créer une DataFrame principale à partir des produits
        df_main = pd.json_normalize(products)
        print(df_main.iloc[0])
        return df_main
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage JSON : {e}")
        return None
    
df_main = json_to_df(products)

def get_others(df_main):
    try:
        # Dénormaliser les colonnes avec des listes de dictionnaires
        df_variants = pd.json_normalize(df_main['variants']).add_prefix('variants_')
        df_images = pd.json_normalize(df_main['images']).add_prefix('images_')
        df_options = pd.json_normalize(df_main['options']).add_prefix('options_')
        # Concaténer les DataFrames dénormalisées avec la DataFrame principale
        df_result = pd.concat([df_main, df_variants, df_images, df_options], axis=1)
        print(df_result.iloc[0])
        return df_result
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage JSON : {e}")
        return None

get_others(df_main)



# 6/
# def get_csv(df_variants, filename="output.csv"):
#     try:
#         # Utiliser to_csv pour générer le fichier CSV
#         df_variants.to_csv(filename, index=False)
#         print(f"Le fichier CSV '{filename}' a été généré avec succès.")
#     except Exception as e:
#         print(f"Une erreur s'est produite lors de la génération du fichier CSV : {e}")
