# Developer Guide: Adding Human Audio Recordings

This guide explains how to add pre-recorded human audio to replace or supplement synthetic TTS audio.

## Quick Start

**Goal**: Replace synthetic TTS audio with authentic native speaker recordings for better pronunciation quality.

**When to use**:
- Critical medical phrases (emergencies, consent, pain assessment)
- High-frequency phrases (greetings, common questions)
- Languages not supported by Google TTS (Zulu, Xhosa, Sepedi)

---

## Step-by-Step Implementation

### 1. Recording Preparation

#### Recording Requirements
- **Language**: Native speaker preferred
- **Environment**: Quiet room, minimal background noise
- **Tone**: Clear, professional, friendly but not overly casual
- **Speed**: Natural speaking pace (not too slow)
- **Equipment**: Any decent microphone (phone is acceptable)

#### Recording Script
For each phrase, record:
1. The phrase in the target language
2. Brief pause (0.5 seconds)
3. Optional: Record 2-3 takes, pick the best

#### File Specifications
- **Format**: MP3 (widely supported, good compression)
- **Alternative**: OGG (better compression, good browser support)
- **Bitrate**: 64-128 kbps (64 kbps sufficient for speech)
- **Sample Rate**: 22050 Hz (speech quality) or 44100 Hz (higher quality)
- **Channels**: Mono (saves 50% space vs stereo)
- **Duration**: Trim silence from beginning/end

#### Conversion Tools
```bash
# Using ffmpeg to convert and optimize
ffmpeg -i input.wav -b:a 64k -ar 22050 -ac 1 phrase_001_zu.mp3

# Batch convert all WAV files
for file in *.wav; do
    ffmpeg -i "$file" -b:a 64k -ar 22050 -ac 1 "${file%.wav}.mp3"
done
```

### 2. File Organization

#### Naming Convention
**Format**: `{phrase_id}_{language_code}.mp3`

**Examples**:
```
phrase_001_zu.mp3   # Phrase 1 in Zulu
phrase_001_xh.mp3   # Phrase 1 in Xhosa
phrase_002_zu.mp3   # Phrase 2 in Zulu
phrase_010_nso.mp3  # Phrase 10 in Sepedi
```

**Why this format?**
- Easy to programmatically locate files
- Clear language identification
- Matches phrase IDs in phrases.json
- Sortable and searchable

#### Directory Structure
```
sa-health-app/
├── app/
│   └── static/
│       └── audio/              # Create this directory
│           ├── phrase_001_zu.mp3
│           ├── phrase_001_xh.mp3
│           ├── phrase_001_nso.mp3
│           ├── phrase_002_zu.mp3
│           └── ...
├── data/
│   └── phrases.json
└── app.py
```

**Create the directory**:
```bash
mkdir -p app/static/audio
```

### 3. Backend Implementation

#### Update app.py

**Current code** (generates TTS for all):
```python
@app.route('/api/audio/<phrase_id>/<language>')
def generate_audio(phrase_id, language):
    # ... existing TTS generation code
```

**Updated code** (checks for human audio first):
```python
import os

@app.route('/api/audio/<phrase_id>/<language>')
def generate_audio(phrase_id, language):
    """Generate or serve audio for a specific phrase"""
    try:
        # STEP 1: Check for pre-recorded human audio first
        audio_filename = f'{phrase_id}_{language}.mp3'
        audio_path = os.path.join(app.static_folder, 'audio', audio_filename)
        
        if os.path.exists(audio_path):
            # Serve pre-recorded human audio
            return send_file(
                audio_path,
                mimetype='audio/mp3',
                as_attachment=False,
                download_name=audio_filename
            )
        
        # STEP 2: Fallback to TTS generation (existing code)
        data = load_phrases_data()
        phrase = next((p for p in data['phrases'] if p['id'] == phrase_id), None)
        
        if not phrase:
            return jsonify({
                'success': False,
                'error': 'Phrase not found'
            }), 404
        
        if language not in phrase['translations']:
            return jsonify({
                'success': False,
                'error': f'Language {language} not available for this phrase'
            }), 404
        
        text = phrase['translations'][language]['text']
        
        # gTTS language mapping
        gtts_language_map = {
            'en': 'en',
            'af': 'af',
            'zu': 'en',
            'xh': 'en',
            'nso': 'en'
        }
        
        gtts_lang = gtts_language_map.get(language, 'en')
        
        # Generate audio using gTTS
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return send_file(
            audio_buffer,
            mimetype='audio/mp3',
            as_attachment=False,
            download_name=f'{phrase_id}_{language}.mp3'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

**What changed?**
1. Added file system check before TTS generation
2. If human recording exists → serve it
3. If not → generate with TTS (existing behavior)
4. No breaking changes - fully backward compatible

### 4. Frontend Updates (Optional but Recommended)

#### Option A: Automatic Detection (Simple)
The quality badge will automatically show correctly if you update the JavaScript array:

```javascript
// In app/templates/app.html - getAudioQuality() function
const humanRecordings = {
    'zu': ['phrase_001', 'phrase_002', 'phrase_003'],  // Add phrase IDs as you record
    'xh': ['phrase_001', 'phrase_002'],
    'nso': ['phrase_001']
};

