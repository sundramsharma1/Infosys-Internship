import streamlit as st
import requests

# Backend URLs
REGISTRATION_URL = "http://127.0.0.1:8000/api/customers/"
LOGIN_URL = "http://127.0.0.1:8000/api/customers/login/"
CAKES_URL = "http://127.0.0.1:8000/api/cakes/"
CAKE_CUSTOMIZATION_URL = "http://127.0.0.1:8000/api/cake-customizations/"
CART_URL = "http://127.0.0.1:8000/api/carts/"
ORDER_URL = "http://127.0.0.1:8000/api/orders/" 

# Initialize session state for login status, page, and selected cake for customization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Login"  # Default page
if "selected_cake_id" not in st.session_state:
    st.session_state.selected_cake_id = None
if "cart_items" not in st.session_state:
    st.session_state.cart_items = []

# Sidebar for page navigation
st.sidebar.title("User Authentication")
page_selection = st.sidebar.selectbox("Choose an option", ["Register", "Login", "Cakes", "Customize Cake", "Cart"])
if not st.session_state.logged_in:
    st.session_state.page = page_selection

# Registration page
if st.session_state.page == "Register" and not st.session_state.logged_in:
    st.title("User Registration")
    with st.form("registration_form"):
        email = st.text_input("Email")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
        mobile_no = st.text_input("Phone Number")  # Changed key to match backend
        address = st.text_area("Address")
        city = st.text_input("City")
        state = st.text_input("State")
        pincode = st.text_input("Pincode")
        username = st.text_input("Username")
        submit_button = st.form_submit_button("Register")

    if submit_button:
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "mobile_no": mobile_no,  # Corrected key name
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode,
            "username": username
        }

        try:
            response = requests.post(REGISTRATION_URL, json=data)
            if response.status_code == 201:
                st.success("Registration successful! You can now log in.")
                st.session_state.page = "Login"  # Move to login page after registration
            else:
                st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

