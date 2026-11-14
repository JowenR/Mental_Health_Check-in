document.addEventListener("DOMContentLoaded", () => {
  // Ask before cancelling
  document.querySelectorAll("[data-confirm]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });
});