// 1. Mobile Menu Toggle
function toggleMenu() {
    const links = document.getElementById('navLinks');
    if (links) links.classList.toggle('active');
}

// 2. Typewriter Effect (only if element exists)
document.addEventListener("DOMContentLoaded", () => {
    const typeWriterElement = document.getElementById('typewriter');
    if (typeWriterElement) {
        const textToType = "Searching: 'Django Expert' offering 'Guitar'...";
        let i = 0;
        function typeWriter() {
            if (i < textToType.length) {
                typeWriterElement.textContent += textToType.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            } else {
                setTimeout(() => {
                    typeWriterElement.textContent = "";
                    i = 0;
                    typeWriter();
                }, 3000);
            }
        }
        typeWriter();
    }

    // 3. 3D Tilt Logic (only on home)
    const container = document.getElementById('tilt-container');
    const card = document.getElementById('tilt-card');
    if (container && card && window.matchMedia("(min-width: 768px)").matches) {
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const xRotation = -((y - rect.height/2) / 20);
            const yRotation = ((x - rect.width/2) / 20);
            card.style.transform = `rotateX(${xRotation}deg) rotateY(${yRotation}deg) scale(1.05)`;
        });

        container.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
        });
    }

    // 4. Spotlight Hover Effect (for features)
    const featureGrid = document.getElementById('feature-grid');
    if (featureGrid) {
        featureGrid.onmousemove = e => {
            for (const box of document.getElementsByClassName('feature-box')) {
                const rect = box.getBoundingClientRect(),
                    x = e.clientX - rect.left,
                    y = e.clientY - rect.top;
                box.style.setProperty('--mouse-x', `${x}px`);
                box.style.setProperty('--mouse-y', `${y}px`);
            }
        };
    }
});


function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    const menuIcon = document.getElementById('menuIcon');
    
    navLinks.classList.toggle('active');
    
    // Icon ko 'bars' se 'times' (cross) mein badlein
    if (navLinks.classList.contains('active')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-times');
    } else {
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
    }
}