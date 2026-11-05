const productSelect = document.getElementById("id_product");
const quantityInput = document.getElementById("id_quantity");

const availableStock = document.getElementById("available-stock");
const sellingPrice = document.getElementById("selling-price");
const quantityHint = document.getElementById("quantity-hint");

const summaryQuantity = document.getElementById("summary-quantity");
const summaryPrice = document.getElementById("summary-price");
const saleTotal = document.getElementById("sale-total");
const saleSubmit = document.getElementById("sale-submit");

let selectedPrice = 0;
let selectedStock = 0;

const money = new Intl.NumberFormat("en-NG", {
    style: "currency",
    currency: "NGN"
});

function updateSaleSummary() {
    const quantity = Number(quantityInput.value);

    summaryQuantity.textContent = quantity > 0 ? quantity : "—";
    summaryPrice.textContent = selectedPrice > 0
        ? money.format(selectedPrice)
        : "—";

    const total = quantity * selectedPrice;

    saleTotal.textContent = money.format(
        Number.isFinite(total) ? total : 0
    );

    const validQuantity =
        Number.isInteger(quantity) &&
        quantity >= 1 &&
        quantity <= selectedStock;

    saleSubmit.disabled = !selectedPrice || !validQuantity;
}

function updateProductInfo() {
    const selectedOption = productSelect.selectedOptions[0];

    if (!selectedOption || !selectedOption.value) {
        selectedPrice = 0;
        selectedStock = 0;

        availableStock.textContent = "—";
        sellingPrice.textContent = "—";
        quantityHint.textContent = "Select a product to see available quantity.";

        quantityInput.value = "";
        quantityInput.removeAttribute("max");

        updateSaleSummary();
        return;
    }

    selectedPrice = Number(selectedOption.dataset.price);
    selectedStock = Number(selectedOption.dataset.quantity);

    availableStock.textContent = `${selectedStock} units`;
    sellingPrice.textContent = money.format(selectedPrice);

    quantityInput.max = selectedStock;
    quantityHint.textContent = `Maximum available: ${selectedStock} units`;

    updateSaleSummary();
}

productSelect.addEventListener("change", updateProductInfo);
quantityInput.addEventListener("input", updateSaleSummary);

// Display the selected product again after a form validation error.
updateProductInfo();
updateSaleSummary();