// Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const sidebar = document.querySelector('.sidebar');
        
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (event) => {
            if (window.innerWidth < 768) {
                if (!sidebar.contains(event.target) && !mobileMenuBtn.contains(event.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
        
        // Tab functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.getAttribute('data-tab');
                
                // Update active tab
                document.querySelectorAll('.tab').forEach(t => {
                    t.classList.remove('active');
                });
                tab.classList.add('active');
                
                // Show active content
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                document.getElementById(tabId).classList.add('active');
            });
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    
                    // Close mobile menu if open
                    sidebar.classList.remove('open');
                    
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                    
                    // Update active sidebar item
                    document.querySelectorAll('.sidebar-item').forEach(item => {
                        item.classList.remove('active');
                    });
                    this.classList.add('active');
                }
            });
        });
        
        // Update active sidebar item on scroll
        const sections = document.querySelectorAll('.content-section');
        const sidebarItems = document.querySelectorAll('.sidebar-item');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    sidebarItems.forEach(item => {
                        item.classList.remove('active');
                        if (item.getAttribute('href') === `#${id}`) {
                            item.classList.add('active');
                        }
                    });
                }
            });
        }, {
            rootMargin: '-100px 0px -50% 0px'
        });
        
        sections.forEach(section => {
            observer.observe(section);
        });
        
        // Copy code functionality
        document.querySelectorAll('pre').forEach(preElement => {
            preElement.addEventListener('click', function() {
                const code = this.textContent;
                navigator.clipboard.writeText(code).then(() => {
                    const original = this.style.backgroundColor;
                    this.style.backgroundColor = '#10b981';
                    setTimeout(() => {
                        this.style.backgroundColor = original;
                    }, 300);
                });
            });
        });
        
        // Mark implementation steps as completed on scroll
        const steps = document.querySelectorAll('.implementation-step');
        const stepObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('completed');
                    }, 300);
                }
            });
        }, {
            threshold: 0.5
        });
        
        steps.forEach(step => {
            stepObserver.observe(step);
        });
        
        // Interactive example: Update weather data
        function updateWeatherExample() {
            const tempElements = document.querySelectorAll('.weather-temp');
            const conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy'];
            const randomTemp = Math.floor(Math.random() * 30) + 10;
            const randomCondition = conditions[Math.floor(Math.random() * conditions.length)];
            
            tempElements.forEach(el => {
                if (el.classList.contains('temp')) {
                    el.textContent = `${randomTemp}°C`;
                }
                if (el.classList.contains('condition')) {
                    el.textContent = randomCondition;
                }
            });
        }
        
        // Update weather every 10 seconds for demo effect
        setInterval(updateWeatherExample, 10000);