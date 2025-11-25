# 🚀 Vercel Deployment Checklist

Follow these steps in order to deploy your shopping website to Vercel with PostgreSQL.

## ✅ Pre-Deployment Checklist

- [x] Database-enabled `app.py` created
- [x] `models.py` with Product, Order, OrderItem models
- [x] `requirements.txt` with all dependencies
- [x] `vercel.json` configuration file
- [x] `.gitignore` file (excludes .env, __pycache__, etc.)
- [x] `products.json` with sample data
- [x] All templates updated for database flow

## 📋 Step-by-Step Deployment

### Step 1: Local Testing (Optional but Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (uses SQLite)
python app.py

# Open browser to http://localhost:5000
# Verify products load and cart works
```

### Step 2: Push to GitHub

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Convert to Vercel Postgres database"

# Push to GitHub
git push origin main
```

### Step 3: Deploy to Vercel (Browser)

1. **Open Vercel:**
   - Go to https://vercel.com
   - Sign in with GitHub

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Select your repository: `Project-3_CST150`
   - Click "Import"

3. **Configure (if needed):**
   - Root Directory: `shopping_website` (if in subdirectory)
   - Framework: Leave as "Other"
   - Build Settings: Leave as default

4. **Add Database (CRITICAL!):**
   - ⚠️ **BEFORE DEPLOYING**: Scroll to "Storage" section
   - Click "Create" → Select "Postgres"
   - Name: `shopping-website-db`
   - Click "Create"
   - ✨ Environment variables added automatically!

5. **Deploy:**
   - Click "Deploy" button
   - Wait 2-3 minutes
   - Click the URL to visit your site

### Step 4: Verify Deployment

- [ ] Site loads at vercel.app URL
- [ ] Products page shows 10 products
- [ ] Can add items to cart
- [ ] Cart persists across page refreshes
- [ ] Checkout form works
- [ ] Order confirmation shows
- [ ] Admin page displays orders
- [ ] Database tables created automatically

## 🔍 Troubleshooting

### Products Not Showing
1. Check Vercel deployment logs
2. Verify `products.json` in repository
3. Check function logs for database errors

### Database Connection Issues
1. Vercel Dashboard → Your Project
2. Click "Storage" → Verify Postgres connected
3. Click "Settings" → "Environment Variables"
4. Verify `POSTGRES_URL` exists
5. Try redeploying

### Build Failures
1. Check deployment logs in Vercel
2. Verify `requirements.txt` is correct
3. Ensure `vercel.json` is valid JSON
4. Check Python version compatibility

## 📊 Post-Deployment

### View Database
1. Vercel Dashboard → Your Project
2. Click "Storage" tab
3. Click your Postgres database
4. Click "Data" tab
5. Browse: `products`, `orders`, `order_items` tables

### Monitor Application
1. Vercel Dashboard → Your Project
2. Click "Functions" to see API calls
3. Click "Logs" for error tracking
4. Check "Analytics" for usage stats

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ All 10 products display correctly
- ✅ Shopping cart functionality works
- ✅ Orders can be placed
- ✅ Admin dashboard shows orders
- ✅ No console errors in browser
- ✅ Database contains seeded products

## 🆘 Getting Help

If you encounter issues:
1. Check the full README.md for detailed troubleshooting
2. Review Vercel deployment logs
3. Verify all files are committed to GitHub
4. Ensure database was created before deployment

---

**Once completed, your site will be live at:** `your-project-name.vercel.app`

**🎉 Happy Deploying!**
