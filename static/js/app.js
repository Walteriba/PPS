// app.js

document.addEventListener("DOMContentLoaded", () => {
  const themeToggleBtn = document.getElementById("theme-toggle-btn");

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      // 1. Determina el nuevo tema
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";

      fetch("/set-theme", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ theme: newTheme }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document.documentElement.setAttribute("data-theme", newTheme);
            document.documentElement.setAttribute("data-bs-theme", newTheme);
            themeToggleBtn.innerHTML =
              newTheme === "light"
                ? '<i class="bi bi-sun text-warning"></i>'
                : '<i class="bi bi-moon text-light"></i>';
          }
        })
        .catch((error) => console.error("Error al cambiar el tema:", error));
    });
  }
});
