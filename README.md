# MVP-of-Advertising-Dashboard

📝 Project Description
This Flask-based web application allows users to create and manage digital advertising campaigns with AI-powered ad copy generation. The dashboard includes user authentication, campaign creation tools, and performance analytics.

🤖 AI Integration
The application leverages OpenAI's API to automatically generate compelling ad copy:

AI-Powered Ad Generation:

Automatically creates engaging ad text based on campaign parameters

Uses GPT-3.5-turbo model for high-quality copy

Incorporates targeting information (interests, demographics) into prompts

Smart Fallback System:

Uses template-based fallback when API is unavailable

Provides graceful degradation if API limits are reached

Prompt Engineering:

python
prompt = f"Create a 1-2 sentence engaging ad for {product_name} targeting {keywords}."
Dynamically incorporates campaign details

Optimized for marketing effectiveness

🚀 Features
User authentication system

Campaign creation with targeting options

Image uploads for campaign banners

AI-generated ad copy

Simulated performance analytics

Responsive dashboard interface

🛠️ Technical Stack
Backend: Python/Flask

Frontend: HTML, Bootstrap

Database: In-memory storage (for demo)

AI: OpenAI API (GPT-3.5-turbo)

Authentication: Flask-Login

⚙️ Setup Instructions
Clone repository:

bash
git clone https://github.com/yourusername/advertising-dashboard.git
cd advertising-dashboard
Set up environment:

bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure .env file:

env
SECRET_KEY=your_secret_key
AI_API_KEY=your_openai_api_key
Run application:

bash
python app.py
📊 Example AI Usage
When creating a campaign for "Summer Sale" targeting "Travel, Fashion", the AI might generate:

"Get ready for your summer adventures! Enjoy 30% off stylish travel essentials perfect for your next getaway."

📁 Project Structure
.
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── static/                # Static files
│   └── uploads/           # Uploaded images
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── dashboard.html     # Campaign list
│   ├── create_campaign.html
│   └── view_campaign.html
└── README.md              # This file
🌟 Future Enhancements
Add real analytics integration

Implement A/B testing for AI-generated copy

Add multi-user support

Expand targeting options

📜 License
MIT License - Free for personal and commercial use
