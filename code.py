# Import necessary libraries
import requests
import pandas as pd
import json
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Endpoints
KALSHI_API_URL = "https://api.elections.kalshi.com/trade-api/v2/events"
MANIFOLD_API_URL = "https://api.manifold.markets/v0/markets"
POLYMARKET_API_URL = "https://gamma-api.polymarket.com/markets"  # Assuming Polymarket uses the same endpoint

# # Add your API keys here (if required)
# KALSHI_API_KEY = os.getenv('KALSHI_API_KEY', 'your_kalshi_api_key_here')
# MANIFOLD_API_KEY = os.getenv('MANIFOLD_API_KEY', 'your_manifold_api_key_here')
# POLYMARKET_API_KEY = os.getenv('POLYMARKET_API_KEY', 'your_polymarket_api_key_here')  # If needed

# Agent 1: Data Collector
def data_collector():
    products = []
    
    # Fetch data from Kalshi
    try:
        headers = {
            'Authorization': f'Bearer {"https://api.elections.kalshi.com/trade-api/v2/events"}',
            'Accept': 'application/json'
        }
        response = requests.get(KALSHI_API_URL, headers=headers)
        response.raise_for_status()
        kalshi_data = response.json()
        
        # Debug: Log the API response structure
        logging.debug(f"Kalshi API response: {json.dumps(kalshi_data, indent=2)[:500]}...")
        
        # Process Kalshi data
        if 'events' in kalshi_data:
            for event in kalshi_data['events']:
                name = event.get('name', 'Unknown Event')
                price = event.get('last_price', 0) / 100  # Convert cents to dollars
                products.append({"name": name, "price": price, "source": "Kalshi"})
            logging.info(f"Collected {len(kalshi_data['events'])} products from Kalshi")
        else:
            logging.warning("No 'events' found in Kalshi API response")
    except Exception as e:
        logging.error(f"Error with Kalshi API: {str(e)}")

    # Fetch data from Manifold
    try:
        headers = {
            'Authorization': f'Key {"https://api.manifold.markets/v0/markets"}',
            'Accept': 'application/json'
        }
        response = requests.get(MANIFOLD_API_URL, headers=headers)
        response.raise_for_status()
        manifold_data = response.json()
        
        # Debug: Log the API response structure
        logging.debug(f"Manifold API response: {json.dumps(manifold_data, indent=2)[:500]}...")
        
        # Process Manifold data
        for market in manifold_data:
            name = market.get('question', 'Unknown Market')
            price = market.get('probability', 0) * 100  # Convert to percentage
            products.append({"name": name, "price": price, "source": "Manifold"})
        logging.info(f"Collected {len(manifold_data)} products from Manifold")
    except Exception as e:
        logging.error(f"Error with Manifold API: {str(e)}")

    # Fetch data from Polymarket
    try:
        headers = {
            'Authorization': f'Bearer {"https://gamma-api.polymarket.com/markets"}',
            'Accept': 'application/json'
        }
        response = requests.get(POLYMARKET_API_URL, headers=headers)
        response.raise_for_status()
        polymarket_data = response.json()
        
        # Debug: Log the API response structure
        logging.debug(f"Polymarket API response: {json.dumps(polymarket_data, indent=2)[:500]}...")
        
        # Process Polymarket data
        for market in polymarket_data:
            name = market.get('question', 'Unknown Market')
            price = market.get('probability', 0) * 100  # Convert to percentage
            products.append({"name": name, "price": price, "source": "Polymarket"})
        logging.info(f"Collected {len(polymarket_data)} products from Polymarket")
    except Exception as e:
        logging.error(f"Error with Polymarket API: {str(e)}")

    logging.info(f"Total products collected: {len(products)}")
    return json.dumps(products)

# Agent 2: Product Identifier
def product_identifier(data):
    try:
        products = json.loads(data)
        unified_products = {}
        
        for product in products:
            name = product['name']
            price = product['price']
            
            # Skip invalid prices
            if not isinstance(price, (int, float)):
                logging.warning(f"Invalid price for {name}: {price}")
                continue
            
            if name not in unified_products:
                unified_products[name] = {"prices": [], "sources": []}
            
            unified_products[name]["prices"].append(price)
            unified_products[name]["sources"].append(product['source'])
        
        logging.info(f"Identified {len(unified_products)} unique products")
        return json.dumps(unified_products)
    except Exception as e:
        logging.error(f"Error in product identification: {str(e)}")
        return json.dumps({})

# Agent 3: Data Organizer
def data_organizer(data):
    try:
        unified_products = json.loads(data)
        rows = []
        
        # Create a dictionary to track products and their details
        product_details = {}
        
        for name, details in unified_products.items():
            # Only consider products that appear in all three sources
            if len(details["sources"]) == 3:  # Check if the product is from all three sources
                prices = details["prices"]
                sources = details["sources"]
                
                # Initialize prices for each source
                kalshi_price = None
                manifold_price = None
                polymarket_price = None
                
                # Assign prices based on the source
                for i, source in enumerate(sources):
                    if source == "Kalshi":
                     kalshi_price = prices[i]
                    elif source == "Manifold":
                        manifold_price = prices[i]
                    elif source == "Polymarket":
                        polymarket_price = prices[i]
                
                # Calculate confidence level
                total_sources = 3  # Number of websites you’re scraping
                confidence = (len(sources) / total_sources) * 100

                # Append the product details to rows
                rows.append({
                    "Product": name, 
                    "Kalshi Price": kalshi_price, 
                    "Manifold Price": manifold_price,
                    "Polymarket Price": polymarket_price,
                    "Total Sources": total_sources,  
                    "Confidence Level": round(confidence, 2)  # e.g., 100.0
                })
        
        if rows:
            df = pd.DataFrame(rows)
            df.to_csv('unified_products.csv', index=False)
            logging.info(f"Saved {len(rows)} common products to unified_products.csv")
            print(df.head())  # Show sample output
        else:
            logging.warning("No common products to save to CSV")
    except Exception as e:
        logging.error(f"Error in data organization: {str(e)}")

# Main flow
if __name__ == "__main__":
    logging.info("Starting data collection...")
    raw_data = data_collector()  # Collect data from APIs
    
    logging.info("Starting product identification...")
    unified_data = product_identifier(raw_data)  # Identify products
    
    logging.info("Starting data organization...")
    data_organizer(unified_data)  # Organize data into CSV
    
    logging.info("Process completed")
 # type: ignore