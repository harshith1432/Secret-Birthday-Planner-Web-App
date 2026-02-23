// Secret Birthday Planner - Client Side Logic

document.addEventListener('DOMContentLoaded', () => {
    console.log('Secret Birthday Planner initialized! 🎂');

    // Dynamic animation for the surprise meter
    const meter = document.getElementById('surprise-meter-bar');
    const percentageText = document.getElementById('surprise-percentage');
    
    if (meter) {
        // Simple mock progress increase for visual effect
        setTimeout(() => {
            meter.style.width = '65%';
            if (percentageText) percentageText.innerText = '65';
        }, 1000);
    }
});
