# Vercel Blob Storage Setup Guide

## What We've Done

✅ Added `vercel-blob` package to requirements.txt
✅ Added `image_url` field to Product model
✅ Updated app.py to support image URLs
✅ Updated templates to display product images
✅ Added CSS styling for product images

## How to Set Up Vercel Blob Storage

### Step 1: Add Blob Storage to Vercel Project

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Click on your project: `P3_cst150`

2. **Add Blob Storage**
   - Click **"Storage"** tab
   - Click **"Create Database"** or **"Connect Store"**
   - Select **"Blob"**
   - Name: `product-images`
   - Click **"Create"**

3. **Environment Variables Added Automatically**
   - Vercel automatically adds `BLOB_READ_WRITE_TOKEN`
   - This allows your app to upload/read images

### Step 2: Deploy Your Code

Run `deploy.bat` or manually:

```bash
cd shopping_website
git add .
git commit -m "Add Blob storage support"
git push origin main
```

### Step 3: Upload Product Images

You have two options:

#### Option A: Use Vercel Dashboard (Easiest)

1. Go to Storage → Blob → product-images
2. Click "Upload"
3. Upload your product images
4. Copy the blob URLs (like: `https://blob.vercel-storage.com/xyz123.jpg`)

#### Option B: Programmatic Upload (Advanced)

Create a simple upload script:

```python
from vercel_blob import upload
import os

# Upload an image
with open('laptop.jpg', 'rb') as f:
    blob = upload('laptop.jpg', f, token=os.environ['BLOB_READ_WRITE_TOKEN'])
    print(f"Uploaded: {blob['url']}")
```

### Step 4: Update Your Database

Once you have blob URLs, update your products:

**Option 1: Via SQL (in Vercel Dashboard)**

Go to your Neon database → Query editor:

```sql
UPDATE products 
SET image_url = 'https://blob.vercel-storage.com/laptop.jpg' 
WHERE id = 1;

UPDATE products 
SET image_url = 'https://blob.vercel-storage.com/ebook.jpg' 
WHERE id = 2;
```

**Option 2: Via products.json (for fresh init)**

Edit `products.json` and add `image_url` field:

```json
{
  "id": 1,
  "name": "Python Programming Guide",
  "description": "Complete guide to Python",
  "cost_price": 15.00,
  "sell_price": 29.99,
  "category": "ebooks",
  "image_url": "https://blob.vercel-storage.com/python-book.jpg"
}
```

Then clear the database and re-initialize.

## Using Placeholder Images (For Testing)

If you don't have images yet, you can use placeholder URLs:

```json
"image_url": "https://placehold.co/400x300/0066cc/white?text=E-Book"
"image_url": "https://placehold.co/400x300/00cc66/white?text=Course"
"image_url": "https://placehold.co/400x300/cc6600/white?text=Software"
```

## Alternative: Static Images (Simpler for School Project)

If Blob storage feels like overkill:

1. Put images in `static/images/products/`
2. In database, store just the filename: `"laptop.jpg"`
3. Update template to use: 
   ```html
   <img src="/static/images/products/{{ product.image_url }}">
   ```

This is simpler and works great for fixed products!

## Testing

After setup:
1. Visit your site
2. You should see product images (if URLs are set)
3. If no image URL, products display normally (no image shown)

## Troubleshooting

**Images not showing?**
- Check blob URLs are correct in database
- Verify `BLOB_READ_WRITE_TOKEN` is set in Vercel
- Check browser console for errors

**Want to add upload functionality?**
- Create an admin upload form
- Use `vercel_blob.upload()` to handle uploads
- Store returned URL in database

## Benefits of Blob Storage

✅ Scalable (handles many images)
✅ CDN delivery (fast loading)
✅ Simple pricing (pay for what you use)
✅ Professional approach
✅ Easy to manage via dashboard

## Free Tier Limits

- 1 GB storage
- 10 GB bandwidth/month
- Perfect for school projects!

---

Need help? The code is ready - just set up Blob storage in Vercel and add your image URLs!
