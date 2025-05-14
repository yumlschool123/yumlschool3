// Переработанная версия скрипта для вопросов на упорядочивание
document.addEventListener('DOMContentLoaded', function() {
    console.log('Улучшенный скрипт ordering.js загружен');
    
    // Инициализация с задержкой, чтобы избежать конфликтов с другими скриптами
    setTimeout(initOrderQuestions, 200);
});

// Глобальные переменные для drag-and-drop
let draggedItem = null;
let placeholder = null;

function initOrderQuestions() {
    console.log('Инициализация вопросов на упорядочивание');
    
    // Находим все контейнеры с вопросами на упорядочивание
    const orderContainers = document.querySelectorAll('.order-container');
    console.log(`Найдено ${orderContainers.length} контейнеров для вопросов на упорядочивание`);
    
    orderContainers.forEach(container => {
        const questionId = container.id.split('_')[1];
        console.log(`Настройка вопроса ID: ${questionId}`);
        
        // Находим контейнер с элементами
        const itemsContainer = container.querySelector('.order-items-container');
        if (!itemsContainer) {
            console.error('Не найден контейнер элементов для вопроса', questionId);
            return;
        }
        
        // Находим все элементы
        const items = itemsContainer.querySelectorAll('.order-item');
        console.log(`Найдено ${items.length} элементов для упорядочивания`);
        
        // Создаем контейнер для скрытых полей, если его нет
        const hiddenInputsContainer = document.getElementById(`order_inputs_${questionId}`);
        if (!hiddenInputsContainer) {
            console.error(`Контейнер для скрытых полей не найден: order_inputs_${questionId}`);
            return;
        }
        
        // Настраиваем каждый элемент
        items.forEach(item => {
            setupOrderItem(item, itemsContainer);
        });
        
        // Находим кнопку сброса или создаем ее
        const resetButton = container.querySelector('.reset-order-btn');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                resetOrder(itemsContainer);
                updateHiddenInputs(container);
            });
        }
        
        // Инициализируем обработчик для контейнера элементов
        itemsContainer.addEventListener('dragover', handleDragOver);
        itemsContainer.addEventListener('drop', handleDrop);
        
        // Инициализируем скрытые поля при загрузке
        updateHiddenInputs(container);
    });
    
    // Добавляем обработчик для всей формы
    const testForm = document.getElementById('test-form');
    if (testForm) {
        testForm.addEventListener('submit', function() {
            // Обновляем все скрытые поля перед отправкой
            document.querySelectorAll('.order-container').forEach(container => {
                updateHiddenInputs(container);
            });
            
            console.log('Форма отправляется, скрытые поля упорядочивания обновлены');
        });
    }
}

function setupOrderItem(item, container) {
    // Убираем существующие обработчики
    const newItem = item.cloneNode(true);
    item.parentNode.replaceChild(newItem, item);
    item = newItem;
    
    // Устанавливаем атрибут draggable
    item.setAttribute('draggable', true);
    
    // Обработчики событий для drag-and-drop
    item.addEventListener('dragstart', handleDragStart);
    item.addEventListener('dragend', handleDragEnd);
    
    // Обработчик для ручки перетаскивания
    const handle = item.querySelector('.order-handle');
    if (handle) {
        handle.addEventListener('mousedown', function(e) {
            e.preventDefault();
            item.focus();
        });
    }
    
    return item;
}

function handleDragStart(e) {
    // Запоминаем элемент
    draggedItem = this;
    
    // Добавляем класс для стилизации
    this.classList.add('dragging');
    
    // Создаем плейсхолдер
    placeholder = createPlaceholder(this);
    
    // Настраиваем данные для drag-and-drop
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', '');
    
    // Настраиваем изображение для перетаскивания
    const rect = this.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    const offsetY = e.clientY - rect.top;
    e.dataTransfer.setDragImage(this, offsetX, offsetY);
    
    // Добавляем обработчики для контейнера
    const container = this.parentNode;
    container.addEventListener('dragover', handleDragOver);
    container.addEventListener('drop', handleDrop);
    
    console.log('Начали перетаскивать элемент:', this.querySelector('.order-text').textContent.trim());
}

