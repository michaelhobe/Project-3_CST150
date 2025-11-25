# Shopping Website - CST150 Project 3

A Flask-based e-commerce website with shopping cart functionality, deployed on Vercel with PostgreSQL database.

## Features

- 📦 Product catalog with categories (E-books, Courses, Software)
- 🛒 Shopping cart with localStorage persistence
- 💳 Checkout system with order processing
- 📊 Admin dashboard for order management
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- ☁️ Deployed on Vercel with automatic database integration

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** Vercel Postgres (PostgreSQL)
- **ORM:** SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel
- **Version Control:** Git/GitHub

## Project Structure

```
shopping_website/
├── app.py                  # Main Flask application
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── products.json          # Sample products data
├── static/
│   ├── css/
│   │   └── style.css      # Styles
│   └── js/
│       ├── cart.js        # Shopping cart logic
│       ├── main.js        # Main JavaScript
│       └── products.js    # Product display logic
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Product catalog
    ├── cart.html          # Shopping cart page
    ├── vercel_checkout.html  # Checkout page
    ├── confirmation.html  # Order confirmation
    └── admin.html         # Admin dashboard
```

## Database Schema

### Products Table
- `id` (Integer, Primary Key)
- `name` (String, 255)
- `description` (Text)
- `cost_price` (Float)
- `sell_price` (Float)
- `category` (String, 100)
- `created_at` (DateTime)

### Orders Table
- `id` (Integer, Primary Key)
- `customer_email` (String, 255)
- `customer_phone` (String, 20)
- `customer_suburb` (String, 100)
- `total_amount` (Float)
- `order_date` (DateTime)
- `status` (String, 20)

### Order Items Table
- `id` (Integer, Primary Key)
- `order_id` (Foreign Key → orders.id)
- `product_id` (Foreign Key → products.id)
- `product_name` (String, 255)
- `quantity` (Integer)
- `price_at_purchase` (Float)

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/Project-3_CST150.git
cd Project-3_CST150/shopping_website
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Open browser:**
```
http://localhost:5000
```

**Note:** For local development, the app automatically uses SQLite database (no setup required). The database and sample products are created automatically on first run.

## Vercel Deployment Guide

### Step-by-Step Browser Instructions

#### Part 1: Push to GitHub

1. **Open Command Prompt/Terminal** in your project directory
2. **Add all files:**
```bash
git add .
```
3. **Commit changes:**
```bash
git commit -m "Convert to Vercel Postgres database"
```
4. **Push to GitHub:**
```bash
git push origin main
```

#### Part 2: Deploy to Vercel (Browser Steps)

1. **Go to Vercel:**
   - Open browser → Navigate to `https://vercel.com`
   - Sign in with your GitHub account

2. **Import Repository:**
   - Click **"Add New..."** button (top right)
   - Select **"Project"**
   - Find your repository: `Project-3_CST150`
   - Click **"Import"**

3. **Configure Project:**
   - Project Name: Leave as default or customize
   - Framework Preset: Leave as "Other"
   - Root Directory: `shopping_website` (if you have multiple projects in repo)
   - Build Settings: Leave as default

4. **Add Database (CRITICAL STEP):**
   - **Before clicking Deploy**, scroll down to find **"Storage"** section
   - Click **"Create"** button
   - Select **"Postgres"** from database options
   - Database Name: `shopping-website-db` (or your choice)
   - Region: Choose closest to your users
   - Click **"Create"**
   
   ✨ **Vercel automatically adds environment variables:**
   - `POSTGRES_URL`
   - `POSTGRES_PRISMA_URL`
   - `POSTGRES_URL_NON_POOLING`
   - And other connection details
   
   **YOU DON'T NEED TO COPY ANYTHING MANUALLY!**

5. **Deploy:**
   - Click **"Deploy"** button
   - Wait 2-3 minutes for build to complete
   - Your site will be live at: `your-project-name.vercel.app`

#### Part 3: Verify Deployment

1. **Visit your site:**
   - Click the provided URL
   - You should see all 10 products (3 ebooks, 3 courses, 4 software)

2. **Test functionality:**
   - Add items to cart
   - Go to checkout
   - Complete an order
   - Check admin page to see the order

3. **View database (optional):**
   - Go to Vercel dashboard
   - Click your project
   - Click **"Storage"** tab
   - Click your Postgres database
   - Click **"Data"** tab
   - Browse tables: `products`, `orders`, `order_items`

### First Run Automatic Setup

When your app runs for the first time on Vercel:
- ✅ Automatically creates all database tables
- ✅ Automatically seeds 10 sample products from `products.json`
- ✅ Ready to use immediately!

## Environment Variables

### Production (Vercel)
**Automatically configured** when you add Postgres database through Vercel dashboard. No manual setup required!

### Local Development
Create a `.env` file (optional - app uses SQLite by default):
```env
# Use SQLite (default, no setup needed)
DATABASE_URL=sqlite:///shopping.db

# OR use local PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## API Endpoints

- `GET /` - Product catalog homepage
- `GET /cart` - Shopping cart page
- `GET /checkout` - Checkout page
- `POST /checkout` - Process order
- `GET /confirmation` - Order confirmation
- `GET /admin` - Admin dashboard
- `GET /api/products` - JSON list of all products
- `GET /api/orders/<id>` - JSON details of specific order
- `GET /health` - Health check endpoint

## Troubleshooting

### Database Not Creating Tables
1. Go to Vercel dashboard → Your project
2. Click **"Storage"** tab
3. Verify Postgres database is connected
4. Go to **"Settings"** → **"Environment Variables"**
5. Verify `POSTGRES_URL` exists
6. Redeploy if needed: **"Deployments"** → **"..."** → **"Redeploy"**

### Products Not Showing
- Check Vercel deployment logs for errors
- Verify `products.json` file exists in repository
- Check database seeding logs in deployment console

### Orders Not Saving
- Verify database connection in deployment logs
- Check Postgres database status in Vercel dashboard
- Ensure `POSTGRES_URL` environment variable is set

### Local Development Issues
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)
- Try deleting `shopping.db` file and restart app

## Features Walkthrough

### Shopping Cart System
- Cart data stored in browser localStorage
- Persists across page refreshes
- Add/remove items with quantity control
- Real-time total calculation

### Checkout Process
1. User fills out email, phone, suburb
2. Cart data sent as JSON to backend
3. Flask creates Order and OrderItem records
4. Order ID returned for confirmation page

### Admin Dashboard
- View all orders with details
- See customer information
- Track order items and totals
- Orders sorted by date (newest first)

## Future Enhancements

- [ ] User authentication system
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Product search and filtering
- [ ] Email notifications for orders
- [ ] Inventory management
- [ ] Order status updates
- [ ] Product images upload
- [ ] Reviews and ratings

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

This project is created for educational purposes as part of CST150 coursework.

## Contact

For questions or issues, please open an issue on GitHub.

---

**Happy Shopping! 🛍️**
