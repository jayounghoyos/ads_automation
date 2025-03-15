# Ads automation with Tweepy

# Description
This project automates job postings on various social media platforms, such as X (Twitter), Meta and Snapchat, using the Django framework. It allows users to upload a CSV file containing job offers, which are then processed and published automatically via APIs. The automation is powered by Tweepy for seamless social media integration.

# How to Run It
1. **Clone the repository**  
   ```sh
   git clone https://https://github.com/jayounghoyos/ads_automation.git
   cd ads-automation
2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
4. **Set up the environment variables**
   * Create a **.env** file and configure API keys for Twitter (X), Meta, and Django settings.
5. **Run database migratiions**
    ```sh
    python manage.py migrate
6. **Start the Django server**
    ```sh
    python manage.py runserver
# Documentation
* **Framework:** Django
* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, Django
* **Database:** SQLite / PostgreSQL
* **APIs:** Tweepy (Twitter API), Meta API
* **CSV Handling:** Pandas

# Description
# File Structure
# CSV Structure


# Most important functions

# Notes  
This project is under constant updates.  
New features will be added for enhanced automation.
