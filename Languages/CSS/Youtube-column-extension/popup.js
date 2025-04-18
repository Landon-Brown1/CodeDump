// popup.js

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("gridInput");
  const saveBtn = document.getElementById("saveBtn");

  // Load saved grid count from storage and apply it
  chrome.storage.local.get(["gridCount"], (data) => {
    const gridCount = data.gridCount || 4; // Default to 4 if not set
    input.value = gridCount;
    setGridCount(gridCount); // Apply it immediately on load
  });

  // Event listener for the input field
  input.addEventListener("input", (e) => {
    const value = parseInt(e.target.value, 10);
    setGridCount(value); // Apply the new value live
  });

  // Event listener for the save button
  saveBtn.addEventListener("click", () => {
    const value = parseInt(input.value, 10);
    chrome.storage.local.set({ gridCount: value }, () => {
      saveBtn.textContent = "Saved!";
      setTimeout(() => (saveBtn.textContent = "Save"), 1000);
    });
  });
});

// Function to apply the grid size
function setGridCount(count) {
  // Set CSS variable for the grid size
  document.documentElement.style.setProperty(
    "--ytd-rich-grid-items-per-row",
    count
  );
}