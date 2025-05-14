/**
 * Функция для настройки вопросов на сопоставление
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Скрипт matching.js загружен');
    setTimeout(initializeMatchingQuestions, 200);
});

// Глобальное хранилище соединений для всех контейнеров
window.containerConnections = {};

/**
 * Инициализирует вопросы на сопоставление на странице
 */
function initializeMatchingQuestions() {
    const matchingContainers = document.querySelectorAll('.matching-container');
    
    matchingContainers.forEach(container => {
        const questionId = container.id.split('_')[1];
        // Инициализируем хранилище для этого вопроса
        window.containerConnections[questionId] = {};
        
        const canvas = container.querySelector(`#matching-canvas-${questionId}`);
        if (!canvas) {
            console.error(`Canvas not found for question ${questionId}`);
            return;
        }

        const ctx = canvas.getContext('2d');
        const leftPoints = container.querySelectorAll('.left-point');
        const rightPoints = container.querySelectorAll('.right-point');
        const hiddenInputsContainer = document.getElementById(`matching_inputs_${questionId}`);
        const connectionCounter = document.getElementById(`connection-count-${questionId}`);
        
        function resizeCanvas() {
            const matchingArea = container.querySelector('.matching-area');
            if (matchingArea) {
                const rect = matchingArea.getBoundingClientRect();
                canvas.width = rect.width;
                canvas.height = rect.height;
                redrawConnections(); // Перерисовываем соединения после изменения размера
            }
        }
        
        // Вызываем resize сразу и при изменении размера окна
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        function handleConnectionPointClick(e) {
            e.preventDefault(); // Предотвращаем возможные побочные эффекты
            const point = e.currentTarget;
            
            // Проверяем, является ли точка уже активной
            if (point.classList.contains('active')) {
                point.classList.remove('active');
                return;
            }
            
            const isLeft = point.classList.contains('left-point');
            const pointId = point.dataset.id;
            
            // Находим активную точку противоположной стороны
            const activeOppositePoint = isLeft 
                ? container.querySelector('.right-point.active')
                : container.querySelector('.left-point.active');
            
            // Убираем активное состояние со всех точек той же стороны
            const samePoints = isLeft ? leftPoints : rightPoints;
            samePoints.forEach(p => p.classList.remove('active'));
            
            // Добавляем активное состояние текущей точке
            point.classList.add('active');
            
            // Если есть активная точка с противоположной стороны, создаем соединение
            if (activeOppositePoint) {
                if (isLeft) {
                    createConnection(pointId, activeOppositePoint.dataset.id);
                } else {
                    createConnection(activeOppositePoint.dataset.id, pointId);
                }
                // Убираем активное состояние после создания соединения
                point.classList.remove('active');
                activeOppositePoint.classList.remove('active');
            }
        }
        
        function createConnection(leftId, rightId) {
            // Используем глобальное хранилище
            const connections = window.containerConnections[questionId];
            
            // Удаляем существующие соединения
            Object.keys(connections).forEach(key => {
                if (key === leftId || connections[key] === rightId) {
                    const oldLeftPoint = container.querySelector(`.left-point[data-id="${key}"]`);
                    const oldRightPoint = container.querySelector(`.right-point[data-id="${connections[key]}"]`);
                    
                    if (oldLeftPoint) oldLeftPoint.classList.remove('connected');
                    if (oldRightPoint) oldRightPoint.classList.remove('connected');
                    
                    delete connections[key];
                }
            });
            
            // Создаем новое соединение
            connections[leftId] = rightId;
            
            // Обновляем визуальное состояние точек
            const leftPoint = container.querySelector(`.left-point[data-id="${leftId}"]`);
            const rightPoint = container.querySelector(`.right-point[data-id="${rightId}"]`);
            
            if (leftPoint) leftPoint.classList.add('connected');
            if (rightPoint) rightPoint.classList.add('connected');
            
            // Обновляем отображение
            updateHiddenInputs();
            redrawConnections();
            
            // Добавляем отладочный вывод
            console.log('Создано соединение:', {
                leftId,
                rightId,
                connections,
                hiddenInputs: Array.from(hiddenInputsContainer.querySelectorAll('input')).map(i => ({
                    name: i.name,
                    value: i.value
                }))
            });
        }
        
        function updateHiddenInputs() {
            // Используем глобальное хранилище
            const connections = window.containerConnections[questionId];
            
            console.log("Обновление скрытых полей для сопоставлений");
            
            // Получаем все левые элементы
            const leftItems = container.querySelectorAll('.left-item');
            
            leftItems.forEach((leftItem, index) => {
                const leftValue = leftItem.dataset.value;
                const leftId = leftItem.dataset.id;
                
                // Находим соответствующее правое значение
                let rightValue = '';
                if (connections[leftId]) {
                    const rightItem = container.querySelector(`.right-item[data-id="${connections[leftId]}"]`);
                    if (rightItem) {
                        rightValue = rightItem.dataset.value;
                    }
                }
                
                // Обновляем скрытые поля
                const leftInput = document.getElementById(`left_${questionId}_${index}`);
                const rightInput = document.getElementById(`match_${questionId}_${index}`);
                
                if (leftInput && rightInput) {
                    leftInput.value = leftValue;
                    rightInput.value = rightValue;
                    console.log(`Обновлена пара ${index}:`, {
                        left: leftValue,
                        right: rightValue
                    });
                }
            });
            
            // Обновляем счетчик соединений
            if (connectionCounter) {
                const count = Object.keys(connections).length;
                connectionCounter.textContent = count;
                console.log(`Обновлен счетчик соединений: ${count}`);
            }
        }
        
        function redrawConnections() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const canvasRect = canvas.getBoundingClientRect();
            
            // Используем глобальное хранилище
            const connections = window.containerConnections[questionId];
            
            for (const leftId in connections) {
                const rightId = connections[leftId];
                const leftPoint = container.querySelector(`.left-point[data-id="${leftId}"]`);
                const rightPoint = container.querySelector(`.right-point[data-id="${rightId}"]`);
                
                if (leftPoint && rightPoint) {
                    const leftRect = leftPoint.getBoundingClientRect();
                    const rightRect = rightPoint.getBoundingClientRect();
                    
                    // Корректируем координаты для точного попадания в точки соединения
                    const x1 = leftRect.right - canvasRect.left;
                    const y1 = leftRect.top + leftRect.height/2 - canvasRect.top;
                    const x2 = rightRect.left - canvasRect.left;
                    const y2 = rightRect.top + rightRect.height/2 - canvasRect.top;
                    
                    // Рисуем прямую линию между точками
                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    
                    // Используем более плавную кривую
                    const midX = (x1 + x2) / 2;
                    const cp1x = midX;
                    const cp1y = y1;
                    const cp2x = midX;
                    const cp2y = y2;
                    
                    ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x2, y2);
                    
                    // Настраиваем стиль линии
                    ctx.strokeStyle = leftPoint.classList.contains('connected') ? '#4CAF50' : '#9D4EDD';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }
            }
        }
        
        // Добавляем обработчики событий для точек
        leftPoints.forEach(point => {
            point.addEventListener('click', handleConnectionPointClick);
        });
        
        rightPoints.forEach(point => {
            point.addEventListener('click', handleConnectionPointClick);
        });
        
        // Обработчик для кнопки сброса
        const resetBtn = container.querySelector('.reset-connections-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => resetConnections(container.id));
        }
    });
}

