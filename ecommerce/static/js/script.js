//  disappearing messages 
document.addEventListener('DOMContentLoaded', function() {
    // Function to remove messages after 5 seconds
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.remove();
        });
    }, 5000);  // 5 seconds
});