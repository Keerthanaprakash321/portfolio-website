document.addEventListener('DOMContentLoaded', () => {
    // --- Contact Form Validation ---
    const contactForm = document.querySelector('form[action*="contact"]'); // Adjust selector as needed
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            let isValid = true;
            const nameInput = contactForm.querySelector('input[name="name"]');
            const emailInput = contactForm.querySelector('input[name="email"]');
            const messageInput = contactForm.querySelector('textarea[name="message"]');

            // Simple validation helper
            const validateField = (input, condition, msg) => {
                const errorSpan = input.nextElementSibling;
                if (errorSpan && errorSpan.classList.contains('error-msg')) {
                    errorSpan.remove();
                }
                if (!condition) {
                    const msgEl = document.createElement('span');
                    msgEl.className = 'error-msg text-red-500 text-xs mt-1 block';
                    msgEl.innerText = msg;
                    input.parentNode.appendChild(msgEl);
                    input.classList.add('border-red-500');
                    return false;
                } else {
                    input.classList.remove('border-red-500');
                    return true;
                }
            };

            if (nameInput) isValid &= validateField(nameInput, nameInput.value.trim() !== '', 'Name is required');
            if (emailInput) isValid &= validateField(emailInput, /\S+@\S+\.\S+/.test(emailInput.value), 'Valid email is required');
            if (messageInput) isValid &= validateField(messageInput, messageInput.value.trim() !== '', 'Message is required');

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // --- Project Filtering ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    if (filterButtons.length > 0 && projectCards.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all
                filterButtons.forEach(b => b.classList.remove('bg-blue-600', 'text-white'));
                filterButtons.forEach(b => b.classList.add('bg-gray-200', 'text-gray-800'));

                // Add active class to clicked
                btn.classList.remove('bg-gray-200', 'text-gray-800');
                btn.classList.add('bg-blue-600', 'text-white');

                const filterValue = btn.getAttribute('data-filter');

                projectCards.forEach(card => {
                    const techs = card.getAttribute('data-tech').toLowerCase();
                    if (filterValue === 'all' || techs.includes(filterValue.toLowerCase())) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // --- Robust Anchor Navigation ---
    const navLinks = document.querySelectorAll('nav a[href*="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const [url, anchor] = href.split('#');

            // If we are already on the home page (or the root), handle scrolling manually
            if (window.location.pathname === '/' || window.location.pathname === url) {
                const targetElement = document.getElementById(anchor);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                    // Update URL hash without jumping
                    history.pushState(null, null, `#${anchor}`);
                }
            } else {
                // Let the browser handle the navigation to '/' naturally
                // The scroll-smooth CSS will handle the rest upon load if supported
            }
        });
    });

    // --- Auto-dismiss Messages ---
    const alerts = document.querySelectorAll('[role="alert"]');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                // Fade out effect
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 500); // Wait for transition to finish
            });
        }, 5000); // 5 seconds
    }
});
