# 📺 youtube_QA

A Streamlit app for extracting transcripts from YouTube videos and performing Q&A on them using Gemini API.

---

## 🚀 Features

- Download audio from YouTube without scraping transcript directly  
- Presents transcripts with timestamps  
- Enables question-answering on video content  
- Streamlit web interface for interactive use

---

## 📋 Table of Contents

1. [Installation](#installation)  
2. [Screenshots](#screenshots)  

---

## 🔧 Installation

```bash
git clone https://github.com/ArchanSureja/youtube_QA.git
cd youtube_QA

# create virtual environment and activate it.
python3 -m venv venv && source venv/bin/activate

pip install -r requirements.txt

#before starting create a .env file and put your gemini key
GEMINI_API_KEY = <Your_API_KEY>

#Start Streamlit app
streamlit run streamlit_app.py

```
## Screenshots : 
![image](https://github.com/user-attachments/assets/ede5fbd4-ace2-4a04-b857-8162e3ed6fd2)
![image](https://github.com/user-attachments/assets/c50dd9fd-2efe-417c-b1da-27097a5be342)



