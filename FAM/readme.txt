Welcome to the app Family Asian Market!

Presentation video: https://www.youtube.com/watch?v=2lCo4se54cQ

This app is inspired by a business my parents own called Family Asian Market (familyasianmarket.com)
This app is a multipage app designed to present the business' items and have a cart and checkout process.
Based on online the convention for shopping apps is to make multipage checkout process. A multipage checkout process accomplishes a few things such as the user's ability to verify the items
and for multi checks with the server. So instead of an instant checkout/buy process, my checkout process goes from cart, review, order, checkout (which uploads the data to the Orders Model)

Here, you will be able to see an app that allows users to shop the business' products online

To run this app: run "python manage.py makemigrations" then "python manage.py migrate" to migrate the models to the database.
After migrations, run "python manage.py runserver"

Once the server is run, click on the link that appears in the terminal.
You will be able to see the basic homepage of the app that uses javascript buttons to display, contact us page, hours page, and about us page.
The javascript decision here was because of how there wasn't a lot of data to display for loading issues. 

On the navigation bar, you will be able to Log In, register, View Products, and even add products to your cart. 
The app also has the icons for the business' social media, which directly links to those pages, as inspired by the actual website.

To view admin capabilities use the log in:
username: famadmin
password: Philippians4678

The admin account can do everything an average user does and add items to the store.
The add item functionality code is from the "Auction" project and edited to fit the needs of the app.
I wanted an admin UI here for my family to potentially use instead of the django admin.

(Add item is from the auction project)
To add an item:
Log in using the admin account
On the navbar, click "Create Item"
Once directed to the "Create Item" page, the admin account can add the form fields: title, description, category, price
The admin user can also edit any product


A regular user can:
Add item/s to cart
Edit the number of items in the cart when they go to the cart page
Review order which is the same as the cart page except it's uneditable
Proceed to payment which asks for the user's information (but not card number or details)
Once the user submits their information, that order goes into their order history
Add comments to an item page

I've opted for a less extensive checkout functionality, as this wouldn't be how we would implement it in the real world,
but I tried to capture the essence of what we would need it for, that is to add the order details into the database.
The order item page was harder to implement, and I didn't have time for the additional functionality of the admin user changin the order status 

I split the products into two categories: Grocery and Menu, as Menu was really by availability.

The form for checkout doesn't verify the data, but that's probably my level of understanding and time constraints for the form field validation

Thank you!
