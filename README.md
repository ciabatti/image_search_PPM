# Image Search with Embedding & Chroma DB

This Django-based web application allows users to search for images by entering a word or query. The query word is embedded using the CLIP model, and the resulting embedding is used to query a Chroma database, which stores the image embeddings. Admin users can upload images with a name and description, generate embeddings for them, and store these embeddings in the Chroma database for fast and efficient image retrieval during search.

The frontend consists of a **search page** where users can input a word to search, and a **results page** where the most similar images are displayed. The results are sorted by similarity (distance), and the description of each image is shown when hovering the mouse over the image. The app is fully **responsive** thanks to **Bootstrap**, ensuring a smooth user experience across different devices.

## Features

- **User Image Search**: Users can input a word which is embedded using the CLIP model, and a similarity search is performed on the Chroma database to find relevant images.
- **Admin Image Upload**: Admin users can upload images, provide a name and description, and generate embeddings to store in Chroma DB.
- **Chroma DB Integration**: Image embeddings are stored in Chroma DB for efficient image search.
- **CLIP Model**: CLIP (Contrastive Language-Image Pretraining) is used for embedding both images and text into a shared feature space.
- **Responsive Frontend**: The application includes a **search page** and a **results page**. The results are displayed in a grid, and each image's description is revealed when the user hovers over the image. The interface is responsive and works well on all screen sizes thanks to the use of **Bootstrap**.
  
## Technologies Used

- **Django**: The web framework used for building the application.
- **Chroma DB**: A database designed for storing and querying embeddings.
- **CLIP (Contrastive Language-Image Pretraining)**: A model that embeds images and text into a common space for similarity search.
- **Docker**: Containerization for consistent and easy deployment of the app.
- **Bootstrap**: A front-end framework used to ensure the app is responsive and works on a variety of devices (mobile, tablet, desktop).
  
## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/image_search_PPM.git
cd image_search_PPM
