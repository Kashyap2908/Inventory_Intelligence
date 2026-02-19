"""
AI-Powered Trend Score Calculator using Google Gemini
Updated for 2026: Using google.genai with JSON structured output
"""

import time
import os
import json
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
import random

# Try to import new Google Gemini SDK
try:
    from google import genai
    from pydantic import BaseModel
    NEW_SDK_AVAILABLE = True
except ImportError:
    NEW_SDK_AVAILABLE = False
    print("⚠️ New google.genai SDK not available, will use fallback")


# Define exactly what the AI should return
class TrendResponse(BaseModel):
    score: float
    reasoning: str


def calculate_trend_score(product):
    """
    Calculate trend score using Google Gemini AI with JSON output
    Falls back to intelligent simulation if AI unavailable
    Returns: 0-10 scale
    """
    
    print(f"\n{'='*60}")
    print(f"🔍 CALCULATING TREND SCORE FOR: {product.name}")
    print(f"{'='*60}")
    
    # Try Google Gemini AI first
    if NEW_SDK_AVAILABLE:
        try:
            # Retrieve API Key (try multiple sources)
            GOOGLE_API_KEY = None
            
            # Method 1: Try config.py
            try:
                from config import GOOGLE_API_KEY as CONFIG_KEY
                GOOGLE_API_KEY = CONFIG_KEY
                print(f"🔑 Found API key in config.py: {GOOGLE_API_KEY[:20]}...")
            except ImportError:
                pass
            
            # Method 2: Try environment variable
            if not GOOGLE_API_KEY:
                GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
                if GOOGLE_API_KEY:
                    print(f"🔑 Found API key in environment")
            
            if not GOOGLE_API_KEY or len(GOOGLE_API_KEY) < 30:
                raise ValueError("Invalid or missing API Key")
            
            # Step 1: Use the NEW Client
            print("🤖 Configuring Google Gemini AI (new SDK)...")
            client = genai.Client(api_key=GOOGLE_API_KEY)
            print("   ✅ Client configured successfully")
            
            # Get current context
            current_month = timezone.now().strftime('%B')
            current_season = get_season()
            
            # Create detailed prompt
            prompt = f"""Analyze the market trend for this product:
Product: {product.name}
Category: {product.category}
Current Stock: {product.total_stock} units
Month: {current_month}
Season: {current_season}

Provide a trend score from 0-10 where:
- 9-10 = Extremely high demand
- 7-8.9 = High demand  
- 5-6.9 = Moderate demand
- 3-4.9 = Low demand
- 0-2.9 = Very low demand

Return your analysis with a score and brief reasoning."""
            
            print(f"💬 Sending prompt to AI (JSON Mode)...")
            
            # Step 2: High-Resolution Timing
            start_time = time.perf_counter()
            
            # Step 3: Request JSON Output with structured schema
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Use stable 1.5 model
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': TrendResponse,
                }
            )
            
            end_time = time.perf_counter()
            
            # Step 4: Extract Data Safely
            result = response.parsed
            latency = end_time - start_time
            
            # Display metrics
            try:
                token_count = response.usage_metadata.total_token_count
                print(f"⏱️ Timing: {latency:.2f}s | 📊 Tokens: {token_count}")
            except:
                print(f"⏱️ Timing: {latency:.2f}s")
            
            print(f"✅ AI SCORE: {result.score}")
            print(f"💡 Reasoning: {result.reasoning[:100]}...")
            print(f"{'='*60}\n")
            
            # Ensure score is in valid range
            trend_score = min(10.0, max(0.0, float(result.score)))
            return round(trend_score, 1)
            
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"❌ AI Error ({error_type}): {error_msg}")
            
            # Check for specific error types
            if "quota" in error_msg.lower() or "429" in error_msg:
                print("💡 API quota exceeded - using simulation")
            elif "api key" in error_msg.lower() or "401" in error_msg:
                print("💡 API key issue - check config.py")
            elif "model" in error_msg.lower() or "404" in error_msg:
                print("💡 Model not found - check model name")
            else:
                print(f"💡 Unexpected error - using simulation")
            
            print(f"🔄 Falling back to simulation...")
    else:
        print("⚠️ New SDK not available, using simulation...")
    
    # Fallback to intelligent market simulation
    print(f"\n🔄 FALLING BACK TO SIMULATION for {product.name}")
    print(f"{'='*60}\n")
    return calculate_simulated_trend_score(product)


