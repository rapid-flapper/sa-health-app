# SA Health App

## Project Overview

A multilingual medical communication app designed for frontline healthcare workers in South Africa. This app addresses the challenge of language barriers in healthcare settings by providing common medical phrases in multiple South African languages, complete with pronunciation guides and audio playback.

## Purpose

South Africa's linguistic diversity presents communication challenges for healthcare workers who may encounter patients speaking unfamiliar languages. This app provides a practical tool to bridge these language gaps, enabling better patient care and communication.

## Target Users

- Frontline healthcare workers in South Africa
- Medical practitioners in multilingual healthcare settings
- Healthcare facilities serving diverse language communities

## Core Features

1. **Bilingual Display** ⭐ **NEW**
   - Side-by-side translation display
   - Healthcare worker selects "Your Language" (what you understand)
   - Healthcare worker selects "Patient's Language" (what patient speaks)
   - Both languages shown together for easy reference
   - Essential for effective medical communication

2. **Multilingual Medical Phrases**
   - Common healthcare phrases in multiple South African languages
   - Clear text display for each phrase
   - Organized by medical categories

3. **Pronunciation Support**
   - Phonetic/pronunciation guides for correct pronunciation
   - Shown for both source and target languages
   - Helps healthcare workers learn proper pronunciation

4. **Audio Playback**
   - Text-to-speech audio for each phrase
   - Audio plays in patient's language
   - Allows healthcare workers to hear native pronunciation
   - Play button for instant audio playback

5. **Mobile-Optimized Interface**
   - Designed for use on mobile devices
   - Quick access in healthcare settings
   - Touch-friendly interface
   - Responsive design adapts to screen size

## Language Support

### Phase 1 (Initial Launch)
- English
- Zulu (isiZulu)
- Xhosa (isiXhosa)
- Afrikaans
- Sepedi (Sesotho sa Leboa)

### Future Phases
Expand to include all 11 official South African languages:
- Setswana
- Sesotho
- Xitsonga
- siSwati
- Tshivenda
- isiNdebele

## Technical Stack

### Backend
- **Framework**: Flask (Python)
- **Audio**: gTTS (Google Text-to-Speech) for pronunciation
- **Data Storage**: JSON file format for phrases (easy to edit and maintain)

### Frontend
- **Design**: Mobile-first responsive web design
- **Technologies**: HTML5, CSS3, JavaScript
- **Approach**: Progressive Web App (PWA)

### Development Environment
- **Virtual Environment**: `health-venv`
- **Python Version**: 3.14.0

## Development Phases

### Phase 1: MVP (Minimum Viable Product)
**Goal**: Create a functional online web app with core features

**Features**:
- ✅ Flask backend setup
- ✅ Mobile-optimized responsive UI
- ✅ 5 initial languages (English, Zulu, Xhosa, Afrikaans, Sepedi)
- ✅ Text display of medical phrases
- ✅ Phonetic pronunciation guides
- ✅ Audio playback using TTS
- ✅ JSON-based phrase management
- ✅ Basic category organization (greetings, symptoms, instructions, etc.)

**Requirements**:
- Online connectivity required
- Works on mobile browsers
- Desktop browser compatible

### Phase 2: Enhanced Features
**Goal**: Add offline capability and advanced features

**Planned Features**:
- 🔄 Progressive Web App (PWA) implementation
- 🔄 Offline functionality (cached content)
- 🔄 Installable on phone home screen
- 🔄 Additional language support
- 🔄 Expanded phrase library
- 🔄 Basic keyword search functionality
- 🔄 Favorites/bookmarks
- 🔄 Usage tracking (optional)

### Phase 3: Intelligent Features (Future)
**Goal**: Add AI-powered phrase discovery and advanced intelligence

**Planned Features**:
- 🔄 Large Language Model (LLM) integration
- 🔄 Natural language query interface (e.g., "I need to ask about chest pain")
- 🔄 Context-aware phrase suggestions
- 🔄 Intelligent semantic search
- 🔄 Smart recommendations based on situation description
- 🔄 Privacy-conscious implementation (anonymized queries)

