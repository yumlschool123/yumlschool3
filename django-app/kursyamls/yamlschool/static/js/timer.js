document.addEventListener('DOMContentLoaded', function() {
    console.log('Timer.js загружен');
    
    const timerContainer = document.getElementById('timer');
    const timeDisplay = document.getElementById('time-remaining');
    
    if (!timerContainer || !timeDisplay) {
        console.error('Элементы таймера не найдены');
        return;
    }
    
    // Получаем время из атрибута data-time или из текста элемента
    let minutes = 0;
    if (timerContainer.dataset.time) {
        minutes = parseInt(timerContainer.dataset.time);
    } else {
        const timeText = timeDisplay.textContent;
        const timeMatch = timeText.match(/(\d+):(\d+)/);
        if (timeMatch) {
            minutes = parseInt(timeMatch[1]);
        }
    }
    
    if (isNaN(minutes) || minutes <= 0) {
        console.error('Невозможно определить время для таймера');
        return;
    }
    
    console.log(`Таймер запущен на ${minutes} минут`);
    
    let totalSeconds = minutes * 60;
    let intervalId = null;
    
    function updateTimer() {
        const minutesLeft = Math.floor(totalSeconds / 60);
        const secondsLeft = totalSeconds % 60;
        
        timeDisplay.textContent = 
            String(minutesLeft).padStart(2, '0') + ':' + 
            String(secondsLeft).padStart(2, '0');
        
        if (totalSeconds <= 0) {
            clearInterval(intervalId);
            console.log('Время истекло!');
            alert('Время истекло! Тест будет автоматически отправлен.');
            document.getElementById('test-form').submit();
        }
        
        totalSeconds--;
    }
    
    // Запускаем таймер
    updateTimer();
    intervalId = setInterval(updateTimer, 1000);
}); 