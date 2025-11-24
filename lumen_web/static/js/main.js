// ===== Existing API Test =====
document.getElementById("api-test").addEventListener("click", async () => {
  const resultDiv = document.getElementById("api-result");
  try {
    const res = await fetch("/api/get-item");
    const data = await res.json();
    resultDiv.textContent = JSON.stringify(data);
  } catch (err) {
    resultDiv.textContent = "Error fetching API: " + err;
  }
});

// ===== New: Search Form Handling =====
const searchForm = document.getElementById("search-form");

if (searchForm) {
  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // prevent full page reload

    const nameInput = document.getElementById("name").value.trim();
    const resultDiv = document.getElementById("search-result");

    if (!nameInput) {
      resultDiv.innerHTML = "<p style='color:red;'>Please enter a name.</p>";
      return;
    }

    try {
      // ✅ Send POST request with JSON body
      const res = await fetch("/api-search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: nameInput }),
      });

      const data = await res.json();

      // ✅ Display backend response
      if (data.found) {
        resultDiv.innerHTML = `<p style='color:green;'>${data.message}</p>`;
      } else if (data.message) {
        resultDiv.innerHTML = `<p style='color:red;'><strong>Result:</strong> ${data.message}</p>`;
      } else {
        resultDiv.innerHTML = `<p style='color:gray;'>No valid response from backend.</p>`;
      }
    } catch (err) {
      resultDiv.innerHTML = `<p style='color:red;'>Error: ${err}</p>`;
    }
  });
}
