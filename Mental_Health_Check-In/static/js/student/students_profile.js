const form = document.getElementById("profileForm");
const btn = document.getElementById("editBtn");
const cancelBtn = document.getElementById("cancelBtn");

if (form && btn) {
  const fields = form.querySelectorAll("input[data-editable]");
  let editing = false;

  const originalValues = {};
  fields.forEach((f) => (originalValues[f.name] = f.value));

  function enterEditMode() {
    editing = true;
    fields.forEach((f) => f.removeAttribute("readonly"));
    if (fields[0]) fields[0].focus();
    btn.textContent = "Save Changes";
    if (cancelBtn) cancelBtn.classList.remove("hidden");
  }

  function exitEditMode() {
    editing = false;
    fields.forEach((f) => {
      f.value = originalValues[f.name];
      f.setAttribute("readonly", "");
    });
    btn.textContent = "Edit Profile";
    if (cancelBtn) cancelBtn.classList.add("hidden");
  }

  form.addEventListener("submit", (e) => {
    if (!editing) {
      e.preventDefault();
      enterEditMode();
    }
  });

  if (cancelBtn) cancelBtn.addEventListener("click", exitEditMode);
}

// --- Toast popup ---
document.querySelectorAll(".toast").forEach((toast) => {
  const show = () => toast.classList.remove("opacity-0", "-translate-y-3");
  const hide = () => {
    toast.classList.add("opacity-0", "-translate-y-3");
    setTimeout(() => toast.remove(), 300);
  };

  requestAnimationFrame(show);
  setTimeout(hide, 3000);

  const closeBtn = toast.querySelector(".toast-close");
  if (closeBtn) closeBtn.addEventListener("click", hide);
});