def calculate_simulated_trend_score(product):
    """
    Intelligent market simulation when AI is unavailable
    Creates realistic scores based on product characteristics
    """
    
    # Base score from category popularity
    category_scores = {
        'Electronics': 7.5,
        'Food': 6.8,
        'Beverages': 7.2,
        'Snacks': 7.8,
        'Personal Care': 6.5,
        'Household': 5.8,
        'Stationery': 5.2,
        'Clothing': 6.9,
        'Toys': 6.0,
        'Health': 7.0,
        'Beauty': 7.3,
        'Sports': 6.4,
        'Books': 5.5,
        'Furniture': 5.0,
    }
    
    base_score = category_scores.get(product.category, 5.5)
    
    # Seasonal adjustments
    seasonal_bonus = get_seasonal_bonus(product)
    base_score += seasonal_bonus
    
    # Stock level adjustments
    stock_adjustment = get_stock_adjustment(product)
    base_score += stock_adjustment
    
    # Time-based variation for realism
    time_variation = random.uniform(-0.5, 0.5)
    base_score += time_variation
    
    # Add small random factor for variety
    random_factor = random.uniform(-0.3, 0.3)
    base_score += random_factor
    
    # Ensure score is between 0 and 10
    base_score = max(0.0, min(10.0, base_score))
    
    return round(base_score, 1)


def get_season():
    """Get current season"""
    month = timezone.now().month
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:
        return "Winter"


def get_seasonal_bonus(product):
    """
    Add seasonal bonus based on current month
    Returns: -1.0 to +2.0 adjustment
    """
    current_month = timezone.now().month
    category = product.category.lower()
    
    # Summer products (May-August)
    if current_month in [5, 6, 7, 8]:
        if any(word in category for word in ['beverage', 'drink', 'cold', 'ice', 'water', 'juice']):
            return 2.0
        elif any(word in category for word in ['snack', 'food']):
            return 1.0
    
    # Winter products (November-February)
    elif current_month in [11, 12, 1, 2]:
        if any(word in category for word in ['hot', 'warm', 'clothing', 'heater', 'blanket']):
            return 2.0
        elif any(word in category for word in ['food', 'snack']):
            return 0.8
    
    # Festival season (October-November)
    elif current_month in [10, 11]:
        if any(word in category for word in ['snack', 'sweet', 'gift', 'decoration', 'clothing']):
            return 1.5
    
    # Back to school (June-July)
    elif current_month in [6, 7]:
        if any(word in category for word in ['stationery', 'book', 'bag', 'electronics']):
            return 1.2
    
    return 0.0


def get_stock_adjustment(product):
    """
    Adjust score based on stock levels
    Returns: -1.0 to +1.0 adjustment
    """
    total_stock = product.total_stock
    
    # Low stock suggests high demand
    if total_stock < 20:
        return 1.0
    elif total_stock < 50:
        return 0.5
    # High stock suggests lower demand
    elif total_stock > 200:
        return -0.8
    elif total_stock > 150:
        return -0.5
    else:
        return 0.0


def update_all_trend_scores():
    """
    Update trend scores for all products using AI
    Call this periodically (e.g., daily via cron job)
    """
    from inventory.models import Product
    
    print("🚀 Starting AI-powered trend score update for all products...")
    
    updated_count = 0
    for product in Product.objects.all():
        old_score = product.trend_score
        new_score = calculate_trend_score(product)
        
        if abs(old_score - new_score) > 0.1:  # Only update if significant change
            product.trend_score = new_score
            product.last_trend_update = timezone.now()
            product.save()
            updated_count += 1
            print(f"   Updated {product.name}: {old_score} → {new_score}")
    
    print(f"✅ Completed! Updated {updated_count} products")
    return updated_count


def update_product_trend_score(product):
    """
    Update trend score for a single product using AI
    Call this when product activity happens
    """
    print(f"🔄 Updating trend score for {product.name}...")
    new_score = calculate_trend_score(product)
    product.trend_score = new_score
    product.last_trend_update = timezone.now()
    product.save()
    print(f"   ✅ Updated to {new_score}")
    return new_score


def batch_update_with_ai(products, max_products=None):
    """
    Batch update multiple products with AI
    Includes rate limiting to avoid API quota issues
    """
    import time
    
    if max_products:
        products = products[:max_products]
    
    updated_count = 0
    for product in products:
        try:
            new_score = calculate_trend_score(product)
            product.trend_score = new_score
            product.last_trend_update = timezone.now()
            product.save()
            updated_count += 1
            
            # Rate limiting - wait 1 second between AI calls
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error updating {product.name}: {e}")
            continue
    
    return updated_count
