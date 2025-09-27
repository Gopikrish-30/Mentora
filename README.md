# Mentora - The AI Course Creator

![Hackathon Winner](https://img.shields.io/badge/Code_O'_Clock-3rd_Place_Winner-success)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> **Mentora** is an AI-powered platform designed to revolutionize corporate training by transforming course creation from a process that takes weeks into one that takes minutes.

[cite_start]This project was developed by the team **Strawhats** for the **Code O'Clock 24-Hour National Level Hackathon**, where it proudly secured 3rd place. [cite: 3, 5]

---

## 🎯 The Problem

[cite_start]In corporate training, course creation is slow, rigid, and disconnected from learners needs. [cite: 9] Trainers spend weeks writing objectives, splitting content into lessons, preparing slides, designing quizzes, and recording videos. [cite_start]By the time the course is complete, learners have often moved ahead, leaving the material outdated and irrelevant. [cite: 10] [cite_start]Moreover, the lack of reusability makes the process repetitive and inefficient, while the final courses frequently fail to connect with real-world job requirements. [cite: 11]

## ✨ Our Solution

[cite_start]We propose an AI-powered course creation system that enables users to generate fully customized learning experiences from diverse content inputs such as text, PDFs, and videos. [cite: 14] [cite_start]The system analyzes the uploaded material and automatically designs a tailored course, while giving users complete control over personalization. [cite: 15]

## 🚀 Key Features

* [cite_start]**Flexible Content Formats:** Choose between micro-lessons, short videos, PPTs or PDFs. [cite: 17]
* [cite_start]**Continuous Assessments:** Add quizzes that are essential for the user to test their skills. [cite: 18]
* [cite_start]**Multilingual Support:** Generate courses in multiple languages for global accessibility. [cite: 19]
* **AI-Monitored Quizzes:** An innovative feature to ensure learner engagement and assessment integrity.
* [cite_start]**Interactive Chatbot (Future Scope):** Enhance learner engagement with conversational support. [cite: 20]

## 📸 Screenshots

Here is a look at the Mentora prototype in action.

| Step 1: Describe Course | Step 2: Upload Content | Step 4: View Outcome |
| :---: | :---: | :---: |
| ![Step 1](assets/image_ce3a7d.png) | ![Step 2](assets/image_ce3af4.png) | ![Step 4](assets/image_ce3b19.png) |

## 🛠️ Technical Architecture

Mentora is powered by a modern, multi-stage AI pipeline to deliver high-quality, relevant content.

![Architecture Diagram](assets/tech_diagram.png)

* [cite_start]**Text Extraction:** We use **PyMuPDF** and **BeautifulSoup** to parse and extract text from PDFs and websites. [cite: 22]
* [cite_start]**Orchestration Framework:** The entire workflow is managed and orchestrated by **LangChain**. [cite: 22]
* [cite_start]**Vector Storage:** Content is processed, chunked, and stored in **ChromaDB** for efficient retrieval. [cite: 22]
* [cite_start]**Generative Core:** Course generation is handled by API calls to powerful Large Language Models, including **Google's Gemini API** and the **GROK API**. [cite: 22]

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

## 👥 The Team (Strawhats)

* [cite_start]**Vidhun KS** [cite: 6]
* [cite_start]**Loganand S** [cite: 6]
* [cite_start]**Thilak L** [cite: 6]
* [cite_start]**Gopi M** [cite: 6]

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.