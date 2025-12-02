// Tab switching functionality
const signupTab = document.getElementById("signup-tab");
const loginTab = document.getElementById("login-tab");
const signupForm = document.getElementById("signup-form");
const loginForm = document.getElementById("login-form");

// Switch to Sign Up form
signupTab.addEventListener("click", () => {
  signupTab.classList.add("active");
  loginTab.classList.remove("active");
  signupForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
  
  // Clear any error messages
  document.getElementById("signup-error").textContent = "";
  document.getElementById("login-error").textContent = "";
});

// Switch to Login form
loginTab.addEventListener("click", () => {
  loginTab.classList.add("active");
  signupTab.classList.remove("active");
  loginForm.classList.remove("hidden");
  signupForm.classList.add("hidden");
  
  // Clear any error messages
  document.getElementById("signup-error").textContent = "";
  document.getElementById("login-error").textContent = "";
});

// Password validation on Sign Up
const signupPasswordInput = document.getElementById("signup-password");
const signupErrorDiv = document.getElementById("signup-error");

signupForm.addEventListener("submit", function (e) {
  const pwd = signupPasswordInput.value;

  // Password requirements:
  // - At least 8 characters
  // - At least 1 capital letter
  // - At least 2 numbers
  // - At least 1 punctuation character
  const hasMinLength = pwd.length >= 8;
  const hasUppercase = /[A-Z]/.test(pwd);
  const digitMatches = pwd.match(/\d/g);
  const digitCount = digitMatches ? digitMatches.length : 0;
  const hasTwoDigits = digitCount >= 2;
  const hasPunctuation = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(pwd);

  // Validate all conditions
  if (!hasMinLength || !hasUppercase || !hasTwoDigits || !hasPunctuation) {
    e.preventDefault(); // Prevent form submission
    signupErrorDiv.textContent =
      "Password must be 8+ chars, 1 capital, 2 numbers, and 1 punctuation.";
  } else {
    signupErrorDiv.textContent = "";
  }
});

// Add input feedback for better UX
signupPasswordInput.addEventListener("input", () => {
  // Clear error message while user is typing
  if (signupErrorDiv.textContent) {
    signupErrorDiv.textContent = "";
  }
});

// Optional: Add dynamic background interaction on mouse move
document.addEventListener("mousemove", (e) => {
  const leaves = document.querySelectorAll(".leaf");
  const mouseX = e.clientX / window.innerWidth;
  const mouseY = e.clientY / window.innerHeight;
  
  leaves.forEach((leaf, index) => {
    const speed = (index + 1) * 10;
    const x = (mouseX - 0.5) * speed;
    const y = (mouseY - 0.5) * speed;
    
    leaf.style.transform = `translate(${x}px, ${y}px)`;
  });
});

// Add subtle parallax effect on scroll (if page becomes scrollable)
window.addEventListener("scroll", () => {
  const scrolled = window.pageYOffset;
  const leaves = document.querySelectorAll(".leaf");
  
  leaves.forEach((leaf, index) => {
    const speed = (index + 1) * 0.5;
    leaf.style.transform = `translateY(${scrolled * speed}px)`;
  });
});