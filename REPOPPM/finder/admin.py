from django.contrib import admin
from .models import Img
from PIL import Image
from datetime import datetime
import torch
import numpy as np
import chromadb
from transformers import CLIPProcessor, CLIPModel
import os

# Load the CLIP model from Hugging Face
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()  # Set to evaluation mode

# Set up the ChromaDB vector database
db_path = "MyChromaDB"
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name='images_collection')  # No embedding function

# Function to get the current date
def get_date():
    date = datetime.now()
    return date.strftime("%d-%m-%Y %H:%M:%S")

# Function to generate embedding with CLIP
def get_clip_embedding(image_path):
    try:
        image = Image.open(image_path).convert("RGB")  # Load and convert the image
        inputs = processor(images=image, return_tensors="pt")  # Prepare the image for CLIP
        with torch.no_grad():
            embedding = model.get_image_features(**inputs)  # Extract embedding
        return embedding.squeeze().tolist()  # Convert tensor to Python list
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return None

# Admin class for Django
class GetEmbeddingAdmin(admin.ModelAdmin):
    @admin.action(description="Get Embedding")
    def emb_db_load(self, request, queryset):
        for item in queryset:
            a = item.name  
            name_with_embedding = f"{a} (embedded)"
            b = get_date()
            name = f"{a} {b}"  
            description = item.description  
            img_path = item.photo.path  

            if not os.path.exists(img_path):
                self.message_user(request, f"Image not found for {name}.", level='error')
                continue  

            # Generate embedding with CLIP
            embedding = get_clip_embedding(img_path)
            if embedding is None:
                self.message_user(request, f"Error processing image: {name}", level='error')
                continue

            # Add the embedding to ChromaDB collection
            collection.add(
                ids=[name],                  
                embeddings=[embedding],  # Use embedding instead of raw images
                metadatas=[{
                    'description': description,
                    'image_path': img_path  
                }],
            )

            item.name = name_with_embedding
            item.save()
        
        self.message_user(request, "Embeddings loaded successfully.")

    actions = [emb_db_load]

# Register the model in Django Admin
admin.site.register(Img, GetEmbeddingAdmin)
