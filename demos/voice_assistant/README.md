# Real Estate Voice Assistant (mini-demo)
## ADK Demo

### Developer setup

Create a python virtualenv and install requirements in `requirements.txt`. 

Create a file called `.env` in the the `src` directory:

```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_LOCATION=
```

Authorize using `gcloud` for a project that has VertexAI enabled:

```
gcloud auth login
gcloud auth application-default login
```

Navigate to the `src/` directory and launch the web server: `adk web`

### Demo

Select the `crm_agent`. Click the microphone button to start a conversation with the agent. Example commands:

* I want to create a new contact
* I want to add a note for Bob Smith
* Retrieve the file for Alice Johnson. Would she be interested in a two-bedroom condo in the West Village?
* Add a listing to Bob Smith's collection... The address is 123 South First St. 
 