# Testing Guide - AI Text Platform

## 🧪 Quick Test

### 1. Test AI Detection

**Bahasa Indonesia:**
```
POST http://localhost:5000/api/detect
Content-Type: application/json

{
  "text": "Artificial Intelligence (AI) adalah teknologi yang memungkinkan mesin untuk belajar dari pengalaman, menyesuaikan diri dengan input baru, dan melakukan tugas seperti manusia. Teknologi ini menggunakan algoritma pembelajaran mesin dan jaringan saraf untuk memproses data besar.",
  "language": "id"
}
```

**English:**
```
POST http://localhost:5000/api/detect
Content-Type: application/json

{
  "text": "The rapid advancement of artificial intelligence has revolutionized various industries. Machine learning algorithms can now process vast amounts of data with unprecedented accuracy, enabling applications ranging from autonomous vehicles to personalized healthcare solutions.",
  "language": "en"
}
```

### 2. Test Text Humanizer

**Academic Style:**
```
POST http://localhost:5000/api/humanize
Content-Type: application/json

{
  "text": "AI is changing how we work. It makes things faster and more efficient.",
  "scope": "academic",
  "audience": "expert",
  "language": "en"
}
```

**Casual Style:**
```
POST http://localhost:5000/api/humanize
Content-Type: application/json

{
  "text": "The utilization of artificial intelligence mechanisms facilitates the optimization of workflow processes.",
  "scope": "casual",
  "audience": "general",
  "language": "en"
}
```

### 3. Test Combined Tool

```
POST http://localhost:5000/api/process
Content-Type: application/json

{
  "text": "Machine learning models are trained on large datasets to recognize patterns and make predictions. This technology has applications in many fields including healthcare, finance, and transportation.",
  "scope": "business",
  "audience": "knowledgeable",
  "language": "en"
}
```

## 📝 Test Cases

### AI Detection Test Cases

1. **Clearly AI-generated text** (Expected: High AI probability)
   - Formal, consistent structure
   - Perfect grammar
   - Generic examples
   - Balanced sentence length

2. **Human-written text** (Expected: Low AI probability)
   - Colloquialisms
   - Minor grammatical errors
   - Personal anecdotes
   - Varied sentence structure

3. **Mixed content** (Expected: Medium probability)
   - Some AI-edited parts
   - Human additions
   - Mixed styles

### Humanizer Test Cases

1. **Academic → Casual conversion**
   - Input: Technical jargon
   - Output: Simple language

2. **Casual → Business conversion**
   - Input: Informal text
   - Output: Professional tone

3. **General → Expert conversion**
   - Input: Basic explanation
   - Output: Technical details

## 🌍 Multi-language Testing

Test dengan berbagai bahasa:

1. **Chinese (中文):**
```json
{
  "text": "人工智能正在改变我们的生活方式。它可以帮助我们更高效地完成任务。",
  "language": "zh"
}
```

2. **Spanish (Español):**
```json
{
  "text": "La inteligencia artificial está revolucionando la forma en que trabajamos y vivimos.",
  "language": "es"
}
```

3. **Arabic (العربية):**
```json
{
  "text": "الذكاء الاصطناعي يغير طريقة عملنا وحياتنا بشكل جذري.",
  "language": "ar"
}
```

## 🔧 Performance Testing

### Rate Limit Testing
- Detection API: 30 requests/minute
- Humanizer API: 20 requests/minute
- Combined API: 15 requests/minute

### Load Testing Script
```python
import requests
import concurrent.futures
import time

def test_api(endpoint, data):
    start = time.time()
    response = requests.post(f"http://localhost:5000{endpoint}", json=data)
    end = time.time()
    return {
        'status': response.status_code,
        'time': end - start
    }

# Run concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for i in range(50):
        future = executor.submit(test_api, '/api/detect', {
            'text': f'Test text number {i}',
            'language': 'en'
        })
        futures.append(future)
    
    results = [f.result() for f in futures]
    print(f"Average response time: {sum(r['time'] for r in results) / len(results):.2f}s")
```

## 🐛 Error Testing

### Invalid Input Tests

1. **Empty text:**
```json
{
  "text": "",
  "language": "en"
}
```
Expected: 400 Bad Request

2. **Invalid language:**
```json
{
  "text": "Test text",
  "language": "xyz"
}
```
Expected: 400 Bad Request

3. **Invalid scope:**
```json
{
  "text": "Test text",
  "scope": "invalid",
  "language": "en"
}
```
Expected: 400 Bad Request

## 🔍 Browser Testing

1. Open http://localhost:5000
2. Test each tab:
   - AI Detector
   - Text Humanizer
   - Combined Tool
3. Check responsive design on mobile
4. Test keyboard shortcuts:
   - Ctrl+Enter: Submit
   - 1, 2, 3: Switch tabs

## ✅ Checklist

- [ ] All API endpoints return correct responses
- [ ] Rate limiting works correctly
- [ ] Error messages are informative
- [ ] UI is responsive on all devices
- [ ] Multi-language detection works
- [ ] Text humanization produces natural output
- [ ] Web context integration works (if API keys provided)
- [ ] Character counting works in all textareas
- [ ] Copy button works correctly
- [ ] Loading states display properly