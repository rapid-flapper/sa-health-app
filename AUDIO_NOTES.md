# Audio Playback - Technical Notes

## Current Implementation

Audio generation uses Google Text-to-Speech (gTTS) library for converting text to speech.

## Language Support Status

| Language | Code | gTTS Support | Status |
|----------|------|--------------|--------|
| English | en | ✅ Full support | Native TTS |
| Afrikaans | af | ✅ Full support | Native TTS |
| Zulu (isiZulu) | zu | ❌ Not supported | English TTS fallback |
| Xhosa (isiXhosa) | xh | ❌ Not supported | English TTS fallback |
| Sepedi | nso | ❌ Not supported | English TTS fallback |

## Current Behavior

### Supported Languages (English, Afrikaans)
- Audio is generated with native pronunciation
- Accurate, natural-sounding speech
- Proper accent and intonation

### Unsupported Languages (Zulu, Xhosa, Sepedi)
- **Current**: Audio is generated using English TTS engine
- **Result**: Text is read with English phonetics (not ideal but functional)
- **User Impact**: Audio won't sound perfectly natural, but text is still pronounced
- **Benefit**: Users can still hear phonetic approximation

## Why This Limitation?

Google Text-to-Speech (gTTS), while supporting 100+ languages, does not yet include:
- isiZulu (Zulu)
- isiXhosa (Xhosa)  
- Sesotho sa Leboa (Sepedi)

These are South African languages with relatively smaller TTS training data availability.

## Future Improvements (Phase 2/3)

### Option 1: TTS-Optimized Respelling ⚠️ TESTED - LIMITED VALUE

**Concept**: Use special respelling format designed for TTS engines.

**Implementation:**
```python
# Original approach
text = "Sawubona, unjani namhlanje?"  # Zulu text
tts = gTTS(text=text, lang='en')       # English TTS (sounds bad)

# TTS-optimized respelling (current)
text = "sah-woo-boh-nah, oon-jah-nee nahm-lahn-jeh"  # All lowercase
tts = gTTS(text=text, lang='en')       # English TTS reads respelling
```

**Test Results: ⚠️ MARGINAL IMPROVEMENT**

**Testing Timeline:**
- **Test 1** (Oct 16, 2025 @ 5:11pm): With capital emphasis letters → ❌ **FAILED**
  - Capital letters spelled individually: "BOH" → "B-O-H"
  - Unusable
  
- **Test 2** (Oct 16, 2025 @ 5:28pm): All lowercase → ⚠️ **MARGINAL**
  - No letter spelling (capitals removed)
  - Still not great quality
  - Slightly better than native text, but not significantly

**Key Findings:**
1. ❌ **ANY capital letters** = Letter-by-letter spelling (even one!)
2. ⚠️ **All lowercase respelling** = Marginal improvement only
3. ⚠️ **Hyphens okay** but don't help much
4. ❌ **Not worth the effort** for small improvement
5. ✅ **Placeholder until human recordings** available

**Current Status: IMPLEMENTED BUT LIMITED**
- Currently in use for Zulu, Xhosa, Sepedi (first 3 phrases)
- All lowercase respellings in `tts_pronunciation` field
- Backend uses it when available
- Better than nothing, but not ideal
- **Real solution: Human recordings**

**Lesson Learned**: 
- Google TTS treats ALL capitals as acronyms/initialisms
- Respelling helps slightly but not enough for professional use
- Phonetic guides are for human reading, not TTS
- Professional TTS quality requires native language support or human audio

### Option 2: Alternative TTS Engines
Consider using:
- **Microsoft Azure Cognitive Services** - Supports Zulu (zu-ZA)
- **Amazon Polly** - May have better African language support
- **Local TTS engines** - Espeak or similar for offline capability

### Option 3: Pre-recorded Human Audio (Best Quality)
Add native speaker recordings for authentic pronunciation.

**Step-by-step Guide for Adding Human Recordings:**

#### Step 1: Prepare Audio Files
1. **Record native speakers** saying each phrase
2. **File naming convention**: `{phrase_id}_{language}.mp3`
   - Example: `phrase_001_zu.mp3`, `phrase_002_xh.mp3`
3. **Audio specifications**:
   - Format: MP3 or OGG
   - Bitrate: 64-128 kbps (good quality, small size)
   - Sample rate: 22050 Hz or 44100 Hz
   - Mono audio (saves space)
4. **File location**: Store in `app/static/audio/` directory
   ```
   app/static/audio/
   ├── phrase_001_zu.mp3
   ├── phrase_001_xh.mp3
   ├── phrase_002_zu.mp3
   └── ...
   ```

#### Step 2: Update Backend (app.py)
Modify the audio generation endpoint to check for human recordings first:

