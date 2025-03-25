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

# CSV Structure

## Job Postings CSV Format  

This project utilizes a structured CSV file to store job vacancy information. The file consists of various fields that define each job posting, including details about the **position, company, location, qualifications, and contact information**.

### **CSV Fields Description**  

| Column Name         | Description |
|---------------------|-------------|
| **Job Id**         | Unique identifier for the job posting. |
| **Experience**     | Required years of experience (e.g., "2 to 12 Years"). |
| **Qualifications** | Required educational qualifications (e.g., "BCA", "M.Tech"). |
| **Salary Range**   | Expected salary range (e.g., "$56K-$116K"). |
| **Location**       | City where the job is based. |
| **Country**        | Country where the job is available. |
| **Latitude** / **Longitude** | Geographic coordinates of the job location. |
| **Work Type**      | Type of employment (e.g., "Intern", "Full-time"). |
| **Company Size**   | Number of employees in the company. |
| **Job Posting Date** | Date when the job was posted. |
| **Preference**     | Specific hiring preferences (e.g., "Female"). |
| **Contact Person** | Name of the person handling recruitment. |
| **Contact**        | Contact details (e.g., phone number). |
| **Job Title**      | Name of the job role (e.g., "Web Developer"). |
| **Role**           | Specific job role category (e.g., "Frontend Web Developer"). |
| **Job Portal**     | Platform where the job was originally posted. |
| **Job Description** | Brief description of the job responsibilities. |
| **Benefits**       | List of benefits offered (e.g., "Health Insurance, PTO"). |
| **Skills**         | Required technical and soft skills for the role. |
| **Responsibilities** | Key duties and tasks associated with the position. |
| **Company**        | Name of the company offering the job. |
| **Company Profile** | JSON-formatted profile of the company, including sector, industry, location, and CEO. |

# Most important functions


# Notes  
This project is under constant updates.  
New features will be added for enhanced automation.