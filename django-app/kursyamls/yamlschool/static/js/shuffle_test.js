document.addEventListener('DOMContentLoaded', function() {
    console.log('Скрипт shuffle_test.js загружен');
    
    // Функция для перемешивания массива (алгоритм Фишера-Йейтса)
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
    
    // Получаем контейнер с вопросами
    const questionsContainer = document.querySelector('.questions');
    console.log('Контейнер вопросов найден?', !!questionsContainer);
    
    if (!questionsContainer) {
        console.error('Контейнер с классом .questions не найден!');
        return;
    }
    
    // Получаем все карточки с вопросами
    const questionCards = Array.from(questionsContainer.querySelectorAll('.question-card'));
    console.log('Найдено карточек вопросов:', questionCards.length);
    
    if (questionCards.length === 0) {
        console.error('Не найдены элементы с классом .question-card внутри .questions!');
        return;
    }
    
    // Перемешиваем вопросы
    const shuffledQuestions = shuffleArray([...questionCards]);
    
    // Очищаем контейнер с вопросами
    questionsContainer.innerHTML = '';
    
    // Добавляем вопросы в перемешанном порядке
    shuffledQuestions.forEach((question, index) => {
        // Обновляем номер вопроса, если это необходимо
        const questionHeader = question.querySelector('h3');
        if (questionHeader) {
            questionHeader.textContent = `Вопрос ${index + 1}`;
        }
        
        // Добавляем вопрос обратно в контейнер
        questionsContainer.appendChild(question);
    });
    
    console.log('Вопросы были успешно перемешаны');
    
    // Перемешиваем варианты ответов для каждого вопроса
    shuffledQuestions.forEach(card => {
        // Для вопросов с одним ответом
        const radioOptions = Array.from(card.querySelectorAll('.answer-option input[type="radio"]'));
        if (radioOptions.length > 0) {
            const optionsContainer = radioOptions[0].closest('div').parentNode;
            const options = Array.from(optionsContainer.querySelectorAll('.answer-option'));
            
            // Сохраняем оригинальный контейнер
            const originalParent = options[0].parentNode;
            
            // Удаляем все варианты ответов
            options.forEach(option => option.remove());
            
            // Перемешиваем и добавляем обратно
            shuffleArray([...options]).forEach(option => {
                originalParent.appendChild(option);
            });
            
            console.log(`Перемешано ${options.length} вариантов ответа с радиокнопками`);
        }
        
        // Для вопросов с множественным выбором
        const checkboxOptions = Array.from(card.querySelectorAll('.answer-option input[type="checkbox"]'));
        if (checkboxOptions.length > 0) {
            const optionsContainer = checkboxOptions[0].closest('div').parentNode;
            const options = Array.from(optionsContainer.querySelectorAll('.answer-option'));
            
            // Сохраняем оригинальный контейнер
            const originalParent = options[0].parentNode;
            
            // Удаляем все варианты ответов
            options.forEach(option => option.remove());
            
            // Перемешиваем и добавляем обратно
            shuffleArray([...options]).forEach(option => {
                originalParent.appendChild(option);
            });
            
            console.log(`Перемешано ${options.length} вариантов ответа с чекбоксами`);
        }
        
        // Обрабатываем вопросы на сопоставление
        const matchingContainer = card.querySelector('.matching-container');
        if (matchingContainer) {
            // Перемешиваем только правую колонку
            const rightColumn = matchingContainer.querySelector('.matching-right-column');
            if (rightColumn) {
                const rightItems = Array.from(rightColumn.querySelectorAll('.right-item'));
                
                // Удаляем все элементы из правой колонки
                rightItems.forEach(item => item.remove());
                
                // Перемешиваем и добавляем обратно
                shuffleArray([...rightItems]).forEach(item => {
                    rightColumn.appendChild(item);
                });
                
                console.log(`Перемешано ${rightItems.length} элементов в правой колонке сопоставления`);
            }
        }
        
        // Обрабатываем вопросы на упорядочивание
        const orderContainer = card.querySelector('.order-container');
        if (orderContainer) {
            const itemsContainer = orderContainer.querySelector('.order-items-container');
            if (itemsContainer) {
                const orderItems = Array.from(itemsContainer.querySelectorAll('.order-item'));
                
                // Удаляем все элементы
                orderItems.forEach(item => item.remove());
                
                // Перемешиваем и добавляем обратно
                shuffleArray([...orderItems]).forEach((item, index) => {
                    // Обновляем номер элемента
                    const orderNumber = item.querySelector('.order-number');
                    if (orderNumber) {
                        orderNumber.textContent = index + 1;
                    }
                    itemsContainer.appendChild(item);
                });
                
                console.log(`Перемешано ${orderItems.length} элементов в задании на упорядочивание`);
            }
        }
    });
    
    console.log('Перемешивание вопросов и ответов завершено!');
}); 