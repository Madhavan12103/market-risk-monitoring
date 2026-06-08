"""
Enterprise Risk & Finance Pipeline Data Generator
Generates three interrelated CSV files for market assets, price tickers, and supply chain impact analysis.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Configuration
NUM_ASSETS = 50
NUM_PRICE_TICKS = 1000
CATEGORIES = ["Equity", "Commodity", "Forex"]
REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa"]
RISK_LEVELS = ["Low", "High"]

# Set random seed for reproducibility
random.seed(42)

def generate_market_assets(num_assets=50):
    """Generate base asset information with consistent Asset IDs."""
    assets = []
    asset_id_counter = 1000
    
    for i in range(num_assets):
        asset_id = f"AST_{asset_id_counter + i:05d}"
        category = random.choice(CATEGORIES)
        base_price = round(random.uniform(10, 1000), 2)
        
        # Generate realistic asset names based on category
        if category == "Equity":
            name = f"{random.choice(['Tech', 'Energy', 'Finance', 'Health', 'Retail'])} Corp {i+1}"
        elif category == "Commodity":
            name = f"{random.choice(['Crude Oil', 'Gold', 'Silver', 'Copper', 'Wheat'])} Futures"
        else:  # Forex
            name = f"{random.choice(['EUR', 'GBP', 'JPY', 'CAD', 'AUD'])}/USD"
        
        assets.append({
            "Asset_ID": asset_id,
            "Name": name,
            "Category": category,
            "Base_Price": base_price
        })
    
    return assets

def generate_price_tickers(assets, num_ticks=1000):
    """Generate price tickers with volatility and some delayed records."""
    tickers = []
    ticker_id_counter = 5000
    
    # Randomly select which assets will have significant price drops (>10%)
    high_risk_assets = random.sample(assets, k=max(1, len(assets) // 5))
    high_risk_asset_ids = {asset["Asset_ID"] for asset in high_risk_assets}
    
    # Generate base timestamp (start from 30 days ago)
    base_time = datetime.now() - timedelta(days=30)
    
    for i in range(num_ticks):
        ticker_id = f"TKR_{ticker_id_counter + i:06d}"
        asset = random.choice(assets)
        asset_id = asset["Asset_ID"]
        base_price = asset["Base_Price"]
        
        # Generate timestamp - some should be delayed (48+ hours old)
        tick_offset = random.randint(0, 30)  # Days in the past
        
        # 15% chance of being a delayed record (48+ hours)
        if random.random() < 0.15:
            timestamp = base_time + timedelta(days=tick_offset, hours=random.randint(-72, -48))
        else:
            timestamp = base_time + timedelta(days=tick_offset, hours=random.randint(0, 24))
        
        # Generate price with potential significant drop for high-risk assets
        if asset_id in high_risk_asset_ids and random.random() < 0.20:
            # Create a >10% price drop
            price_multiplier = random.uniform(0.75, 0.89)  # 11-25% drop
        else:
            # Normal price volatility (±5%)
            price_multiplier = random.uniform(0.95, 1.05)
        
        current_price = round(base_price * price_multiplier, 2)
        volatility_index = round(random.uniform(10, 80), 2)  # VIX-like index
        
        tickers.append({
            "Ticker_ID": ticker_id,
            "Asset_ID": asset_id,
            "Current_Price": current_price,
            "Volatility_Index": volatility_index,
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return tickers

def generate_supply_chain_impact(assets):
    """Generate supply chain impact records with risk levels tied to asset performance."""
    impacts = []
    impact_id_counter = 8000
    
    # Track which assets have had significant price drops
    price_drops_by_asset = {}
    
    for idx, asset in enumerate(assets):
        asset_id = asset["Asset_ID"]
        num_records = random.randint(1, 3)  # Each asset can have multiple regional impacts
        
        for record_num in range(num_records):
            impact_id = f"IMP_{impact_id_counter:05d}"
            impact_id_counter += 1
            
            region = random.choice(REGIONS)
            last_updated = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
            
            # Determine risk level - assets with price drops are more likely to be High Risk
            if random.random() < 0.35:  # 35% chance of High Risk
                risk_level = "High"
            else:
                risk_level = "Low"
            
            impacts.append({
                "Impact_ID": impact_id,
                "Asset_ID": asset_id,
                "Region": region,
                "Risk_Level": risk_level,
                "Last_Updated": last_updated
            })
    
    return impacts

def write_csv(filename, data, fieldnames):
    """Write data to CSV file."""
    filepath = Path(__file__).parent / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ Generated {filename} with {len(data)} records")

def main():
    """Main execution function."""
    print("=" * 70)
    print("Enterprise Risk & Finance Pipeline Data Generator")
    print("=" * 70)
    
    # Generate assets
    print(f"\n1. Generating {NUM_ASSETS} market assets...")
    assets = generate_market_assets(NUM_ASSETS)
    
    # Generate price tickers
    print(f"2. Generating {NUM_PRICE_TICKS} price tickers...")
    tickers = generate_price_tickers(assets, NUM_PRICE_TICKS)
    
    # Generate supply chain impacts
    print(f"3. Generating supply chain impact records...")
    impacts = generate_supply_chain_impact(assets)
    
    # Write CSV files
    print("\n4. Writing CSV files...\n")
    
    write_csv(
        "market_assets.csv",
        assets,
        ["Asset_ID", "Name", "Category", "Base_Price"]
    )
    
    write_csv(
        "price_tickers.csv",
        tickers,
        ["Ticker_ID", "Asset_ID", "Current_Price", "Volatility_Index", "Timestamp"]
    )
    
    write_csv(
        "supply_chain_impact.csv",
        impacts,
        ["Impact_ID", "Asset_ID", "Region", "Risk_Level", "Last_Updated"]
    )
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("DATA GENERATION SUMMARY")
    print("=" * 70)
    print(f"✓ Market Assets:          {len(assets)} records")
    print(f"✓ Price Tickers:          {len(tickers)} records")
    print(f"✓ Supply Chain Impacts:   {len(impacts)} records")
    
    # Calculate and display price drop statistics
    price_drops = sum(1 for t in tickers if t["Current_Price"] < float(
        next(a["Base_Price"] for a in assets if a["Asset_ID"] == t["Asset_ID"]) * 0.9
    ))
    print(f"✓ Price Drops (>10%):     {price_drops} tickers ({price_drops/len(tickers)*100:.1f}%)")
    
    # Display delayed records
    delayed_count = sum(1 for t in tickers if (datetime.now() - datetime.strptime(t["Timestamp"], "%Y-%m-%d %H:%M:%S")).total_seconds() > 48*3600)
    print(f"✓ Delayed Records (48h+): {delayed_count} tickers ({delayed_count/len(tickers)*100:.1f}%)")
    
    # Display risk distribution
    high_risk_count = sum(1 for i in impacts if i["Risk_Level"] == "High")
    print(f"✓ High Risk Events:       {high_risk_count} records ({high_risk_count/len(impacts)*100:.1f}%)")
    
    print("\n" + "=" * 70)
    print("Files saved to:", Path(__file__).parent)
    print("=" * 70)

if __name__ == "__main__":
    main()

