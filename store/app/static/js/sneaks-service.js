// Import the necessary libraries
const SneaksAPI = require('sneaks-api'); 
const express = require('express'); 
const app = express(); 
const sneaks = new SneaksAPI(); 

// Define a GET route to fetch sneaker products based on keyword and limit
app.get('/products', (req, res) => {
    // Extract query parameters from the request (e.g., 'keyword' and 'limit')
    const { keyword, limit } = req.query; 
    
    // Call the Sneaks API to fetch products based on the keyword and limit
    sneaks.getProducts(keyword, parseInt(limit), (err, products) => {
        if (err) {
            // If there's an error, send a 500 status code and the error message
            return res.status(500).json({ error: err });
        }
        res.json(products);
    });
});

// Start the server to listen on port 3001 for incoming requests
app.listen(3001, () => console.log('Sneaks service running on http://localhost:3001'));

/* 
1. Imports: We import SneaksAPI (from the sneaks-api library) to interact with the sneaker data and express to create a web server.

2. GET Route (/products): This route accepts keyword and limit as query parameters, 
calls the Sneaks API to fetch product data, and sends the result back as a JSON response.

3. Server Setup: We use app.listen() to start the server on port 3001.
*/