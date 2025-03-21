import os
# from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests

# load_dotenv()

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash", temperature=0.7):
        self.client = genai.Client(api_key="AIzaSyDVC0r3225IQ4Kk3SUU8P9cBK1KmfqoYQw")
        self.model_name = model_name
        self.default_config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=0.9,
            top_k=32,
            max_output_tokens=8192,
            response_mime_type="text/plain"
        )

    def generate(self, prompt, config=None):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[types.Content(
                role="user",
                parts=[types.Part.from_text(text = prompt)]
            )],
            config=config or self.default_config
        )
        return response.text

class ResearchAgent(GeminiAgent):
    # def get_trending_topics(self):
        # prompt = """Identify 5 trending HR topics for 2024 with SEO potential. 
        # Format as comma-separated values."""
        # return self.generate(prompt).split(", ")

    def get_trending_topics(self):
        """Fetch trending HR topics with detailed descriptions"""
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "(HR OR 'human resources') AND (trends OR innovation OR workplace)",
            "sortBy": "relevancy",
            "apiKey": "4a1a276177544069a3f7d8937aa1301f",
            "pageSize": 5,
            "language": "en"
        }


        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        # Process articles into topic-description pairs
        trending_topics = {}

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            
            # Generate a focused topic and detailed description using Gemini
            prompt = f"""Based on this HR news:
            Title: {title}
            Description: {description}

            1. Extract the main HR topic (in 3-5 words)
            2. Generate a comprehensive description (100 words) explaining:
                - What the topic is about
                - Why it's important for HR
                - Current trends and implications
            
            Format as: {{topic}}: {{description}}"""
            
            response = self.generate(prompt)
            if ":" in response:
                topic, desc = response.split(":", 1)
                trending_topics[topic.strip()] = desc.strip()

        return trending_topics

    def gather_keywords(self, topic, description):
        """Generate SEO keywords based on topic and description"""
        prompt = f"""Based on this HR topic and description:
        Topic: {topic}
        Description: {description}
        
        Generate 10 relevant SEO keywords that capture the key aspects and themes.
        Format as comma-separated values."""
        
        return self.generate(prompt, types.GenerateContentConfig(temperature=0.5)).split(", ")

class ContentPlanningAgent(GeminiAgent):
    def create_outline(self, topic, keywords):
        prompt = f"""Create detailed blog outline for topic: {topic}
        Keywords: {', '.join(keywords)}
        Include 5 sections with 3 subsections each. Use markdown formatting."""
        return self.generate(prompt)

class ContentGenerationAgent(GeminiAgent):
    def write_section(self, outline, section_num):
        prompt = f"""Write 400 words for section {section_num} of this blog outline:
        {outline}
        Use markdown formatting and integrate keywords naturally."""
        return self.generate(prompt)

class SEOAgent(GeminiAgent):
    def optimize_content(self, content, keywords):
        prompt = f"""Optimize this blog content for SEO:
        Content: {content}
        Keywords: {', '.join(keywords)}
        Improve keyword density, add meta description, and ensure proper heading hierarchy."""
        return self.generate(prompt, types.GenerateContentConfig(temperature=0.3))

class ReviewAgent(GeminiAgent):
    def proofread(self, content):
        prompt = f"""Review and improve this blog post:
        {content}
        Check grammar, readability, and SEO best practices."""
        return self.generate(prompt, types.GenerateContentConfig(temperature=0.2))

class BlogGenerator:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.planning_agent = ContentPlanningAgent()
        self.writing_agent = ContentGenerationAgent()
        self.seo_agent = SEOAgent()
        self.review_agent = ReviewAgent()

    def generate_blog(self, topic=None):
        # Research phase
        trending_topics = self.research_agent.get_trending_topics()
        # print(topics)
        # return
        
        selected_topic = next(iter(trending_topics.keys()))
        description = trending_topics[selected_topic]

        keywords = self.research_agent.gather_keywords(selected_topic, description)

        
        # Planning phase
        outline = self.planning_agent.create_outline(selected_topic, keywords)
        
        # Writing phase
        full_content = "\n".join([self.writing_agent.write_section(outline, i+1) 
                                for i in range(5)])
        
        # SEO optimization
        optimized = self.seo_agent.optimize_content(full_content, keywords)
        
        # Final review
        final = self.review_agent.proofread(optimized)
        
        return final

if __name__ == "__main__":
    generator = BlogGenerator()
    blog_content = generator.generate_blog()
    with open("blog_post.md", "w") as f:
        f.write(blog_content)
    print("Blog generated successfully!")