**Implementation Considerations**:
- Maintain category-based browsing as fallback
- Use as assistance tool, not for medical diagnosis
- Consider local open-source models for offline/privacy
- Build substantial phrase database first before LLM integration

## Development Progress

**Current Phase**: Phase 1 - MVP Development  
**Current Branch**: `dev`  
**Last Updated**: October 16, 2025

### Phase 1 Milestones

- [x] **Milestone 1: Project Foundation** ✅
  - [x] Install Flask and required dependencies
  - [x] Create project folder structure
  - [x] Create requirements.txt
  - [x] Verify virtual environment setup

- [x] **Milestone 2: Data Structure** ✅
  - [x] Design and create JSON schema for phrases
  - [x] Create initial phrases.json with sample data
  - [x] Include all 5 languages in sample phrases
  - [x] Add category metadata structure
  - [x] Test JSON loading in Python

- [x] **Milestone 3: Flask Backend** ✅
  - [x] Create basic Flask app structure
  - [x] Implement route for home page
  - [x] Implement API endpoint for phrases by category
  - [x] Implement API endpoint for all categories
  - [x] Test backend with sample data

- [x] **Milestone 4: Frontend UI** ✅
  - [x] Create mobile-first responsive layout
  - [x] Implement category filter/selector
  - [x] Display phrases with translations
  - [x] Add phonetic pronunciation display
  - [x] Style with modern, clean design
  - [x] Test on mobile viewport

- [ ] **Milestone 5: Audio Playback**
  - [ ] Install and configure gTTS library
  - [ ] Implement audio generation endpoint
  - [ ] Add play button to each phrase
  - [ ] Test audio playback across languages
  - [ ] Handle audio loading states

- [ ] **Milestone 6: Phase 1 Completion**
  - [ ] Full integration testing
  - [ ] Test on actual mobile device
  - [ ] Add more phrases across categories
  - [ ] Update documentation
  - [ ] Deploy for testing (optional)

### Completed Milestones

- [x] **Milestone 0: Project Setup** *(Merged to main)*
  - [x] Repository cloned
  - [x] Virtual environment created (health-venv)
  - [x] Git workflow established (main + dev branches)
  - [x] Comprehensive README created
  - [x] .gitignore configured
  - [x] Project memories established

---

**Note**: Milestones may be adjusted as development progresses. Each milestone completion on `dev` will be considered for merge to `main` branch.

## Project Structure

```
sa-health-app/
├── health-venv/           # Virtual environment (not in git)
├── app/                   # Flask application
│   ├── static/           # CSS, JS, audio files
│   ├── templates/        # HTML templates
│   └── routes.py         # Flask routes
├── data/                 # Phrase data
│   └── phrases.json      # Medical phrases database
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Setup Instructions

### Prerequisites
- Python 3.14.0 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rapid-flapper/sa-health-app.git
cd sa-health-app
```

2. Create and activate virtual environment:
```bash
python -m venv health-venv
.\health-venv\Scripts\Activate.ps1  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open browser and navigate to:
```
http://localhost:5000
```

## Design Decisions

### Why Flask?
- Lightweight and beginner-friendly
- Python-based (familiar for data scientists)
- Flexible and easy to extend
- Good documentation and community support

### Why JSON for Data Storage?
- Simple to edit manually
- No database complexity for MVP
- Easy to version control
- Sufficient for initial phrase volume
- Can migrate to database later if needed

### Why Text-to-Speech?
- No need for native speaker recordings initially
- Easy to generate audio automatically
- Scalable to multiple languages
- Can be upgraded to pre-recorded audio later

### Why Mobile-First?
- Healthcare workers are often on the move
- Mobile phones are ubiquitous in healthcare settings
- Quick access is critical in patient interactions
- PWA allows installation like a native app

## Contributing

This is a personal project in active development. Contributions, suggestions, and feedback are welcome!

## License

[To be determined]

## Contact

[To be added]

---

**Status**: Phase 1 Development
**Last Updated**: October 16, 2025
