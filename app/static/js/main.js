// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.remove('show');
            setTimeout(function() {
                alert.remove();
            }, 150);
        }, 5000);
    });
});

// Skills input enhancement
document.addEventListener('DOMContentLoaded', function() {
    const skillsInput = document.getElementById('skills');
    if (skillsInput) {
        // Trim whitespace from skills
        skillsInput.addEventListener('blur', function() {
            const skills = this.value.split(',');
            const trimmedSkills = skills.map(skill => skill.trim()).filter(skill => skill);
            this.value = trimmedSkills.join(', ');
        });
        
        // Prevent duplicate commas
        skillsInput.addEventListener('input', function() {
            this.value = this.value.replace(/,\s*,/g, ',');
        });
    }
});

// Phone number formatting
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    }
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Responsive navbar collapse
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.addEventListener('click', function(e) {
            const isNavbarClick = navbarToggler.contains(e.target) || navbarCollapse.contains(e.target);
            
            if (!isNavbarClick && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    }
}); 