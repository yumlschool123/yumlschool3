/**
 * Счетчик баллов для формы создания/редактирования теста
 */
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, есть ли на странице форма для теста
    if (!document.querySelector('form')) {
        return;
    }

    // Создаем элементы счетчика
    createScoreCounter();
    
    // Инициализируем отслеживание баллов
    initScoreTracking();
    
    // Добавляем обработчик для кнопки скрытия счетчика
    initToggleButton();
});

/**
 * Создает HTML-элементы счетчика баллов
 */
function createScoreCounter() {
    // Кнопка для скрытия/показа счетчика
    const toggleBtn = document.createElement('div');
    toggleBtn.className = 'toggle-counter';
    toggleBtn.id = 'toggle-counter';
    toggleBtn.innerHTML = '&#9776;';
    document.body.appendChild(toggleBtn);
    
    // Контейнер счетчика баллов
    const scoreCounter = document.createElement('div');
    scoreCounter.className = 'score-counter';
    scoreCounter.id = 'score-counter';
    
    scoreCounter.innerHTML = `
        <h3>Статистика баллов</h3>
        <div class="score-counter-info">
            <span class="total-score" id="total-score">0</span>
            <p>Общий балл всех вопросов</p>
            <p>Количество вопросов: <span id="question-count">0</span></p>
            <p>Средний балл: <span id="average-score">0</span></p>
        </div>
        <div id="counter-status" class="score-counter-valid">
            Баллы распределены корректно
        </div>
    `;
    
    document.body.appendChild(scoreCounter);
}

/**
 * Инициализирует отслеживание изменений баллов
 */
function initScoreTracking() {
    // Находим все поля ввода баллов
    updateScoreCounter();
    
    // Добавляем обработчики для отслеживания изменений
    // Используем делегирование событий для отслеживания новых полей
    document.addEventListener('input', function(e) {
        // Проверяем, что это поле ввода баллов
        if (e.target.matches('input[type="number"][name*="points"]')) {
            updateScoreCounter();
        }
    });
    
    // Отслеживаем добавление новых вопросов
    // Это зависит от того, как в вашем коде добавляются новые вопросы
    // Общий подход - отслеживать мутации DOM
    const observer = new MutationObserver(function(mutations) {
        for (let mutation of mutations) {
            if (mutation.type === 'childList' && mutation.addedNodes.length) {
                updateScoreCounter();
            }
        }
    });
    
    // Находим контейнер вопросов (может потребоваться изменить селектор)
    const questionsContainer = document.querySelector('form') || document.body;
    
    // Настраиваем наблюдение
    observer.observe(questionsContainer, {
        childList: true,
        subtree: true
    });
}

/**
 * Обновляет значения в счетчике баллов
 */
function updateScoreCounter() {
    // Находим все поля ввода баллов
    const pointsInputs = document.querySelectorAll('input[type="number"][name*="points"]');
    
    let totalScore = 0;
    let validInputs = 0;
    
    // Подсчитываем сумму баллов
    pointsInputs.forEach(input => {
        const value = parseFloat(input.value);
        if (!isNaN(value) && value > 0) {
            totalScore += value;
            validInputs++;
        }
    });
    
    // Обновляем данные в счетчике
    document.getElementById('total-score').textContent = totalScore.toFixed(1);
    document.getElementById('question-count').textContent = pointsInputs.length;
    
    // Вычисляем средний балл
    const averageScore = validInputs > 0 ? (totalScore / validInputs).toFixed(2) : '0';
    document.getElementById('average-score').textContent = averageScore;
    
    // Проверяем на корректность распределения баллов
    const counterStatus = document.getElementById('counter-status');
    
    // Здесь можно добавить дополнительные проверки, например, минимальный балл для теста
    if (totalScore <= 0 && pointsInputs.length > 0) {
        counterStatus.className = 'score-counter-invalid';
        counterStatus.textContent = 'Общий балл должен быть больше 0';
    } else if (pointsInputs.length === 0) {
        counterStatus.className = 'score-counter-invalid';
        counterStatus.textContent = 'Добавьте хотя бы один вопрос';
    } else {
        counterStatus.className = 'score-counter-valid';
        counterStatus.textContent = 'Баллы распределены корректно';
    }
}

/**
 * Инициализирует функциональность кнопки переключения видимости счетчика
 */
function initToggleButton() {
    const toggleBtn = document.getElementById('toggle-counter');
    const scoreCounter = document.getElementById('score-counter');
    
    toggleBtn.addEventListener('click', function() {
        scoreCounter.classList.toggle('hidden');
        
        // Сохраняем состояние в localStorage
        const isHidden = scoreCounter.classList.contains('hidden');
        localStorage.setItem('scoreCounterHidden', isHidden ? 'true' : 'false');
    });
    
    // Восстанавливаем состояние из localStorage
    const isHidden = localStorage.getItem('scoreCounterHidden') === 'true';
    if (isHidden) {
        scoreCounter.classList.add('hidden');
    }
} 