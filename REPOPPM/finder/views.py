from django.shortcuts import render, redirect
from django.conf import settings 
from django.views.decorators.http import require_POST
from django.urls import reverse
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os

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
    results = collection.query(query_texts=[query], n_results=6, include=["distances","metadatas"])
    return results

# search view
def finder(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            return redirect(reverse('result') + f'?query={query}')
    return render(request, 'searchbar.html')

# result view
def result(request):
    
    query = request.POST.get('query', '')
    images = []

    if query:
        # get images by query
        results = search_images(query)
        # prepares the data to be displayed
        images = [
    {
        'path': os.path.join(settings.MEDIA_URL, os.path.basename(md['image_path'])),
        'distance': distance,
        'description': md.get('description', 'Nessuna descrizione disponibile')  
    }
    for image_id, distance, md in zip(results['ids'][0], results['distances'][0], results['metadatas'][0])
    if 'image_path' in md  # check image_path exists
]

       
    return render(request, 'result/result.html', {'images': images, 'query': query})
