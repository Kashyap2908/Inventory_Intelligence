# Quick Switch Guide: Simulation ↔ AI

## 🎯 The One-Line Change

To switch from simulation to real AI, change just ONE line in your code!

---

## 📍 Location

**File:** `inventory/views.py`  
**Line:** ~760 (inside `trend_dashboard` function)

---

## 🔄 The Change

### Current (Simulation Mode) ✅
```python
new_score = calculate_trend_score(product)  # Uses simulation by default
```

### Switch to AI Mode 🤖
```python
new_score = calculate_trend_score(product, force_ai=True)  # Uses real AI
```

---

## ✏️ Step-by-Step Instructions

### Step 1: Get New API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy the key

**IMPORTANT:** Your current API key is disabled (reported as leaked). You MUST get a new one.

### Step 2: Update config.py
```python
# config.py
GOOGLE_API_KEY = "your-new-api-key-here"
```

### Step 3: Edit views.py
Open `inventory/views.py` and find line ~760:

**Before:**
```python
new_score = calculate_trend_score(product)
```

**After:**
```python
new_score = calculate_trend_score(product, force_ai=True)
```

### Step 4: Save and Test
```bash
python manage.py runserver
```

Visit the Trend Dashboard - it will now use real AI!

---

## 🔍 How to Verify It's Working

### Check Console Output

**Simulation Mode shows:**
```
🔄 Auto-updating trend scores on page load...
============================================================
🔍 CALCULATING TREND SCORE FOR: Basmati Rice 5kg
============================================================
✅ Auto-updated 53 products on page load
```

**AI Mode shows:**
```
🔄 Auto-updating trend scores on page load...
============================================================
🔍 CALCULATING TREND SCORE FOR: Basmati Rice 5kg
============================================================
🔑 Found API key in config.py
🤖 Configuring Google Gemini AI
✅ AI SCORE: 6.5
💡 Reasoning: High demand for rice products...
✅ Auto-updated 53 products on page load
```

---

## ⚡ Quick Reference

| Mode | Code | Speed | API Usage |
|------|------|-------|-----------|
| **Simulation** | `calculate_trend_score(product)` | Instant | None |
| **AI** | `calculate_trend_score(product, force_ai=True)` | 1-2s per product | Yes |

---

## 🎛️ Advanced: Hybrid Mode

Use AI only for important products to save API quota:

```python
for product in products:
    old_score = product.trend_score
    
    # Use AI for high-value products, simulation for others
    if product.total_stock > 100 or product.trend_score >= 7:
        new_score = calculate_trend_score(product, force_ai=True)  # AI
    else:
        new_score = calculate_trend_score(product)  # Simulation
    
    if abs(old_score - new_score) > 0.1:
        product.trend_score = new_score
        product.last_trend_update = timezone.now()
        product.save(update_fields=['trend_score', 'last_trend_update'])
        updated_count += 1
```

---

## 🔙 Switch Back to Simulation

Just remove `force_ai=True`:

```python
new_score = calculate_trend_score(product)  # Back to simulation
```

---

## ❓ FAQ

### Q: Should I change the other 3 places where trend scores are updated?
**A: NO** - Keep them as simulation:
- Line ~521: Stock entry (fast user action)
- Line ~585: Billing (customer checkout)  
- Line ~1562: Order approval (admin action)

These need to be instant. Only change the trend dashboard.

### Q: Why use simulation by default?
**A:** 
- ✅ Fast (instant vs 1-2 seconds per product)
- ✅ Reliable (no API failures)
- ✅ No quota limits
- ✅ Works offline
- ✅ Perfect for project submission

### Q: When should I use AI mode?
**A:** Only when:
- Demonstrating to faculty
- Need real market analysis
- Have valid API key with quota

---

## � API Quota Impact

### Simulation Only (Recommended)
```
Trend Dashboard:    0 API calls
Stock/Billing:      0 API calls
TOTAL:              0 API calls/day ✅
```

### AI for Dashboard Only
```
Trend Dashboard:    55 API calls (once per page load)
Stock/Billing:      0 API calls
TOTAL:              55 API calls/day ✅
```

### AI Everywhere (NOT Recommended)
```
Trend Dashboard:    55 API calls
Stock/Billing:      60+ API calls
TOTAL:              115+ API calls/day ❌
```

---

## 📝 Summary

**To use real AI:**
1. ✅ Get new API key from https://makersuite.google.com/app/apikey
2. ✅ Update `config.py` with new key
3. ✅ Add `force_ai=True` to line ~760 in `views.py`
4. ✅ Restart server

**That's it!** One parameter change switches the entire system from simulation to real AI.

---

## 🎓 For Project Submission

**Recommendation:** Keep simulation mode because:
- Faculty can test without API key
- No network dependency
- Fast and reliable
- Produces realistic varied scores (3.0-9.0)
- No quota limits

Switch to AI mode only for live demonstration if needed!
