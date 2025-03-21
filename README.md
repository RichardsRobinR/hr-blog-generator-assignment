# HR Blog Content Generator

## Overview
An AI-powered system that generates SEO-optimized HR blog content using Gemini AI and specialized agents.

## Architecture
![Untitled Diagram drawio](https://github.com/user-attachments/assets/c69a18a2-b006-49fe-ad5e-ad009184d0c3)


### Core Components
- 🤖 **Base Agent**
  - GeminiAgent: Handles AI model interactions
  
- 🔄 **Specialized Agents**
  - ResearchAgent: Topic discovery and analysis
  - ContentPlanningAgent: Blog structure creation
  - ContentGenerationAgent: Content writing
  - SEOAgent: Search optimization
  - ReviewAgent: Quality assurance

### Workflow
1. Research trending HR topics
2. Generate structured outline
3. Create comprehensive content
4. Optimize for SEO
5. Review and polish

## Technologies

### AI & APIs
- 🧠 Google Gemini 1.5 Flash
- 📰 NewsAPI (HR trends)

### Dependencies
```bash
google-generativeai>=0.3.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## Setup

### Prerequisites
- Python 3.8+
- Valid API keys:
  - Google Gemini AI
  - NewsAPI

### Installation

1. Clone repository:
```bash
git clone https://github.com/RichardsRobinR/hr-blog-generator-assignment/
cd hr-blog-generator-assignment
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
echo "NEWS_API_KEY=your_key_here" >> .env
```

## Usage

### Basic Execution
```bash
python main.py
```

### Output
- Generated blog post in markdown format
- SEO-optimized content structure
- Keyword-rich sections

## Configuration

### Adjustable Parameters
- Model temperature
- Token limits
- News query parameters
- Content structure



