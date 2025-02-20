from django.shortcuts import render, redirect
from django.conf import settings 
from django.views.decorators.http import require_POST
from django.urls import reverse
import chromadb
import torch
from transformers import CLIPProcessor, CLIPModel
import os

# Load the CLIP model from Hugging Face
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()  # Set to evaluation mode

# Set up the ChromaDB database
db_path = "MyChromaDB"
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name='images_collection')  # No embedding_function required

# Function to get text embedding using CLIP
def get_text_embedding(text):
    try:
        inputs = processor(text=[text], return_tensors="pt")  # Prepare the text
        with torch.no_grad():
            embedding = model.get_text_features(**inputs)  # Generate text embedding
            
        return embedding.squeeze().tolist()  
    except Exception as e:
        print(f"Error extracting the text embedding: {e}")
        return None

# Function to search images using text embedding
def search_images(query):
    query_embedding = get_text_embedding(query)  # Convert text to embedding
    if query_embedding is None:
        return {'ids': [[]], 'distances': [[]], 'metadatas': [[]]}  # No results

    # Perform search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=6,  
        include=["distances", "metadatas"]
    )
    return results

# View for the search bar
def finder(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            return redirect(reverse('result') + f'?query={query}')
    return render(request, 'searchbar.html')

# View for search results
def result(request):
    query = request.POST.get('query', '')  
    images = []

    if query:
        results = search_images(query)

        # Extract distances
        distances = results['distances'][0]

        if distances:
            min_distance = min(distances)  # Find the closest match
            threshold = min_distance * 1.05  # Set the 10% threshold

            # Prepare data for display
            images = [
                {
                    'path': os.path.join(settings.MEDIA_URL, os.path.basename(md['image_path'])),
                    'distance': distance,
                    'description': md.get('description', 'No description available')  
                }
                for image_id, distance, md in zip(results['ids'][0], distances, results['metadatas'][0])
                if 'image_path' in md and distance <= threshold  # Filter by distance threshold
            ]

    return render(request, 'result/result.html', {'images': images, 'query': query})
