## API Documentation

### Obtain JWT Token
- **POST:** `/token/`: Get JWT Token
- **POST** `/token/refresh/`: Refresh JWT token.

### Customer APIs
- **POST** `/customers/register/`: Register a new customer.
- **POST** `/customers/login/`: Login a customer.
- **GET** `/customers/`: List all customers.
- **GET** `/customers/{id}/`: Retrieve a specific customer.
- **PUT** `/customers/{id}/`: Update a specific customer.
- **DELETE** `/customers/{id}/`: Delete a specific customer.
- **GET** `/customers/get-by-email/`: Retrieve a customer by email.
- **POST** `/customers/update-profile-picture/`: Update a customer's profile picture.

----- 

### Cake APIs
- **GET** `/cakes/`: List all cakes.
- **POST** `/cakes/`: Create a new cake.
- **GET** `/cakes/{id}/`: Retrieve a specific cake.
- **PUT** `/cakes/{id}/`: Update a specific cake.
- **DELETE** `/cakes/{id}/`: Delete a specific cake.

----- 

### Cake Customization APIs
- **GET** `/cake-customizations/`: List all cake customizations.
- **POST** `/cake-customizations/`: Create a new cake customization.
- **GET** `/cake-customizations/{id}/`: Retrieve a specific cake customization.
- **PUT** `/cake-customizations/{id}/`: Update a specific cake customization.
- **DELETE** `/cake-customizations/{id}/`: Delete a specific cake customization.

----- 

### Cart APIs
- **GET** `/carts/`: List all cart items.
- **POST** `/add-cake-to-cart/`: Add a cake to the cart.
- **GET** `/carts/{id}/`: Retrieve a specific cart item.
- **PUT** `/carts/{id}/`: Update a specific cart item.
- **DELETE** `/carts/{id}/`: Delete a specific cart item.

----- 

### Order APIs
- **GET** `/orders/`: List all orders.
- **POST** `/orders/`: Create a new order.
- **GET** `/orders/{id}/`: Retrieve a specific order.
- **PUT** `/orders/{id}/`: Update a specific order.
- **DELETE** `/orders/{id}/`: Delete a specific order.
- **GET** `/orders/by-user/`: Retrieve orders by user ID.
- **GET** `/orders/delivery-tracking/{id}/`: Track delivery of a specific order.

----- 

### Store APIs
- **GET** `/stores/`: List all stores.
- **POST** `/stores/`: Create a new store.
- **GET** `/stores/{id}/`: Retrieve a specific store.
- **PUT** `/stores/{id}/`: Update a specific store.
- **DELETE** `/stores/{id}/`: Delete a specific store.
- **GET** `/stores/{id}/cakes/`: List all cakes in a specific store.
- **GET** `/stores/search/`: Search stores by name or city.
- **GET** `/stores/filter/`: Filter stores by city.
- **GET** `/stores/{id}/store-has-cakes/`: Check if a store has cakes.

----- 

### Payment APIs
- **POST** `/payment/`: Process a payment.

---

## Admin API Documentation

### Admin Customer APIs
- **GET** `/admin/customers/`: List all customers.
- **POST** `/admin/customers/`: Create a new customer.
- **GET** `/admin/customers/{id}/`: Retrieve a specific customer.
- **PUT** `/admin/customers/{id}/`: Update a specific customer.
- **DELETE** `/admin/customers/{id}/`: Delete a specific customer.

----- 

### Admin Cake APIs
- **GET** `/admin/cakes/`: List all cakes.
- **POST** `/admin/cakes/`: Create a new cake.
- **GET** `/admin/cakes/{id}/`: Retrieve a specific cake.
- **PUT** `/admin/cakes/{id}/`: Update a specific cake.
- **DELETE** `/admin/cakes/{id}/`: Delete a specific cake.

----- 

### Admin Cake Customization APIs
- **GET** `/admin/cake-customizations/`: List all cake customizations.
- **POST** `/admin/cake-customizations/`: Create a new cake customization.
- **GET** `/admin/cake-customizations/{id}/`: Retrieve a specific cake customization.
- **PUT** `/admin/cake-customizations/{id}/`: Update a specific cake customization.
- **DELETE** `/admin/cake-customizations/{id}/`: Delete a specific cake customization.

----- 

### Admin Order APIs
- **GET** `/admin/orders/`: List all orders.
- **POST** `/admin/orders/`: Create a new order.
- **GET** `/admin/orders/{id}/`: Retrieve a specific order.
- **PUT** `/admin/orders/{id}/`: Update a specific order.
- **DELETE** `/admin/orders/{id}/`: Delete a specific order.

----- 

### Admin Store APIs
- **GET** `/admin/stores/`: List all stores.
- **POST** `/admin/stores/`: Create a new store.
- **GET** `/admin/stores/{id}/`: Retrieve a specific store.
- **PUT** `/admin/stores/{id}/`: Update a specific store.
- **DELETE** `/admin/stores/{id}/`: Delete a specific store.
- **GET** `/admin/stores/{id}/store-has-cakes/`: List cakes available in a specific store.

----- 

<h4 align='center'>© 2024 Sundram Sharma</h4>