if (humanRecordings[language]?.includes(phraseId)) {
    return {
        type: 'human',
        label: '🎙️ Human Recording',
        description: 'Best Quality - Native Speaker'
    };
}
```

#### Option B: Metadata in JSON (More Maintainable)
Add human audio indicator to phrases.json:

```json
{
  "id": "phrase_001",
  "categories": ["greeting", "introduction"],
  "has_human_audio": ["zu", "xh", "nso"],
  "translations": {
    "en": {...},
    "zu": {...}
  }
}
```

Then in JavaScript:
```javascript
function getAudioQuality(phrase, language) {
    if (phrase.has_human_audio?.includes(language)) {
        return {type: 'human', label: '🎙️ Human Recording', ...};
    }
    // ... rest of logic
}
```

### 5. Testing Workflow

#### Add One Test Recording
```bash
# 1. Record "Hello, how are you today?" in Zulu
# 2. Convert to MP3
ffmpeg -i recording.wav -b:a 64k -ar 22050 -ac 1 phrase_001_zu.mp3

# 3. Copy to audio directory
cp phrase_001_zu.mp3 app/static/audio/

# 4. Update frontend (if using Option A)
# Add 'phrase_001' to humanRecordings['zu'] array
```

#### Test in Browser
1. Run: `python app.py`
2. Visit: `http://localhost:5000/app`
3. Select "Patient's Language": Zulu
4. Find first phrase
5. Look for: **🎙️ Human Recording** badge (blue)
6. Click "Play Audio"
7. Should hear your recording (not synthetic TTS)

### 6. Gradual Rollout Strategy

#### Phase 2A: Emergency Phrases (Top Priority)
Record human audio for:
- Emergency category phrases
- Pain assessment phrases
- Critical consent phrases
- **Estimate**: 10-15 phrases × 3 languages = 30-45 recordings

#### Phase 2B: Common Phrases (High Impact)
- Greetings
- Basic instructions
- Symptom questions
- **Estimate**: 20-30 phrases × 3 languages = 60-90 recordings

#### Phase 2C: Complete Coverage (Optional)
- All remaining phrases
- **Estimate**: 100 phrases × 3 languages = 300 recordings

#### Prioritization Criteria
1. **Frequency of use** - Most commonly used phrases first
2. **Criticality** - Emergency/consent phrases prioritized
3. **TTS quality gap** - Phrases where TTS sounds worst
4. **User feedback** - What users request most

### 7. Quality Assurance

#### Recording Checklist
- [ ] Native speaker or verified fluent speaker
- [ ] Clear pronunciation (not too fast, not too slow)
- [ ] No background noise
- [ ] Professional but friendly tone
- [ ] Matches written text exactly
- [ ] File size <100 KB (preferably 50-75 KB)

#### Testing Checklist
- [ ] File plays in browser
- [ ] Badge shows "🎙️ Human Recording"
- [ ] Audio quality is clear
- [ ] No clipping or distortion
- [ ] Volume level is consistent with TTS audio
- [ ] Works on mobile devices

### 8. Storage & Performance

#### Storage Calculation
```
Average file size: 75 KB per phrase
100 phrases × 3 languages = 300 files
300 files × 75 KB = 22.5 MB total

Acceptable for:
✅ Web hosting (negligible)
✅ Mobile data (users download only what they need)
✅ Offline PWA (Phase 3)
```

#### Performance Impact
- **Human audio**: Instant playback (served from disk)
- **TTS audio**: 1-3 second generation delay
- **Result**: Human audio actually FASTER than TTS!

### 9. Maintenance

#### Adding New Recordings
```bash
# 1. Record new phrase
# 2. Name file correctly
phrase_025_zu.mp3

# 3. Copy to audio directory  
cp phrase_025_zu.mp3 app/static/audio/

# 4. Update frontend array (Option A) or phrases.json (Option B)
# 5. Commit to git
git add app/static/audio/phrase_025_zu.mp3
git commit -m "Add human audio: phrase 25 in Zulu"
git push
```

#### Updating Existing Recordings
- Better recording available? Just replace the file
- Same filename = automatic update
- No code changes needed

### 10. Alternative: Phonetic TTS Workaround

**Quick improvement without recordings**: Use phonetic text instead of native text for TTS.

```python
# In app.py - generate_audio function
if language in ['zu', 'xh', 'nso']:
    # Use phonetic guide for better English TTS pronunciation
    text = phrase['translations'][language]['phonetic']
else:
    text = phrase['translations'][language]['text']
```

**Example**:
- Native text: "Sawubona, unjani namhlanje?"
- Phonetic text: "sah-woo-BOH-nah, oon-JAH-nee nahm-HLAHN-jeh"
- English TTS reads phonetic → May sound closer to actual pronunciation

**Test this first** before investing in recordings - might be good enough!

---

## Summary

1. ✅ **Record** native speakers (MP3, 64kbps, mono)
2. ✅ **Name** files as `{phrase_id}_{language}.mp3`
3. ✅ **Place** in `app/static/audio/` directory
4. ✅ **Update** backend (already handles automatically with provided code)
5. ✅ **Update** frontend quality detection (update array or JSON)
6. ✅ **Test** in browser
7. ✅ **Deploy** and gather user feedback

**Result**: Users see blue "🎙️ Human Recording" badge and hear authentic native speaker pronunciation!

---

*Last Updated: October 16, 2025*  
*For questions: Refer to AUDIO_NOTES.md for technical details*
