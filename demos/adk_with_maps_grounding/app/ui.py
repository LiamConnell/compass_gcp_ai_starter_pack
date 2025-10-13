from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import sys
import os
import re
from typing import List, Dict

# Add the parent directory to the path so we can import maps_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maps_agent.run_agent import run_agent

def add_inline_links(text: str, grounding_links: List[Dict]) -> str:
    """
    Add inline links to grounded places mentioned in the text.
    """
    if not text or not grounding_links:
        return text
    
    # Create a copy of the text to modify
    result_text = text
    
    # Process links from longest title to shortest to avoid partial matches
    sorted_links = sorted(grounding_links, key=lambda x: len(x['title']), reverse=True)
    
    for link in sorted_links:
        title = link['title']
        uri = link['uri']
        
        # Create pattern that matches the title as whole words (case insensitive)
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(title) + r'\b'
        
        # Create the replacement link HTML
        replacement = f'<a href="{uri}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">{title}</a>'
        
        # Replace all occurrences (case insensitive)
        result_text = re.sub(pattern, replacement, result_text, flags=re.IGNORECASE)
    
    return result_text

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "ask"})

@app.get("/blurb-generator", response_class=HTMLResponse)
async def blurb_generator(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_tab": "blurb"})

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    try:
        events = await run_agent(question)
        # Extract the response content, grounding links, and widget token from events
        response = ""
        grounding_links = []
        widget_context_token = None
        
        for event in events:
            if hasattr(event, 'content') and event.author == "maps_agent":
                # Extract text from content parts
                if hasattr(event.content, 'parts') and event.content.parts:
                    # Get text from the first part
                    response = event.content.parts[0].text if event.content.parts[0].text else ""
                else:
                    response = str(event.content)
            
            # Extract grounding metadata if available
            if hasattr(event, 'grounding_metadata') and event.grounding_metadata:
                # Get the widget context token
                widget_context_token = getattr(event.grounding_metadata, 'google_maps_widget_context_token', None)
                
                grounding_chunks = getattr(event.grounding_metadata, 'grounding_chunks', [])
                for chunk in grounding_chunks:
                    if hasattr(chunk, 'maps') and chunk.maps:
                        maps_data = chunk.maps
                        if hasattr(maps_data, 'title') and hasattr(maps_data, 'uri'):
                            grounding_links.append({
                                'title': maps_data.title,
                                'uri': maps_data.uri,
                                'place_id': getattr(maps_data, 'place_id', None)
                            })
        
        # Add inline links to the response text
        response_with_links = add_inline_links(response, grounding_links)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "question": question,
            "response": response_with_links,
            "grounding_links": grounding_links,
            "widget_context_token": widget_context_token,
            "active_tab": "ask"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "question": question,
            "error": str(e),
            "active_tab": "ask"
        })

@app.post("/generate-blurb", response_class=HTMLResponse)
async def generate_blurb(request: Request, address: str = Form(...), persona: str = Form(...), other_notes: str = Form("")):
    try:
        # Construct the prompt
        prompt = f"Generate a blurb about {address} that would appeal to {persona}. Write it in a natural, engaging way without being overly obvious about the target audience"
        if other_notes.strip():
            prompt += f". Additional notes: {other_notes}"
        
        events = await run_agent(prompt)
        # Extract the response content, grounding links, and widget token from events
        response = ""
        grounding_links = []
        widget_context_token = None
        
        for event in events:
            if hasattr(event, 'content') and event.author == "maps_agent":
                # Extract text from content parts
                if hasattr(event.content, 'parts') and event.content.parts:
                    # Get text from the first part
                    response = event.content.parts[0].text if event.content.parts[0].text else ""
                else:
                    response = str(event.content)
            
            # Extract grounding metadata if available
            if hasattr(event, 'grounding_metadata') and event.grounding_metadata:
                # Get the widget context token
                widget_context_token = getattr(event.grounding_metadata, 'google_maps_widget_context_token', None)
                
                grounding_chunks = getattr(event.grounding_metadata, 'grounding_chunks', [])
                for chunk in grounding_chunks:
                    if hasattr(chunk, 'maps') and chunk.maps:
                        maps_data = chunk.maps
                        if hasattr(maps_data, 'title') and hasattr(maps_data, 'uri'):
                            grounding_links.append({
                                'title': maps_data.title,
                                'uri': maps_data.uri,
                                'place_id': getattr(maps_data, 'place_id', None)
                            })
        
        # Add inline links to the response text
        response_with_links = add_inline_links(response, grounding_links)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "address": address,
            "persona": persona,
            "other_notes": other_notes,
            "response": response_with_links,
            "grounding_links": grounding_links,
            "widget_context_token": widget_context_token,
            "active_tab": "blurb"
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "address": address,
            "persona": persona,
            "other_notes": other_notes,
            "error": str(e),
            "active_tab": "blurb"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)