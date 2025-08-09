# ManasEcomStore
This project is a headless e-commerce backend built with Django and Django REST Framework (DRF).
It provides a complete set of RestAPIs that are used by a separate React + Vite + TypeScript frontend.

- Headless Website - 
    - *Frontend* is deployed in **Vercel**.
    - *Backend* is deployed separately in **Digital Ocean Droplet**.
 
- Website Link - https://ecommerce-frontend-kivd.vercel.app/

<img width="1897" height="1069" alt="image" src="https://github.com/user-attachments/assets/871efb5e-fef4-4a0a-a473-83171bdaa002" />

## Table of Contents
1. [Features](#features)
2. [Run Locally](#run-locally)
3. [API Documentation](#api-documentation)
4. [Feedback](#feedback)
5. [Author](#author)


## Features
- Supports **JWT Authentication system**, with Refresh token rotation.
- Uses K-means clustering-based recommendation model in a Search engine.
- Uses **Django Rest Frameworks** to define RestAPI endpoints.
- It has a scalable design.

## Run Locally
This project uses [UV](https://pypi.org/project/uv/) python virtual environment.

1. Clone the project and move inside Project directory
   ```bash
    git clone https://github.com/GreyHatStyle/Ecommerce-Backend.git
    cd Ecommerce-Backend
   ```

2. Install uv using pip
   ```bash
   pip install uv
   ```
2. Sync the packages, (this will automatically install all required python libraries and make a `.venv` *Virtul Enviornment* of **UV**).
   ```bash
   uv sync
   ```
3. Activate virtual enviornment
   - **Linux/Ubuntu** users.
       ```bash
       source ./.venv/bin/activate
       ```
   - **Windows** users
        ```bash
         .venv\Scripts\activate.bat
        ```

4. Now move to `ecommerce\` directory
   ```bash
   cd ecommerce
   ```
6. And start the Django local server
   ```bash
   uv run manage.py runserver
   ```
   OR
   ```bash
    python manage.py runserver
   ```

This process will start the server in your local system.

## Api Documentation
For reviewing RestAPIs visit https://knozifies.live/

## Feedback
If you have any feedback, please reach me it manasbisht1142004@gmail.com.


## Author

- [@GreyHatStyle(Manas Bisht)](https://github.com/GreyHatStyle)