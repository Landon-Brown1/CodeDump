// content.js

function applyGridSetting(gridCount) {
  // Set on <html> for legacy compatibility
  document.documentElement.style.setProperty(
    "--ytd-rich-grid-items-per-row",
    gridCount
  );

  // Wait until the grid renderer is available and patch that too
  const tryApplyToRenderer = () => {
    const gridRenderer = document.querySelector("ytd-rich-grid-renderer");

    if (gridRenderer) {
      gridRenderer.style.setProperty(
        "--ytd-rich-grid-items-per-row",
        gridCount
      );
    } else {
      // Try again in a bit — YouTube might still be building DOM
      setTimeout(tryApplyToRenderer, 100);
    }
  };

  tryApplyToRenderer();
}

// Get grid count from storage and apply
chrome.storage.local.get(["gridCount"], (data) => {
  const gridCount = data.gridCount || 4;
  applyGridSetting(gridCount);

  // Also observe for navigation/page changes (SPA-style)
  const observer = new MutationObserver(() => {
    applyGridSetting(gridCount);
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
});