/**
 * Сбрасывает все соединения для указанного контейнера
 */
function resetConnections(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error('Container not found:', containerId);
        return;
    }
    
    const questionId = containerId.split('_')[1];
    console.log('Resetting connections for question:', questionId);
    
    try {
        // Очищаем соединения в глобальном хранилище
        window.containerConnections[questionId] = {};
        
        // Очищаем canvas
        const canvas = container.querySelector(`#matching-canvas-${questionId}`);
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        
        // Убираем все классы connected и active
        container.querySelectorAll('.connection-point').forEach(point => {
            point.classList.remove('connected', 'active');
        });
        
        // Сбрасываем скрытые поля
        const hiddenInputsContainer = document.getElementById(`matching_inputs_${questionId}`);
        if (hiddenInputsContainer) {
            hiddenInputsContainer.querySelectorAll('input[id^="match_"]').forEach(input => {
                input.value = '';
            });
        }
        
        // Обновляем счетчик соединений
        const counter = document.getElementById(`connection-count-${questionId}`);
        if (counter) {
            counter.textContent = '0';
        }
        
        console.log('Successfully reset connections for question:', questionId);
        
    } catch (error) {
        console.error('Error resetting connections:', error);
    }
}

// Заменяем обработчик отправки формы
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('test-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Обновляем все matching контейнеры перед отправкой
            document.querySelectorAll('.matching-container').forEach(container => {
                const questionId = container.id.split('_')[1];
                const hiddenInputsContainer = document.getElementById(`matching_inputs_${questionId}`);
                const connections = window.containerConnections[questionId] || {};
                
                if (hiddenInputsContainer) {
                    // Очищаем существующие скрытые поля
                    hiddenInputsContainer.innerHTML = '';
                    
                    // Добавляем главное поле
                    const mainInput = document.createElement('input');
                    mainInput.type = 'hidden';
                    mainInput.name = `question_${questionId}`;
                    mainInput.value = 'matched';
                    hiddenInputsContainer.appendChild(mainInput);
                    
                    // Получаем все левые элементы
                    const leftItems = container.querySelectorAll('.left-item');
                    leftItems.forEach((leftItem, index) => {
                        const leftId = leftItem.dataset.id;
                        const leftValue = leftItem.dataset.value;
                        
                        // Находим соответствующее правое значение
                        let rightValue = '';
                        if (connections[leftId]) {
                            const rightItem = container.querySelector(`.right-item[data-id="${connections[leftId]}"]`);
                            if (rightItem) {
                                rightValue = rightItem.dataset.value;
                            }
                        }
                        
                        // Создаем скрытые поля для пары
                        const leftInput = document.createElement('input');
                        leftInput.type = 'hidden';
                        leftInput.name = `question_${questionId}_left_${index}`;
                        leftInput.value = leftValue;
                        hiddenInputsContainer.appendChild(leftInput);
                        
                        // Создаем поле для сопоставления в формате "leftValue:rightValue"
                        const matchInput = document.createElement('input');
                        matchInput.type = 'hidden';
                        matchInput.name = `question_${questionId}_match_${index}`;
                        matchInput.value = rightValue ? `${leftValue}:${rightValue}` : '';
                        hiddenInputsContainer.appendChild(matchInput);
                        
                        console.log(`Отправка пары ${index}:`, {
                            left: leftValue,
                            right: rightValue,
                            match: matchInput.value
                        });
                    });
                }
            });
            
            // Выводим отладочную информацию перед отправкой
            const formData = new FormData(form);
            const formDataObj = {};
            formData.forEach((value, key) => {
                formDataObj[key] = value;
            });
            console.log('Отправляемые данные формы:', formDataObj);
            
            // Отправляем форму
            form.submit();
        });
    }
});

// Добавляем функцию валидации формы
function validateForm() {
    const matchingContainers = document.querySelectorAll('.matching-container');
    let isValid = true;
    let hasUnconnectedItems = false;
    
    matchingContainers.forEach(container => {
        const questionId = container.id.split('_')[1];
        const connections = window.containerConnections[questionId] || {};
        const leftItems = container.querySelectorAll('.left-item');
        
        // Проверяем, все ли элементы соединены
        if (Object.keys(connections).length < leftItems.length) {
            hasUnconnectedItems = true;
            console.warn(`Не все элементы соединены в вопросе ${questionId}`);
            container.classList.add('warning');
        }
    });
    
    if (hasUnconnectedItems) {
        if (!confirm('Некоторые элементы не соединены. Вы уверены, что хотите продолжить?')) {
            isValid = false;
        }
    }
    
    return isValid;
}

// Добавляем обработчики для кнопок сброса при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки сброса и добавляем обработчики
    document.querySelectorAll('.reset-connections-btn').forEach(button => {
        button.addEventListener('click', function() {
            const containerId = `matching_${this.dataset.questionId}`;
            resetConnections(containerId);
        });
    });
}); 