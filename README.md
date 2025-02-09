# Image Search with Embedding & Chroma DB

This Django-based web application allows users to search for images by entering a word or query. 
The query word is embedded using the CLIP model, and the resulting embedding is used to query a Chroma database, which stores the image embeddings.
Admin users can upload images with a name and description, generate embeddings for them, and store these embeddings in the Chroma database for fast and efficient image retrieval during search.

## Features

- **User Image Search**: Users can input a word which is embedded using the CLIP model, and a similarity search is performed on the Chroma database to find relevant images.
- **Admin Image Upload**: Admin users can upload images, provide a name and description, and generate embeddings to store in Chroma DB.
- **Chroma DB Integration**: Image embeddings are stored in Chroma DB for efficient image search.
- **CLIP Model**: CLIP (Contrastive Language-Image Pretraining) is used for embedding both images and text into a shared feature space.

## Technologies Used

- **Django**: The web framework used for building the application.
- **Chroma DB**: A database designed for storing and querying embeddings.
- **CLIP (Contrastive Language-Image Pretraining)**: A model that embeds images and text into a common space for similarity search.
- **Docker**: Containerization for consistent and easy deployment of the app.


