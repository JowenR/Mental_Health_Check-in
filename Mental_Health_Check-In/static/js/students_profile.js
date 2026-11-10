const form = document.getElementById("profileForm");
const btn = document.getElementById("editBtn");
const fields = form.querySelectorAll("input[data-editable]");
let editing = false;

form.addEventListener("submit", (e) => {
  if (!editing) {
    e.preventDefault();
    editing = true;
    fields.forEach((f) => f.removeAttribute("readonly"));
    fields[0].focus();
    btn.textContent = "Save Changes";
  }
});

// --- Toast popup ---
document.querySelectorAll(".toast").forEach((toast) => {
  const show = () => toast.classList.remove("opacity-0", "-translate-y-3");
  const hide = () => {
    toast.classList.add("opacity-0", "-translate-y-3");
    setTimeout(() => toast.remove(), 300);
  };

  requestAnimationFrame(show);
  setTimeout(hide, 3000);
  toast.querySelector(".toast-close").addEventListener("click", hide);
});