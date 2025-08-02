# Foundation Project: Google Drive Clone

## ✅ Features Implemented
- Upload a file (stored in AWS S3)
- List all uploaded files
- Delete a file from both frontend and S3
- File metadata stored in a local SQLite database
- Hosted on an EC2 instance with public access
- Dockerized deployment (runs in a container on EC2)

---

## 🚀 Deployment Details
- The application is deployed on an **AWS EC2 instance**
- **Public URL (Frontend):** [http://13.203.232.114/](http://13.203.232.114/)
- Dockerized and running in a container

---

## 🧱 Tech Stack
- **Frontend:** React
- **Backend:** Python (Flask)
- **Database:** SQLite (local DB storing metadata)
- **Cloud Storage:** AWS S3
- **Infrastructure:** AWS EC2
- **Containerization:** Docker

---

## 📹 Demo

[🎥 Click to watch the screen recording on YouTube](https://youtu.be/-U4GnAXGRdc)

The demo showcases:
- Uploading a file
- Listing all uploaded files
- Deleting a file
- Verifying uploads in the S3 bucket
- EC2 instance running the containerized service

---

## 📸 Screenshots (also committed to this repo)
- ✅ Uploading file from the UI
- ✅ Files listed in the frontend
- ✅ Deleting a file
- ✅ AWS S3 bucket showing stored file
- ✅ EC2 instance terminal showing container running

---

## 📝 How to Run Locally (Optional)
```bash
git clone https://github.com/your-username/gdclone.git
cd gdclone
docker build -t gdclone .
docker run -p 5000:5000 gdclone
