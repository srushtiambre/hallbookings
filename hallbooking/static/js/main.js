// Close alert messages
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });

    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const startTime = form.querySelector('[name="start_time"]');
    const endTime = form.querySelector('[name="end_time"]');
    const expectedAttendees = form.querySelector('[name="expected_attendees"]');
    const capacity = parseInt(expectedAttendees?.max || 0);

    if (startTime && endTime) {
        if (startTime.value >= endTime.value) {
            alert('Start time must be before end time');
            return false;
        }
    }

    if (expectedAttendees && capacity) {
        if (parseInt(expectedAttendees.value) > capacity) {
            alert(`Expected attendees cannot exceed hall capacity of ${capacity}`);
            return false;
        }
    }

    return true;
}

// AJAX availability check
function checkAvailability(hallId, date) {
    if (!date) return;

    fetch(`/api/check-availability/?hall_id=${hallId}&date=${date}`)
        .then(response => response.json())
        .then(data => {
            const check = document.getElementById('availabilityCheck');
            if (check) {
                const text = document.getElementById('availabilityText');
                if (data.available) {
                    check.className = 'availability-check available';
                    text.textContent = '✓ This date appears to be available';
                } else {
                    check.className = 'availability-check unavailable';
                    text.textContent = '⚠ This date may have conflicts. Please choose another time slot.';
                }
                check.style.display = 'block';
            }
        })
        .catch(error => console.error('Error checking availability:', error));
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Format date input to show only future dates
const dateInputs = document.querySelectorAll('input[type="date"]');
dateInputs.forEach(input => {
    const today = new Date().toISOString().split('T')[0];
    input.setAttribute('min', today);
});

console.log('Hall Booking System initialized');
