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

### Option 1: Alternative TTS Engines
Consider using:
- **Microsoft Azure Cognitive Services** - Supports Zulu (zu-ZA)
- **Amazon Polly** - May have better African language support
- **Local TTS engines** - Espeak or similar for offline capability

### Option 2: Pre-recorded Audio
- Record native speakers for common phrases
- Higher quality, authentic pronunciation
- Offline-capable
- More storage required

### Option 3: Hybrid Approach
- Use pre-recorded audio for common phrases
- TTS for dynamic/custom content
- Best of both worlds

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