# Login page
elif st.session_state.page == "Login" and not st.session_state.logged_in:
    st.title("User Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        login_data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(LOGIN_URL, json=login_data)
            if response.status_code == 200:
                # Log full response to debug missing customer_id
                login_response = response.json()

                st.session_state.logged_in = True
                st.session_state.token = login_response.get("token")
                
                # Ensure customer_id is set if available in the response
                st.session_state.customer_id = login_response.get("customer_id")
                
                if st.session_state.customer_id is not None:
                    st.success("Login successful!")
                    st.session_state.page = "Cakes"  # Move to cakes page after login
                else:
                    st.error("Login successful, but customer ID is missing.")
            else:
                st.error(f"Login failed: {response.json().get('detail', 'Incorrect credentials')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")


# Cakes page
elif st.session_state.page == "Cakes" and st.session_state.logged_in:
    st.title("Available Cakes")
    try:
        response = requests.get(CAKES_URL)
        if response.status_code == 200:
            cakes = response.json()
            if cakes:
                for cake in cakes:
                    st.subheader(cake.get("name", "Unnamed Cake"))
                    image_url = cake.get("image")
                    if image_url:
                        st.image(image_url, width=300)
                    else:
                        st.write("No image available.")
                    st.write(cake.get("description", "No description available"))
                    st.write(f"Flavour: {cake.get('flavour', 'N/A')}")
                    st.write(f"Size: {cake.get('size', 'N/A')}")
                    st.write(f"Price: ${cake.get('price', 'N/A')}")

                    # Customization and Add to Cart buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        # Customize button that navigates to the Customize Cake page
                        if st.button(f"Customize {cake.get('name', 'Unnamed Cake')}", key=f"customize_{cake['id']}"):
                            st.session_state.selected_cake_id = cake["id"]
                            st.session_state.page = "Customize Cake"
                    with col2:
                        # Quantity input and Add to Cart button
                        quantity = st.number_input(f"Quantity for {cake.get('name', 'Unnamed Cake')}", min_value=1, max_value=10, value=1, key=f"quantity_{cake['id']}")
                        if st.button(f"Add {cake.get('name', 'Unnamed Cake')} to Cart", key=f"add_to_cart_{cake['id']}"):
                            if st.session_state.get("customization_id") is None:
                                st.error("Please customize the cake before adding it to the cart.")
                            else:
                                # Prepare data for adding to cart
                                cart_data = {
                                    "customer": st.session_state.customer_id,
                                    "cake": cake["id"],
                                    "quantity": quantity,
                                    "customization": st.session_state.customization_id
                                }
                                try:
                                    # Send POST request to add cake to cart
                                    cart_response = requests.post("http://127.0.0.1:8000/api/add-cake-to-cart/", json=cart_data)
                                    if cart_response.status_code == 201:
                                        st.success(f"{cake.get('name', 'Unnamed Cake')} added to cart!")
                                    else:
                                        st.error(f"Failed to add to cart: {cart_response.json().get('detail', 'Unknown error')}")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Error connecting to backend: {e}")
            else:
                st.write("No cakes are available at the moment.")
        else:
            st.error(f"Failed to load cakes data: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")


# Customize Cake page
elif st.session_state.page == "Customize Cake" and st.session_state.logged_in:
    st.title("Customize Your Cake")

    if st.session_state.selected_cake_id is None:
        st.error("No cake selected for customization.")
    else:
        with st.form("customization_form"):
            message = st.text_area("Message", placeholder="Write a custom message for your cake")
            egg_version = st.selectbox("Egg Version", ["egg", "eggless"])
            toppings = st.selectbox("Toppings", ["sprinkles", "chocolate chips", "none"])
            shape = st.selectbox("Shape", ["round", "square", "heart"])
            submit_customization = st.form_submit_button("Submit Customization")

        if submit_customization:
            customization_data = {
                "message": message,
                "egg_version": egg_version,
                "toppings": toppings,
                "shape": shape,
                "cake": st.session_state.selected_cake_id,
                "customer": st.session_state.customer_id
            }

            try:
                response = requests.post(CAKE_CUSTOMIZATION_URL, json=customization_data)
                if response.status_code == 201:
                    # Store customization ID for use in the cart
                    customization_id = response.json().get("id")
                    st.session_state.customization_id = customization_id
                    st.success("Customization submitted successfully!")
                    st.session_state.page = "Cakes"  # Move back to cakes page after customization
                else:
                    st.error(f"Customization failed: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {e}")

# Cart Page
elif st.session_state.page == "Cart" and st.session_state.logged_in:
    st.title("Your Cart")
    cart_url = f"{CART_URL}{st.session_state.customer_id}/"  # API endpoint to get cart details for logged-in user

    try:
        # Fetch cart details
        cart_response = requests.get(cart_url)
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            items = cart_data.get("items", [])  # List of items in the cart

            if items:
                # Loop through each item in the cart and display its details
                for item in items:
                    cake_name = item["cake"]["name"]
                    quantity = item["quantity"]
                    customization_message = item["customization"]["message"]
                    price_per_item = item["cake"]["price"]
                    item_total = item.get("total_price", price_per_item * quantity)  # Calculate total per item if not provided

                    # Display item details
                    st.subheader(cake_name)
                    st.write(f"Quantity: {quantity}")
                    st.write(f"Customization: {customization_message}")
                    st.write(f"Price per item: ${price_per_item}")
                    st.write(f"Total for this item: ${item_total}")
                    st.write("----")

                # Display the overall total
                cart_total = cart_data.get("total_price", sum(item.get("total_price", price_per_item * quantity) for item in items))
                st.write(f"**Cart Total: ${cart_total}**")

                # Order button
                if st.button("Place Order"):
                    order_data = {
                        "customer": st.session_state.customer_id,
                        "cart": cart_data["id"]  # Assuming the cart has an ID
                    }
                    try:
                        # Send POST request to place an order
                        order_response = requests.post(ORDER_URL, json=order_data)
                        if order_response.status_code == 201:
                            st.success("Order placed successfully!")
                            st.session_state.page = "Cakes"  # Redirect to cakes page after placing order
                        else:
                            st.error(f"Failed to place order: {order_response.json().get('detail', 'Unknown error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend: {e}")
            else:
                st.write("Your cart is empty.")
        else:
            st.error(f"Failed to load cart data: {cart_response.status_code} - {cart_response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
