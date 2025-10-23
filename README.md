# AI Text Detector & Humanizer Platform

Platform multibahasa yang sangat akurat untuk mendeteksi teks yang dihasilkan AI dan mengubahnya menjadi tulisan yang natural dan sesuai konteks.

## 🌟 Fitur Utama

### 🔍 AI Text Detector
- **Deteksi Multi-bahasa**: Mendukung 70+ bahasa dunia dengan akurasi tinggi
- **Multi-model Analysis**: Menggunakan berbagai model AI untuk hasil yang lebih akurat
- **Linguistic Feature Analysis**: Analisis mendalam terhadap pola linguistik
- **Real-time Detection**: Hasil deteksi instan dengan confidence score

### ✍️ Text Humanizer
- **6 Writing Styles**:
  - Academic: Formal, research-based dengan referensi
  - Business: Profesional, ringkas, berorientasi hasil
  - General: Netral, mudah dipahami, informatif
  - Email: Sopan, langsung, personal
  - Creative: Ekspresif, imajinatif, engaging
  - Casual: Santai, conversational, friendly

- **3 Target Audiences**:
  - General Public: Tanpa pengetahuan khusus
  - Knowledgeable: Pemahaman dasar topik
  - Expert: Keahlian mendalam

- **Web Context Integration**: Mengakses internet untuk informasi terkini
- **Adaptive Writing**: Menyesuaikan gaya penulisan dengan konteks

### 🔄 Combined Tool
- Deteksi dan humanisasi dalam satu langkah
- Efisien untuk workflow yang cepat

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone repository:
```bash
git clone <repository-url>
cd workspace
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

4. Set environment variables (optional untuk fitur lanjutan):
```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Running the Application

```bash
cd backend
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## 📖 API Documentation

### POST /api/detect
Deteksi apakah teks dihasilkan oleh AI.

**Request Body:**
```json
{
  "text": "Text to analyze",
  "language": "en"  // Optional, auto-detect if not provided
}
```

**Response:**
```json
{
  "is_ai_generated": true,
  "confidence": 0.85,
  "language": {"en": 0.99},
  "model_scores": {...},
  "explanation": [...]
}
```

### POST /api/humanize
Ubah teks menjadi lebih natural dan manusiawi.

**Request Body:**
```json
{
  "text": "Text to humanize",
  "scope": "general",
  "audience": "general",
  "language": "en",
  "use_web_context": true
}
```

**Response:**
```json
{
  "original_text": "...",
  "humanized_text": "...",
  "modifications": [...],
  "web_contexts": [...]
}
```

### POST /api/process
Kombinasi deteksi dan humanisasi.

**Request Body:**
```json
{
  "text": "Text to process",
  "scope": "general",
  "audience": "general",
  "language": "en"
}
```

## 🌍 Supported Languages

Platform ini mendukung 70+ bahasa termasuk:
- Bahasa major: English, 中文, Español, हिन्दी, العربية, Português, বাংলা, Русский, 日本語, Deutsch
- Bahasa Asia: Bahasa Indonesia, ไทย, Tiếng Việt, 한국어, தமிழ், తెలుగు, മലയാളം
- Bahasa Eropa: Français, Italiano, Polski, Nederlands, Svenska, Ελληνικά
- Dan banyak lagi...

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Models**: Transformers, NLTK, spaCy
- **Language Detection**: langdetect, pycld3
- **Web Scraping**: BeautifulSoup, Selenium
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS dengan desain modern dan responsive

## 📊 Features in Detail

### AI Detection Methods:
1. **Pre-trained Models**: Multiple state-of-the-art AI detection models
2. **Linguistic Analysis**: 
   - Vocabulary diversity
   - Sentence structure patterns
   - POS tag distribution
   - Readability scores
3. **Heuristic Scoring**: Custom algorithms based on AI writing patterns

### Humanization Techniques:
1. **Vocabulary Adjustment**: Sesuai dengan scope dan audience
2. **Natural Variations**: Menambah variasi alami dalam penulisan
3. **Tone Adaptation**: Menyesuaikan nada sesuai konteks
4. **Web Context Integration**: Informasi terkini dari internet
5. **AI Polish**: Optional enhancement dengan GPT-4/Claude

## 🔒 Privacy & Security

- Tidak ada data yang disimpan permanen
- Semua processing dilakukan secara real-time
- API keys disimpan sebagai environment variables
- HTTPS ready untuk deployment production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

Untuk pertanyaan atau masalah, silakan buka issue di repository ini.