# VertexAI client compatible with OpenAI sdk

If a customer really likes the OpenAI python library, but wants to call Vertex, they can use this code to provide a plug-and-play class that will use application default credentials according to best practices. Without this class, they are only able to authenticate with a Gemini API key. 