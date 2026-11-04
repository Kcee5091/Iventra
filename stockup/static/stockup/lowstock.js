const searchInput = document.getElementById("product-search");
const filterButtons = document.querySelectorAll(".filter-btn");
const productRows = document.querySelectorAll(".product-row");
const emptySearch = document.getElementById("empty-search");

let activeFilter = "all";

function filterProducts() {
    const searchTerm = searchInput.value.toLowerCase().trim();

    let visibleCount = 0;

    productRows.forEach(row => {
        const productName = row.dataset.name;
        const productStatus = row.dataset.status;

        const matchesSearch = productName.includes(searchTerm);

        const matchesFilter =
            activeFilter === "all" ||
            activeFilter === productStatus;

        const visible = matchesSearch && matchesFilter;

        row.classList.toggle("d-none", !visible);

        if (visible) {
            visibleCount++;
        }
    });

    if (emptySearch) {
        emptySearch.classList.toggle("d-none", visibleCount !== 0);
    }
}

// Search
if (searchInput) {
    searchInput.addEventListener("input", filterProducts);
}

// Filters
filterButtons.forEach(button => {
    button.addEventListener("click", () => {

        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        activeFilter = button.dataset.filter;

        filterProducts();
    });
});