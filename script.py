# IMPORT ZONE ------
import requests
import json
import pandas as pd
# ------------------

url = "https://tchungle.com"
limit = "2"
page = 1

# def get_json(url, limit, page):
#     url_json = url + "/products.json?limit=" + limit + '&page=' + page
#     try:
#         response = requests.get(url_json)
#         response.raise_for_status()  # Gestion error HTTP
#         text = response.text
#         datas = json.loads(text)
#         products = []

#         for data in datas.get('products', []):
#             product = {}
#             for key, value in data.items():
#                 if isinstance(value, dict):
#                     for sub_key, sub_value in value.items():
#                         product[f"{key}_{sub_key}"] = sub_value
#                 else:
#                     product[key] = value
#             products.append(product)
#         return products

#     except requests.exceptions.ConnectionError as e:
#         return {'error': f"Connexion impossible: {e}"}

#     except requests.exceptions.Timeout as e:
#         return {'error': f"Délai dépassé: {e}"}

#     except requests.exceptions.RequestException as e:
#         return {'error': f"Erreur: {e}"}

# products = get_json(url, limit, page)





def json_to_df(df_products):
    try:
        # Créer une DataFrame principale à partir des produits
        df_main = pd.json_normalize(df_products)
        print(df_main.iloc[0])
        return df_main
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage JSON : {e}")
        return None
    


def get_products(url):
    all_products = pd.DataFrame()
    page = 1
    while True:
        limit = "2"  # Choisissez la limite souhaitée
        url_json = f"{url}/products.json?limit={limit}&page={page}"

        try:
            response = requests.get(url_json)
            response.raise_for_status()  # Gestion error HTTP
            text = response.text
            data = json.loads(text)
            
            if not data.get('products'):
                break  # Aucun produit trouvé, sortir de la boucle

            products_df = json_to_df(data['products'])
            all_products = pd.concat([all_products, products_df], ignore_index=True)
            page += 1
            # test
            if page == 5:
                break

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            break  # Sortir de la boucle en cas d'erreur

    return all_products

df_products = get_products(url)
# print(df_products)

def get_variants(df_products):
    try:
        # Colonnes communes à tous les produits
        common_columns = ['id', 'title', 'handle', 'body_html', 'vendor', 'product_type', 'created_at', 'updated_at']

        # Colonnes spécifiques aux variants
        variant_columns = ['id', 'product_id', 'title', 'option1', 'option2', 'option3', 'sku', 'requires_shipping', 'taxable', 'featured_image', 'position', 'created_at', 'updated_at', 'compare_at_price', 'fulfillment_service', 'inventory_management', 'inventory_policy', 'inventory_quantity', 'old_inventory_quantity', 'inventory_quantity_adjustment', 'inventory_quantity_new', 'price', 'cost_price', 'selling_price', 'is_published', 'published_at', 'purchasable', 'total_sold', 'variant_created_at', 'variant_updated_at']

        # Filtrer les colonnes communes
        df_variants = df_products[common_columns].copy()

        # Ajouter les colonnes spécifiques aux variants
        for i in range(1, 4):
            option_column = f'option{i}'
            if option_column in df_products.columns:
                df_variants[option_column] = df_products[option_column]

        # Vérifier si les colonnes spécifiques aux variants existent dans df_products
        variant_columns_to_check = ['sku', 'price', 'inventory_quantity']
        if all(column in df_products.columns for column in variant_columns_to_check):
            # Ajouter d'autres colonnes spécifiques aux variants
            df_variants['sku'] = df_products['sku']
            df_variants['price'] = df_products['price']
            df_variants['inventory_quantity'] = df_products['inventory_quantity']
        else:
            raise ValueError("Certaines colonnes spécifiques aux variants sont manquantes dans le DataFrame df_products.")

        # Supprimer les colonnes avec l'indication "Valeur par défaut"
        columns_to_drop = ['compare_at_price', 'fulfillment_service', 'inventory_management', 'inventory_policy']
        df_variants = df_variants.drop(columns=columns_to_drop)

        return df_variants

    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement des variants : {e}")
        return None

# Gestion des erreurs lors de la génération du fichier CSV
def get_csv(df_variants, filename="output.csv"):
    try:
        if df_variants is not None:  # Vérifier si df_variants n'est pas None
            # Utiliser to_csv pour générer le fichier CSV
            df_variants.to_csv(filename, index=False)
            print(f"Le fichier CSV '{filename}' a été généré avec succès.")
        else:
            print("Le DataFrame df_variants est None. La génération du fichier CSV a échoué.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la génération du fichier CSV : {e}")

# Génération du fichier CSV
df_variants = get_variants(df_products)
get_csv(df_variants)



# def json_to_df(df_products):
#     try:
#         # Créer une DataFrame principale à partir des produits
#         df_main = pd.json_normalize(df_products)
#         print(df_main.iloc[0])
#         return df_main
#     except json.JSONDecodeError as e:
#         print(f"Erreur lors du décodage JSON : {e}")
#         return None
    
# df_main = json_to_df(df_products)

# def get_others(df_main):
#     try:
#         # Dénormaliser les colonnes avec des listes de dictionnaires
#         df_variants = pd.json_normalize(df_main['variants']).add_prefix('variants_')
#         df_images = pd.json_normalize(df_main['images']).add_prefix('images_')
#         df_options = pd.json_normalize(df_main['options']).add_prefix('options_')
#         # Concaténer les DataFrames dénormalisées avec la DataFrame principale
#         df_result = pd.concat([df_main, df_variants, df_images, df_options], axis=1)
#         print(df_result.iloc[0])
#         return df_result
#     except json.JSONDecodeError as e:
#         print(f"Erreur lors du décodage JSON : {e}")
#         return None

# get_others(df_main)



# 6/
# def get_csv(df_variants, filename="output.csv"):
#     try:
#         # Utiliser to_csv pour générer le fichier CSV
#         df_variants.to_csv(filename, index=False)
#         print(f"Le fichier CSV '{filename}' a été généré avec succès.")
#     except Exception as e:
#         print(f"Une erreur s'est produite lors de la génération du fichier CSV : {e}")
