const searchInput = document.getElementById("product-search");
const filterButtons = document.querySelectorAll(".filter-btn");
const sortSelect = document.getElementById("product-sort");
const productList = document.getElementById("product-list");
const emptySearch = document.getElementById("empty-search");
const resultCount = document.getElementById("result-count");

const productRows = Array.from(
    document.querySelectorAll(".product-row")
);

let activeFilter = "all";


function updateProducts() {

    const searchTerm = searchInput.value.toLowerCase().trim();

    let visibleCount = 0;

    productRows.forEach(row => {

        const name = row.dataset.name;
        const category = row.dataset.category;
        const status = row.dataset.status;

        const matchesSearch =
            name.includes(searchTerm) ||
            category.includes(searchTerm);

        const matchesFilter =
            activeFilter === "all" ||
            status === activeFilter;

        const visible = matchesSearch && matchesFilter;

        row.classList.toggle("d-none", !visible);

        if (visible) {
            visibleCount++;
        }

    });


    // Update result count
    if (resultCount) {
        resultCount.textContent =
            `Showing ${visibleCount} products`;
    }


    // Show empty search message
    if (emptySearch) {
        emptySearch.classList.toggle(
            "d-none",
            visibleCount !== 0
        );
    }

}


// SEARCH
if (searchInput) {
    searchInput.addEventListener("input", updateProducts);
}


// FILTERS
filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        filterButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        activeFilter = button.dataset.filter;

        updateProducts();

    });

});


// SORTING
if (sortSelect && productList) {

    sortSelect.addEventListener("change", () => {

        const sortType = sortSelect.value;

        const sortedRows = [...productRows];

        sortedRows.sort((a, b) => {

            const nameA = a.dataset.name;
            const nameB = b.dataset.name;

            const priceA = Number(a.dataset.price);
            const priceB = Number(b.dataset.price);

            const dateA = Number(a.dataset.created);
            const dateB = Number(b.dataset.created);

            switch (sortType) {

                case "oldest":
                    return dateA - dateB;

                case "name":
                    return nameA.localeCompare(nameB);

                case "price-low":
                    return priceA - priceB;

                case "price-high":
                    return priceB - priceA;

                case "newest":
                default:
                    return dateB - dateA;

            }

        });


        sortedRows.forEach(row => {
            productList.appendChild(row);
        });

    });

}