function handleDragEnd(e) {
    // Удаляем класс перетаскивания
    this.classList.remove('dragging');
    
    // Удаляем плейсхолдер
    if (placeholder && placeholder.parentNode) {
        placeholder.parentNode.removeChild(placeholder);
    }
    
    // Удаляем обработчики с контейнера
    const container = this.parentNode;
    container.removeEventListener('dragover', handleDragOver);
    container.removeEventListener('drop', handleDrop);
    
    // Обновляем скрытые поля
    const orderContainer = this.closest('.order-container');
    if (orderContainer) {
        updateHiddenInputs(orderContainer);
    }
    
    // Сбрасываем переменные
    draggedItem = null;
    placeholder = null;
    
    console.log('Перетаскивание завершено');
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    if (!draggedItem || !placeholder) return;
    
    // Находим все элементы, исключая плейсхолдер и перетаскиваемый элемент
    const items = Array.from(this.children).filter(item => 
        item !== placeholder && item !== draggedItem && item.classList.contains('order-item')
    );
    
    // Если нет других элементов, добавляем плейсхолдер в конец
    if (items.length === 0) {
        this.appendChild(placeholder);
        return;
    }
    
    // Находим ближайший элемент к курсору
    const mouseY = e.clientY;
    let closestItem = null;
    let closestDistance = Infinity;
    
    items.forEach(item => {
        const rect = item.getBoundingClientRect();
        const centerY = rect.top + rect.height / 2;
        const distance = Math.abs(mouseY - centerY);
        
        if (distance < closestDistance) {
            closestDistance = distance;
            closestItem = item;
        }
    });
    
    if (closestItem) {
        const rect = closestItem.getBoundingClientRect();
        const midY = rect.top + rect.height / 2;
        
        // Определяем, вставлять до или после ближайшего элемента
        if (mouseY < midY) {
            this.insertBefore(placeholder, closestItem);
        } else {
            this.insertBefore(placeholder, closestItem.nextSibling);
        }
    }
}

function handleDrop(e) {
    e.preventDefault();
    
    if (!draggedItem || !placeholder) return;
    
    // Вставляем перетаскиваемый элемент на место плейсхолдера
    if (placeholder.parentNode) {
        placeholder.parentNode.insertBefore(draggedItem, placeholder);
        placeholder.parentNode.removeChild(placeholder);
    }
    
    // Обновляем номера элементов
    updateOrderNumbers(this);
}

function createPlaceholder(item) {
    const placeholder = document.createElement('div');
    placeholder.className = 'order-item placeholder';
    placeholder.style.height = `${item.offsetHeight}px`;
    placeholder.style.margin = getComputedStyle(item).margin;
    return placeholder;
}

function updateOrderNumbers(container) {
    // Обновляем номера элементов
    const items = Array.from(container.querySelectorAll('.order-item')).filter(item => 
        !item.classList.contains('placeholder')
    );
    
    items.forEach((item, index) => {
        const orderNumber = item.querySelector('.order-number');
        if (orderNumber) {
            orderNumber.textContent = index + 1;
        }
    });
}

function updateHiddenInputs(container) {
    // Получаем ID вопроса
    const questionId = container.id.split('_')[1];
    if (!questionId) {
        console.error('Не найден ID вопроса в атрибуте id');
        // Выходим из функции, но не прерываем выполнение
        return;
    }
    
    const itemsContainer = container.querySelector('.order-items-container');
    const hiddenInputsContainer = document.getElementById(`order_inputs_${questionId}`);
    
    if (!itemsContainer || !hiddenInputsContainer) {
        console.error('Не найдены необходимые контейнеры для вопроса', questionId);
        return;
    }
    
    // Очищаем контейнер скрытых полей
    hiddenInputsContainer.innerHTML = '';
    
    // Получаем все элементы в текущем порядке
    const items = Array.from(itemsContainer.querySelectorAll('.order-item')).filter(item => 
        !item.classList.contains('placeholder')
    );
    
    if (items.length === 0) {
        console.warn(`Не найдены элементы для вопроса ${questionId}`);
        return;
    }
    
    // Создаем главное поле для отметки ответа на вопрос
    const mainInput = document.createElement('input');
    mainInput.type = 'hidden';
    mainInput.name = `question_${questionId}`;
    mainInput.value = 'ordered';
    hiddenInputsContainer.appendChild(mainInput);
    
    // Создаем скрытые поля для каждого элемента
    items.forEach((item, index) => {
        const value = item.dataset.value;
        if (!value) {
            console.warn(`Элемент не имеет атрибута data-value`, item);
            return;
        }
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = `question_${questionId}_order_${index}`;
        input.value = value;
        hiddenInputsContainer.appendChild(input);
        
        // Обновляем номера
        item.querySelector('.order-number').textContent = index + 1;
        
        console.log(`Добавлен элемент порядка [${index}]: ${value}`);
    });
    
    console.log(`Обновлены скрытые поля для вопроса ${questionId}: ${items.length} элементов`);
}

function resetOrder(container) {
    // Получаем все элементы
    const items = Array.from(container.querySelectorAll('.order-item')).filter(item => 
        !item.classList.contains('placeholder')
    );
    
    // Перемешиваем элементы
    for (let i = items.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [items[i], items[j]] = [items[j], items[i]];
    }
    
    // Удаляем элементы из контейнера
    items.forEach(item => {
        if (item.parentNode === container) {
            container.removeChild(item);
        }
    });
    
    // Добавляем элементы в перемешанном порядке
    items.forEach((item, index) => {
        container.appendChild(item);
        
        // Обновляем номер элемента
        const orderNumber = item.querySelector('.order-number');
        if (orderNumber) {
            orderNumber.textContent = index + 1;
        }
    });
    
    // Обновляем номера всех элементов
    updateOrderNumbers(container);
    
    console.log('Порядок элементов сброшен');
} 