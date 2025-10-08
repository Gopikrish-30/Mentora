# Mentora - The AI Course Creator

![Hackathon Winner](https://img.shields.io/badge/Code_O'_Clock-3rd_Place_Winner-success)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> **Mentora** is an AI-powered platform designed to revolutionize corporate training by transforming course creation from a process that takes weeks into one that takes minutes.

This project was developed by the team **Strawhats** for the **Code O'Clock 24-Hour National Level Hackathon**, where it proudly secured 3rd place. 

---

## 🎯 The Problem

In corporate training, course creation is slow, rigid, and disconnected from learners needs. Trainers spend weeks writing objectives, splitting content into lessons, preparing slides, designing quizzes, and recording videos. By the time the course is complete, learners have often moved ahead, leaving the material outdated and irrelevant. Moreover, the lack of reusability makes the process repetitive and inefficient, while the final courses frequently fail to connect with real-world job requirements.

## ✨ Our Solution

We propose an AI-powered course creation system that enables users to generate fully customized learning experiences from diverse content inputs such as text, PDFs, and videos. The system analyzes the uploaded material and automatically designs a tailored course, while giving users complete control over personalization. 

## 🚀 Key Features

**Flexible Content Formats:** Choose between micro-lessons, short videos, PPTs or PDFs. 
**Continuous Assessments:** Add quizzes that are essential for the user to test their skills.
**Multilingual Support:** Generate courses in multiple languages for global accessibility.
**AI-Monitored Quizzes:** An innovative feature to ensure learner engagement and assessment integrity.
**Interactive Chatbot (Future Scope):** Enhance learner engagement with conversational support.

## 📸 Screenshots

Here is a look at the Mentora prototype in action.

| Step 1: Describe Course |
| :---: |
<img width="680" height="680" alt="Screenshot 2025-10-08 at 9 11 29 PM" src="https://github.com/user-attachments/assets/e21782ea-cf48-43ec-8352-d0fd54c0ba4f" />

| Course With Quiz |
| :---: |
<img width="680" height="680" alt="Screenshot 2025-10-08 at 9 15 38 PM" src="https://github.com/user-attachments/assets/8eff22ba-f774-421f-8040-600cfbc46313" />


| Trainer Review |
| :---: |
<img width="680" height="680" alt="Screenshot 2025-10-08 at 9 15 56 PM" src="https://github.com/user-attachments/assets/e43100d3-3993-472e-8d2b-a86e52109bdc" />


## 🛠️ Technical Architecture

Mentora is powered by a modern, multi-stage AI pipeline to deliver high-quality, relevant content.

**Architecture Diagram**
<img width="680" height="680" alt="Flow1 drawio-1" src="https://github.com/user-attachments/assets/9b90e4ab-c1f4-42b1-b647-bc3ceeef0fa9" />



**Text Extraction:** We use **PyMuPDF** and **BeautifulSoup** to parse and extract text from PDFs and websites. [cite: 22]
**Orchestration Framework:** The entire workflow is managed and orchestrated by **LangChain**. [cite: 22]
**Vector Storage:** Content is processed, chunked, and stored in **ChromaDB** for efficient retrieval. [cite: 22]
**Generative Core:** Course generation is handled by API calls to powerful Large Language Models, including **Google's Gemini API** and the **GROK API**.

## ⚙️ Getting Started

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/thilak0105/Code-O-Clock.git](https://github.com/thilak0105/Code-O-Clock.git)
cd Code-O-Clock
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
*(Note: You need to create a `requirements.txt` file first by running `pip freeze > requirements.txt`)*
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:**
Create a file named `.env` in the root directory and add your API keys:
```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
GROK_API_KEY="YOUR_GROK_API_KEY"
```

**5. Run the application:**
```bash
python app.py
```

**6. Run the frontend in other Terminal:**
```
npm start
```

##  The Team (Strawhats)

- **Gopi M** - [GitHub Profile](https://github.com/Gopikrish-30)
- **Thilak L** - [GitHub Profile](https://github.com/thilak0105)
- **Vidhun KS** - [GitHub Profile](https://github.com/doraemon-21)
- **Loganand S** - [GitHub Profile](https://github.com/loganand612)



## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
