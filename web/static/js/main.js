// Prysmax Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initDashboard();
    
    // Auto-refresh data every 30 seconds
    setInterval(refreshStats, 30000);
});

function initDashboard() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add hover effects to stat cards
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click handlers for action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.title;
            const row = this.closest('tr');
            const victimId = row.querySelector('.victim-cell .victim-id').textContent;
            
            handleAction(action, victimId);
        });
    });
    
    // Add mobile menu toggle
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.createElement('button');
    menuToggle.className = 'menu-toggle';
    menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    menuToggle.style.display = 'none';
    
    // Add to main content for mobile
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(menuToggle, mainContent.firstChild);
    }
    
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });
    
    // Show menu toggle on mobile
    function checkMobile() {
        if (window.innerWidth <= 768) {
            menuToggle.style.display = 'block';
        } else {
            menuToggle.style.display = 'none';
            sidebar.classList.remove('open');
        }
    }
    
    window.addEventListener('resize', checkMobile);
    checkMobile();
}

function refreshStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatCards(data);
        })
        .catch(error => {
            console.error('Error refreshing stats:', error);
        });
}

function updateStatCards(data) {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    if (statNumbers.length >= 4) {
        statNumbers[0].textContent = data.total_clients;
        statNumbers[1].textContent = formatNumber(data.passwords_captured);
        statNumbers[2].textContent = formatNumber(data.cookies_stolen);
        statNumbers[3].textContent = data.discord_tokens;
    }
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function handleAction(action, victimId) {
    switch(action) {
        case 'View Details':
            showVictimDetails(victimId);
            break;
        case 'Download':
            downloadVictimData(victimId);
            break;
        default:
            console.log(`Action ${action} for victim ${victimId}`);
    }
}

function showVictimDetails(victimId) {
    // Create modal for victim details
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Victim Details - ${victimId}</h3>
                <button class="modal-close">&times;</button>
            </div>
            <div class="modal-body">
                <div class="victim-details">
                    <div class="detail-group">
                        <label>Victim ID:</label>
                        <span>${victimId}</span>
                    </div>
                    <div class="detail-group">
                        <label>Status:</label>
                        <span class="status-badge secure">Active</span>
                    </div>
                    <div class="detail-group">
                        <label>Last Seen:</label>
                        <span>Just now</span>
                    </div>
                    <div class="detail-group">
                        <label>Data Collected:</label>
                        <div class="data-stats">
                            <span class="data-item"><i class="fas fa-key"></i> 651 Passwords</span>
                            <span class="data-item"><i class="fas fa-cookie"></i> 1,234 Cookies</span>
                            <span class="data-item"><i class="fab fa-discord"></i> 3 Tokens</span>
                            <span class="data-item"><i class="fas fa-wallet"></i> 2 Wallets</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add close handlers
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function downloadVictimData(victimId) {
    // Simulate download
    const link = document.createElement('a');
    link.href = '#';
    link.download = `Prysmax-${victimId}.zip`;
    
    // Show download notification
    showNotification(`Downloading data for ${victimId}...`, 'info');
    
    // Simulate download delay
    setTimeout(() => {
        showNotification(`Download completed: Prysmax-${victimId}.zip`, 'success');
    }, 2000);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '9999',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.background = '#10b981';
            break;
        case 'error':
            notification.style.background = '#ef4444';
            break;
        case 'warning':
            notification.style.background = '#f59e0b';
            break;
        default:
            notification.style.background = '#3b82f6';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other scripts
window.PrysmaxDashboard = {
    refreshStats,
    showNotification,
    handleAction,
    formatNumber
};

