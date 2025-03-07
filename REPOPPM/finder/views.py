from django.shortcuts import render, redirect
from django.conf import settings 
from django.views.decorators.http import require_POST
from django.urls import reverse
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
import numpy as np

# chromadb setup
db_path = "MyChromaDB"
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()
collection = client.get_or_create_collection(
    name='images_collection',
    embedding_function=embedding_function,
    data_loader=data_loader
)

def search_images(query):
    results = collection.query(query_texts=[query], n_results=6, include=["distances", "metadatas"])
    return results

#searchbar view
def finder(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            return redirect(reverse('result') + f'?query={query}')
    return render(request, 'searchbar.html')

# Result view
def result(request):
    query = request.POST.get('query', '')  
    images = []

    if query:
        results = search_images(query)
        distances = np.array(results['distances'][0])

        if len(distances) > 0:
            min_distance = np.min(distances) # Find the closest match (minimum distance)
            std_dev = np.std(distances)  #  Compute standard deviation of distances
            threshold = min_distance + (std_dev * 1.5)  # Define a dynamic threshold

            images = [
                {
                    'path': os.path.join(settings.MEDIA_URL, os.path.basename(md['image_path'])),
                    'distance': distance,
                    'description': md.get('description', 'Nessuna descrizione disponibile')
                }
                for image_id, distance, md in zip(results['ids'][0], distances, results['metadatas'][0])
                if 'image_path' in md and distance <= threshold  # filtered by threshold
            ]

    return render(request, 'result/result.html', {'images': images, 'query': query})