```python
import os

@app.route('/api/audio/<phrase_id>/<language>')
def generate_audio(phrase_id, language):
    """Generate or serve audio for a specific phrase"""
    try:
        # Check for pre-recorded human audio first
        audio_filename = f'{phrase_id}_{language}.mp3'
        audio_path = os.path.join(app.static_folder, 'audio', audio_filename)
        
        if os.path.exists(audio_path):
            # Serve pre-recorded human audio
            return send_file(
                audio_path,
                mimetype='audio/mp3',
                as_attachment=False
            )
        
        # Fallback to TTS generation (existing code)
        data = load_phrases_data()
        phrase = next((p for p in data['phrases'] if p['id'] == phrase_id), None)
        
        if not phrase:
            return jsonify({'success': False, 'error': 'Phrase not found'}), 404
        
        if language not in phrase['translations']:
            return jsonify({'success': False, 'error': f'Language {language} not available'}), 404
        
        text = phrase['translations'][language]['text']
        gtts_lang = gtts_language_map.get(language, 'en')
        
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return send_file(audio_buffer, mimetype='audio/mp3', as_attachment=False)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

#### Step 3: Update Frontend Indicator (app.html)
Update the quality detection to recognize human recordings:

```javascript
// In getAudioQuality() function
async function getAudioQuality(phraseId, language) {
    // Check if human recording exists
    // Option A: Make a HEAD request to check file existence
    try {
        const response = await fetch(`/api/audio/${phraseId}/${language}`, {method: 'HEAD'});
        if (response.headers.get('X-Audio-Source') === 'human') {
            return {type: 'human', label: '🎙️ Human Recording', ...};
        }
    } catch {}
    
    // Option B: Maintain a list of phrases with human recordings
    const humanRecordings = {
        'zu': ['phrase_001', 'phrase_002'],  // Update as you add recordings
        'xh': ['phrase_001'],
        'nso': []
    };
    
    if (humanRecordings[language]?.includes(phraseId)) {
        return {type: 'human', label: '🎙️ Human Recording', ...};
    }
    
    // Fall back to TTS detection
    // ... existing code
}
```

Or simpler approach - add metadata to phrases.json:
```json
{
  "id": "phrase_001",
  "has_human_audio": ["zu", "xh"],  // List languages with human recordings
  "translations": {...}
}
```

#### Step 4: Testing
1. Add one test recording (e.g., `phrase_001_zu.mp3`)
2. Visit app, play that phrase
3. Should see blue "🎙️ Human Recording" badge
4. Audio should play from file, not gTTS
5. Verify quality and file size

#### Step 5: Gradual Rollout
- Start with top 10-20 most-used phrases
- Focus on critical categories (Emergencies, Greetings)
- Gather user feedback on which phrases need human audio most
- Expand over time

**Storage Estimates:**
- Average MP3: ~50-100 KB per phrase
- 100 phrases × 3 languages × 75 KB = ~22 MB total
- Reasonable for web app

### Option 4: Hybrid Approach (Recommended)
- **Human recordings** for top 50-100 common phrases (best quality)
- **Phonetic TTS** for remaining Zulu/Xhosa/Sepedi (improved quality)
- **Native TTS** for English/Afrikaans (already good)
- **Standard TTS** for any future languages
- Best balance of quality, cost, and coverage

## Recommendation

For Phase 1 MVP:
- ✅ Current implementation is acceptable
- ✅ English/Afrikaans work perfectly
- ✅ Zulu/Xhosa/Sepedi still provide value (phonetic reading)
- ✅ Users have phonetic guides as primary pronunciation aid

For Phase 2:
- Explore Microsoft Azure TTS (has Zulu support)
- Consider pre-recorded audio for top 50 phrases
- Gather user feedback on priority

## User Communication

### Audio Quality Indicators

The app displays visual badges to inform users about audio quality:

**🟢 Native TTS (Green Badge)**
- Languages: English, Afrikaans
- Quality: Good - Natural pronunciation
- Description: "Good Quality - Natural Pronunciation"

**🟡 Approximation (Yellow Badge)**
- Languages: Zulu, Xhosa, Sepedi
- Quality: Limited - Uses English TTS
- Description: "Limited Quality - Uses English TTS (Phonetic guide recommended)"

**🎙️ Human Recording (Blue Badge)** *(Future)*
- Quality: Best - Native speaker audio
- Description: "Best Quality - Native Speaker"
- Status: Not yet implemented (placeholder for Phase 2)

### User Guidance

When users play audio for Zulu, Xhosa, or Sepedi:
1. They will see a **yellow "🟡 Approximation" badge**
2. Hovering shows: "Limited Quality - Uses English TTS (Phonetic guide recommended)"
3. The phonetic pronunciation guide remains the primary learning tool
4. Audio serves as a helpful supplement but not perfectly native for these languages
5. Users should focus on reading the phonetic guide while listening

## Technical Details

### Implementation
```python
gtts_language_map = {
    'en': 'en',     # English - supported
    'af': 'af',     # Afrikaans - supported
    'zu': 'en',     # Zulu - fallback to English
    'xh': 'en',     # Xhosa - fallback to English
    'nso': 'en'     # Sepedi - fallback to English
}
```

### Future: Azure TTS Example
```python
# Microsoft Azure supports Zulu
# Locale: zu-ZA (Zulu - South Africa)
speech_config = speechsdk.SpeechConfig(subscription, region)
speech_config.speech_synthesis_voice_name = "zu-ZA-ThandoNeural"
```

---

*Last Updated: October 16, 2025*  
*Milestone 5: Audio Playback*
