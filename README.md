<h2 align="center">SweetSpot API</h2>

<h3 align="center">API Development of Sweet Spot: Delivering Delight to Your Doorstep</h3>
<p align="center">SweetSpot is a Python-powered e-commerce platform designed for ordering and delivering customized cakes. It features online ordering, real-time delivery tracking, and efficient store management, all aimed at providing a seamless user experience while enhancing customer satisfaction and optimizing operations.</p>

## Table of Contents 🗂️
- [Features](#features)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Technologies Used](#technologies-used)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [APIs and Integrations](#apis-and-integrations)
- [Acknowledgements](#acknowledgements)
- [Looking Ahead](#looking-ahead)
- [Let’s Connect](#lets-connect)

-----

## Features
- **Authentication**: User can register and login
- **Cake Selection**: Browse and customize cakes with design, ingredients, and size options.  
- **Store Management**: Easily manage multiple stores with updates and additions.  
- **Shopping Cart**: Add, review, and adjust cakes before checkout.  
- **Payment & Checkout**: Secure and efficient transaction processing.  
- **Real-Time Tracking**: Track orders with real-time updates and notifications.  
- **API Management**: Handle user registration, login, payments, and order management via API.  
- **Complete Web Flow**: Seamless experience from browsing to order and delivery tracking.


## Installation 
- [View](Documentation.md)


## API Documentation 
#### Obtain JWT Token
- **POST:** `/token/`: Get JWT Token
- **POST** `/token/refresh/`: Refresh JWT token.

#### Customer APIs
- **POST** `/customers/register/`: Register a new customer.
- **POST** `/customers/login/`: Login a customer.
- **GET** `/customers/`: List all customers.
- **GET** `/customers/{id}/`: Retrieve a specific customer.
- **PUT** `/customers/{id}/`: Update a specific customer.
- **DELETE** `/customers/{id}/`: Delete a specific customer.
- **GET** `/customers/get-by-email/`: Retrieve a customer by email.
- **POST** `/customers/update-profile-picture/`: Update a customer's profile picture.

#### Cake APIs
- **GET** `/cakes/`: List all cakes.
- **POST** `/cakes/`: Create a new cake.
- **GET** `/cakes/{id}/`: Retrieve a specific cake.
- **PUT** `/cakes/{id}/`: Update a specific cake.
- **DELETE** `/cakes/{id}/`: Delete a specific cake.

#### Cake Customization APIs
- **GET** `/cake-customizations/`: List all cake customizations.
- **POST** `/cake-customizations/`: Create a new cake customization.
- **GET** `/cake-customizations/{id}/`: Retrieve a specific cake customization.
- **PUT** `/cake-customizations/{id}/`: Update a specific cake customization.
- **DELETE** `/cake-customizations/{id}/`: Delete a specific cake customization.

#### Cart APIs
- **GET** `/carts/`: List all cart items.
- **POST** `/add-cake-to-cart/`: Add a cake to the cart.
- **GET** `/carts/{id}/`: Retrieve a specific cart item.
- **PUT** `/carts/{id}/`: Update a specific cart item.
- **DELETE** `/carts/{id}/`: Delete a specific cart item.

#### Order APIs
- **GET** `/orders/`: List all orders.
- **POST** `/orders/`: Create a new order.
- **GET** `/orders/{id}/`: Retrieve a specific order.
- **PUT** `/orders/{id}/`: Update a specific order.
- **DELETE** `/orders/{id}/`: Delete a specific order.
- **GET** `/orders/by-user/`: Retrieve orders by user ID.
- **GET** `/orders/delivery-tracking/{id}/`: Track delivery of a specific order.

#### Store APIs
- **GET** `/stores/`: List all stores.
- **POST** `/stores/`: Create a new store.
- **GET** `/stores/{id}/`: Retrieve a specific store.
- **PUT** `/stores/{id}/`: Update a specific store.
- **DELETE** `/stores/{id}/`: Delete a specific store.
- **GET** `/stores/{id}/cakes/`: List all cakes in a specific store.
- **GET** `/stores/search/`: Search stores by name or city.
- **GET** `/stores/filter/`: Filter stores by city.
- **GET** `/stores/{id}/store-has-cakes/`: Check if a store has cakes.

#### Payment APIs
- **POST** `/payment/`: Process a payment.


#### Admin API Documentation

###### Admin Customer APIs
- **GET** `/admin/customers/`: List all customers.
- **POST** `/admin/customers/`: Create a new customer.
- **GET** `/admin/customers/{id}/`: Retrieve a specific customer.
- **PUT** `/admin/customers/{id}/`: Update a specific customer.
- **DELETE** `/admin/customers/{id}/`: Delete a specific customer.

###### Admin Cake APIs
- **GET** `/admin/cakes/`: List all cakes.
- **POST** `/admin/cakes/`: Create a new cake.
- **GET** `/admin/cakes/{id}/`: Retrieve a specific cake.
- **PUT** `/admin/cakes/{id}/`: Update a specific cake.
- **DELETE** `/admin/cakes/{id}/`: Delete a specific cake.

###### Admin Cake Customization APIs
- **GET** `/admin/cake-customizations/`: List all cake customizations.
- **POST** `/admin/cake-customizations/`: Create a new cake customization.
- **GET** `/admin/cake-customizations/{id}/`: Retrieve a specific cake customization.
- **PUT** `/admin/cake-customizations/{id}/`: Update a specific cake customization.
- **DELETE** `/admin/cake-customizations/{id}/`: Delete a specific cake customization.

###### Admin Order APIs
- **GET** `/admin/orders/`: List all orders.
- **POST** `/admin/orders/`: Create a new order.
- **GET** `/admin/orders/{id}/`: Retrieve a specific order.
- **PUT** `/admin/orders/{id}/`: Update a specific order.
- **DELETE** `/admin/orders/{id}/`: Delete a specific order.

###### Admin Store APIs
- **GET** `/admin/stores/`: List all stores.
- **POST** `/admin/stores/`: Create a new store.
- **GET** `/admin/stores/{id}/`: Retrieve a specific store.
- **PUT** `/admin/stores/{id}/`: Update a specific store.
- **DELETE** `/admin/stores/{id}/`: Delete a specific store.
- **GET** `/admin/stores/{id}/store-has-cakes/`: List cakes available in a specific store.

-----

### Technologies Used 
##### Backend 
- **Python**: Core programming language for application development.
- **Django**: Web framework for rapid development and clean design.
- **Django REST Framework**: Toolkit for building Web APIs.
- **PostgreSQL**: Open-source relational database system.

##### Frontend 
- **HTML/CSS**: For structuring and styling web pages.
- **Streamlit**: Framework used for building the entire web application, including user interfaces

##### APIs and Integrations 
- **Google Maps API**: For embedding maps and location services.
- **Formspree**: API for handling form submissions.
- **Swagger/OpenAPI**: For API documentation and testing.
- **SMTP (Gmail)**: For email notifications and communications with users.

<hr>

## Acknowledgements 

This project was developed as part of my learning journey during the Python Full Stack Infosys Springboard Internship 5.0. The internship offered invaluable hands-on experience in full-stack development, enhancing my expertise in Python, Django, and web application architecture.

A heartfelt thank you to **Sri Lalitha L** for their invaluable mentorship and guidance throughout this project.

## Looking Ahead 
I’m excited to explore more opportunities in the fields of Full Stack Development, API Development, API Testing.

## Let’s Connect 
Feel free to discuss ideas, projects, and opportunities in API development, Full Stack Development, or any related topics. I’m always eager to learn and collaborate.
- 📧 Email: [sundramsharma12244@gmail.com](mailto:sundramsharma12244@gmail.com)
- 💼 LinkedIn: [Sundram Sharma](https://www.linkedin.com/in/sundram1/)

----- 

<h4 align='center'>© 2024 Sundram Sharma</h4>
