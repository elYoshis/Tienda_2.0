document.addEventListener('DOMContentLoaded', () => {
    // Referencias a los elementos del DOM
    const searchInput = document.getElementById('searchInput');
    const typeSelect = document.getElementById('typeSelect');
    const sizeSelect = document.getElementById('sizeSelect');
    const priceRange = document.getElementById('priceRange');
    const priceLabel = document.getElementById('priceLabel');
    const productsContainer = document.getElementById('productsContainer'); 

    // Verificamos que estamos en la página del catálogo antes de ejecutar la lógica
    if (!productsContainer) return;

    // Función para obtener los productos desde Flask
    async function fetchProducts() {
        const q = searchInput.value;
        const type = typeSelect.value;
        const size = sizeSelect.value;
        const maxPrice = priceRange.value;

        // Construir la URL con los parámetros
        const params = new URLSearchParams({ q, type, size, max_price: maxPrice });
        
        try {
            const response = await fetch(`/catalogo/api/productos?${params.toString()}`);
            const products = await response.json();
            renderProducts(products);
        } catch (error) {
            console.error("Error cargando productos:", error);
        }
    }

    // Función para dibujar los productos en el HTML
    function renderProducts(products) {
        productsContainer.innerHTML = ''; // Limpiamos el contenedor
        
        if (products.length === 0) {
            productsContainer.innerHTML = '<p class="text-gray-400 col-span-full text-center py-10">No se encontraron juguetes con esos filtros.</p>';
            return;
        }

        products.forEach(p => {
            // Reconstruimos la tarjeta del producto usando template strings
            const imageHtml = p.main_image 
                ? `<img src="/static/img/uploads/${p.main_image}" class="object-cover w-full h-full">`
                : `<span class="text-gray-500">Sin Imagen</span>`;

            const card = `
            <div class="bg-gray-800 rounded-2xl overflow-hidden p-4 shadow-lg">
                <div class="h-40 bg-gray-700 rounded-xl mb-4 flex items-center justify-center overflow-hidden">
                    ${imageHtml}
                </div>
                <h3 class="font-bold text-lg mb-1">${p.name}</h3>
                <p class="text-pink-400 font-bold text-xl">Bs. ${p.price}</p>
                <form action="/carrito/add/${p.id}" method="POST">
                    <button type="submit" class="mt-4 w-full bg-pink-500 hover:bg-pink-600 text-white py-2 rounded-full font-semibold transition">
                        Agregar al carrito
                    </button>
                </form>
            </div>
            `;
            productsContainer.innerHTML += card;
        });
    }

    // Escuchadores de eventos
    searchInput.addEventListener('input', fetchProducts);
    typeSelect.addEventListener('change', fetchProducts);
    sizeSelect.addEventListener('change', fetchProducts);
    
    priceRange.addEventListener('input', (e) => {
        priceLabel.textContent = e.target.value;
    });
    priceRange.addEventListener('change', fetchProducts);
});