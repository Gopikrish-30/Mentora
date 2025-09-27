# AI Provider Quota Solution

## Problem
The Gemini API has quota limitations that prevent the course creator from working when limits are exceeded.

## Solution
Implemented a multi-provider AI system with intelligent fallback support.

## Available Providers

### 1. DeepSeek API (Recommended)
- **Status**: Primary provider
- **Cost**: Free tier available
- **Performance**: Excellent for course generation
- **Setup**: `python setup_deepseek.py`

### 2. Ollama (Local)
- **Status**: Fallback provider
- **Cost**: Free (runs locally)
- **Performance**: Good, requires local resources
- **Setup**: `python setup_ollama.py`

### 3. Hugging Face (Local)
- **Status**: Fallback provider
- **Cost**: Free (runs locally)
- **Performance**: Basic, lightweight
- **Setup**: Automatic (requires transformers)

### 4. Gemini (Original)
- **Status**: Fallback provider
- **Cost**: Free tier with quotas
- **Performance**: Excellent when available
- **Setup**: `export GOOGLE_API_KEY='your-key'`

## Quick Setup

### Option 1: DeepSeek (Recommended)
```bash
# 1. Get API key from https://platform.deepseek.com/
# 2. Run setup
python setup_deepseek.py

# 3. Start application
python app.py
```

### Option 2: Ollama (Local)
```bash
# 1. Install Ollama
python setup_ollama.py

# 2. Start application
python app.py
```

### Option 3: Complete Setup
```bash
# Install everything and test
python setup_all_providers.py
```

## How It Works

1. **Provider Selection**: System automatically selects the best available provider
2. **Fallback Chain**: DeepSeek → Ollama → Hugging Face → Gemini
3. **Error Handling**: If one provider fails, automatically tries the next
4. **Transparent**: Users don't need to know which provider is being used

## Provider Comparison

| Provider | Cost | Performance | Setup | Quota Limits |
|----------|------|-------------|-------|--------------|
| DeepSeek | Free tier | Excellent | Easy | Generous |
| Ollama | Free | Good | Medium | None |
| Hugging Face | Free | Basic | Easy | None |
| Gemini | Free tier | Excellent | Easy | Strict |

## Troubleshooting

### No Providers Available
```bash
# Check what's available
python -c "from ai_providers import ai_manager; print([p.__class__.__name__ for p in ai_manager.providers if p.is_available()])"
```

### DeepSeek Issues
- Verify API key: `echo $DEEPSEEK_API_KEY`
- Test API: `python setup_deepseek.py`

### Ollama Issues
- Check if running: `curl http://localhost:11434/api/tags`
- Start service: `ollama serve`
- Download model: `ollama pull llama2`

### Hugging Face Issues
- Install transformers: `pip install transformers torch`
- Check disk space (models are large)

## Performance Tips

1. **Use DeepSeek**: Best performance and reliability
2. **Local Models**: Good for privacy and offline use
3. **Model Selection**: Larger models = better quality but slower
4. **Caching**: Generated content is cached in ChromaDB

## Cost Analysis

### DeepSeek
- Free tier: ~1000 requests/month
- Paid: $0.14 per 1M tokens
- **Recommended for most users**

### Ollama
- Free to run locally
- Requires 8GB+ RAM
- **Good for privacy-conscious users**

### Hugging Face
- Free to run locally
- Requires 4GB+ RAM
- **Good for basic use cases**

## Migration Guide

### From Gemini Only
1. Run `python setup_deepseek.py`
2. Get DeepSeek API key
3. Restart application
4. System will automatically use DeepSeek

### Adding Local Models
1. Run `python setup_ollama.py`
2. Install Ollama and download models
3. System will use Ollama as fallback

## Support

If you encounter issues:
1. Check provider availability
2. Verify API keys
3. Test individual providers
4. Check system resources (for local models)

## Future Enhancements

- [ ] Provider performance monitoring
- [ ] Automatic provider switching based on performance
- [ ] User preference for provider selection
- [ ] Cost tracking and optimization
- [ ] Additional providers (OpenAI, Anthropic, etc.)
