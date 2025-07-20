# AI Time Capsule

Transform your diary entries into thoughtful letters to your future self using the power of AI.

## Description

AI Time Capsule is an elegant Streamlit-based web application that allows you to write diary entries, then uses an AI language model to rewrite them as thoughtful, motivational letters to your future self. Everything runs locally and for free using Hugging Face's open-source models — no API keys or paid services required.

## Features

- **Elegant Interface**: Clean, professional design with sophisticated styling
- **Local AI Processing**: Uses google/flan-t5-base model for high-quality text transformation
- **Multiple Tones**: Choose from Motivational, Gentle, or Funny letter styles
- **Save Your Letters**: Keep your letters with timestamps for future reference
- **Track Your Journey**: Monitor how many letters you've created
- **Complete Privacy**: Everything runs on your computer, no data leaves your device
- **Completely Free**: No API keys, subscriptions, or hidden costs

## Project Structure

```
ai-time-capsule/
├── app.py                  # Main Streamlit app with elegant UI
├── requirements.txt        # Python dependencies
├── utils.py                # AI model interface and helper functions
├── prompts/
│   └── templates.json      # Prompt templates for different tones
├── outputs/
│   └── saved_letters/      # Your saved letters
└── README.md               # Project documentation
```

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-time-capsule.git
cd ai-time-capsule
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Open Your Browser
Navigate to `http://localhost:8501` and start creating thoughtful letters.

## How to Use

1. **Write Your Diary Entry**: Express your thoughts and feelings in the left column
2. **Choose Your Tone**: Select Motivational, Gentle, or Funny from the sidebar
3. **Transform**: Click the button to generate your letter
4. **Review**: Read your personalized letter to your future self
5. **Save**: Store your letter for future inspiration

## AI Model Details

- **Model**: `google/flan-t5-base`
- **Type**: Text-to-text generation
- **Size**: ~250MB (downloads automatically on first run)
- **Performance**: Excellent for rewriting and transformation tasks
- **Privacy**: Runs 100% locally on your machine

## Customization

### Adding New Tones
Edit `prompts/templates.json` to add your own letter styles:

```json
{
  "your_tone": "Your custom prompt template here: {entry}"
}
```

### Styling Changes
Modify the CSS in `app.py` to customize colors, fonts, and layouts.

## Technical Notes

- **Memory Usage**: ~2-4GB RAM when model is loaded
- **First Run**: Model download may take 5-10 minutes
- **Supported**: Windows, macOS, Linux
- **Python**: 3.8+ required

## Troubleshooting

### Model Won't Load
- Ensure you have stable internet for the initial download
- Check that you have enough RAM (4GB+ recommended)
- Try restarting the app

### Streamlit Issues
- Make sure port 8501 isn't in use
- Try running with `streamlit run app.py --server.port 8502`

## Writing Guidelines

- Write about your genuine feelings and experiences
- Include your current goals and challenges
- Mention what you're grateful for
- Be honest about your struggles
- Practice self-compassion in your reflections

## Contributing

This project is open source. Feel free to:
- Report bugs and issues
- Suggest new features and improvements
- Enhance the user experience
- Improve documentation

## License

This project is available under the MIT License.

## Acknowledgments

- Hugging Face for providing excellent free models
- Streamlit for the wonderful application framework
- The open source community for continuous innovation

---

*Crafted for meaningful self-reflection and future connection*