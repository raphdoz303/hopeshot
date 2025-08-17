# ⚙️ HopeShot Setup Guide

**Complete guide to get HopeShot running on your machine**

---

## 📋 **Prerequisites**
- **Python 3.11+** *(tested with 3.13.7)*
- **Node.js 18+** *(for Next.js)*
- **Git** *(for version control)*

---

## 🚀 **Installation Steps**

### **1️⃣ Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/hopeshot.git
cd hopeshot
```

### **2️⃣ Backend Setup** *(Python/FastAPI)*
```bash
cd backend

# Install Python dependencies
py -m pip install -r requirements.txt

# Start development server
py -m uvicorn main:app --reload --port 8000
```

🎯 **Backend will be available at**: `http://localhost:8000`

### **3️⃣ Frontend Setup** *(Next.js/React)*
```bash
# From project root
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

🎯 **Frontend will be available at**: `http://localhost:3000`

---

## ✅ **Verification Steps**

### **🔧 Test Backend**
Visit these URLs in your browser:
- 🏠 `http://localhost:8000/` - *Root endpoint*
- 🧪 `http://localhost:8000/api/test` - *Test endpoint*

### **🎨 Test Frontend**
- 🏠 `http://localhost:3000/` - *Homepage*
- 🧪 `http://localhost:3000/test` - *API testing interface*

### **🔄 Test Full-Stack Communication**
1. ✅ Ensure both servers are running
2. 🌐 Visit `http://localhost:3000/test`
3. 🖱️ Click the API test buttons
4. 📄 Verify JSON responses appear

---

## 💻 **Development Workflow**

### **🏁 Starting Development Session**
```bash
# Terminal 1: Backend
cd backend
py -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### **📝 Making Changes**
1. **Edit** code files
2. **Auto-reload** - servers automatically restart *(hot reload enabled)*
3. **Test** changes in browser
4. **Commit** when feature is complete

---

## 🛠️ **Troubleshooting**

### **⚠️ Common Issues**

**🐍 Python/pip not found**:
- Use `py` instead of `python`
- Use `py -m pip` instead of `pip`

**📦 Package installation errors**:
- Update `requirements.txt` to use `>=` instead of `==` for version flexibility

**🌐 CORS errors in browser**:
- Ensure backend CORS middleware allows `http://localhost:3000`
- Check that both servers are running

**🚪 Port conflicts**:
- **Backend**: Change `--port 8000` to another port
- **Frontend**: Next.js will auto-suggest alternative ports

### **🆘 Getting Help**
- 🔍 Check browser developer console for frontend errors
- 📺 Check terminal output for backend errors  
- 🧪 Use the test page at `/test` to isolate API issues

---

## 📁 **Project Structure**
```
hopeshot/
├── 📄 .env.example      # Environment variables template
├── 📖 README.md         # Project overview
├── 🐍 backend/          # FastAPI application
│   ├── main.py         # Main application file
│   └── requirements.txt
├── ⚛️  frontend/         # Next.js application
│   ├── src/            # Source code
│   └── package.json
└── 📚 docs/             # Documentation
```

---

*🔧 Last updated: **August 17, 2024*** | *⚡ Ready to build something amazing!*