from django.contrib import admin
from .models import Img
from PIL import Image
from datetime import datetime
import numpy as np
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os

# Embedding function
db_path = "MyChromaDB"
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()
collection = client.get_or_create_collection(
    name='images_collection',  
    embedding_function=embedding_function,
    data_loader=data_loader
)

#get current date/time
def get_date():
    date = datetime.now()
    res = date.strftime("%d-%m-%Y %H:%M:%S")
    return res

class GetEmbeddingAdmin(admin.ModelAdmin):
    # Define the custom action
    @admin.action(description="Get Embedding")
    def emb_db_load(self, request, queryset):
        for item in queryset:
            # get image info
            a = item.name  
            name_with_embedding = f"{a} (embedded)"
            b = get_date()
            name = f"{a} {b}"  
            description = item.description  
            img_path = item.photo.path  

            # check the path 
            if not os.path.exists(img_path):
                self.message_user(request, f"Image not founf for {name}.", level='error')
                continue  # next image

            # open and conver image in a numpy array 
            try:
                image = np.array(Image.open(img_path))
            except Exception as e:
                self.message_user(request, f"Error opening image: {e}", level='error')
                continue  # next images
            # add data to chroma
            collection.add(
                ids=[name],                  
                images=[image],         
                metadatas=[{
                    'description': description,
                    'image_path': img_path  
                }],
            )
            item.name = name_with_embedding
            item.save()  # Save the updated name in the database
        self.message_user(request, "Embeddings loaded successfully.")
    actions=[emb_db_load]

#register action
admin.site.register(Img, GetEmbeddingAdmin)
