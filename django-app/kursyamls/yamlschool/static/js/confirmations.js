/**
 * Confirmation dialog system for the system
 * Adds confirmation dialogs to various actions like delete, edit, and form submissions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Confirm form submissions
    addConfirmationToForms();

    // Confirm delete actions
    addConfirmationToDeleteButtons();

    // Confirm edit actions for sensitive items
    addConfirmationToEditButtons();
    
    // Обработка форм удаления для предметов (subjects)
    setupSubjectDeleteForms();
});

/**
 * Add confirmation dialogs to forms with data-confirm attribute
 */
function addConfirmationToForms() {
    const forms = document.querySelectorAll('form[data-confirm]');
    
    forms.forEach(form => {
        // Проверяем, что обработчик ещё не был установлен
        if (form.hasAttribute('data-confirm-handler-set') || form.hasAttribute('data-custom-handler')) {
            return;
        }
        
        form.setAttribute('data-confirm-handler-set', 'true');
        form.addEventListener('submit', function(e) {
            const message = this.dataset.confirm || 'Вы уверены, что хотите выполнить это действие?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
            return true;
        });
    });
}

/**
 * Add confirmation to all delete buttons and forms
 */
function addConfirmationToDeleteButtons() {
    // For buttons with delete/удалить in their text
    const deleteButtons = document.querySelectorAll('button, a.btn, input[type="submit"]');
    
    deleteButtons.forEach(button => {
        // Проверяем, находится ли кнопка внутри формы, которая уже имеет атрибут data-confirm
        const parentForm = button.closest('form[data-confirm]');
        if (parentForm) {
            // Если кнопка находится внутри формы с data-confirm, пропускаем её
            return;
        }
        
        // Проверяем, находится ли кнопка внутри формы с уже установленным обработчиком
        const parentFormWithHandler = button.closest('form[data-confirm-handler-set], form[data-custom-handler]');
        if (parentFormWithHandler) {
            // Если кнопка находится внутри формы с обработчиком, пропускаем её
            return;
        }

        const buttonText = button.textContent.toLowerCase();
        if (buttonText.includes('удал') || buttonText.includes('delet') || buttonText.includes('remov')) {
            if (!button.hasAttribute('data-confirm-handler-set')) {
                button.setAttribute('data-confirm-handler-set', 'true');
                
                button.addEventListener('click', function(e) {
                    if (!confirm('Вы уверены, что хотите удалить этот элемент? Это действие нельзя отменить.')) {
                        e.preventDefault();
                        return false;
                    }
                    return true;
                });
            }
        }
    });
    
    // For forms with action containing delete/удалить
    const deleteForms = document.querySelectorAll('form');
    
    deleteForms.forEach(form => {
        // Пропускаем формы, у которых уже есть атрибут data-confirm
        if (form.hasAttribute('data-confirm')) {
            return;
        }

        // Проверяем, что обработчик ещё не был установлен
        if (form.hasAttribute('data-confirm-handler-set') || form.hasAttribute('data-custom-handler')) {
            return;
        }
        
        // Пропускаем если это форма удаления пользователя или предмета с кастомным обработчиком
        if (form.classList.contains('delete-user-form') || form.classList.contains('delete-subject-form')) {
            return;
        }
        
        const action = form.getAttribute('action') || '';
        if (action.toLowerCase().includes('delete') || action.toLowerCase().includes('удал')) {
            form.setAttribute('data-confirm-handler-set', 'true');
            
            form.addEventListener('submit', function(e) {
                if (!confirm('Вы уверены, что хотите удалить этот элемент? Это действие нельзя отменить.')) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });
        }
    });
}

/**
 * Add confirmation to edit buttons for sensitive areas
 */
function addConfirmationToEditButtons() {
    // Edit buttons in admin panels or sensitive areas
    const editButtons = document.querySelectorAll('.admin-panel button, .admin-panel a.btn, .admin-panel input[type="submit"]');
    
    editButtons.forEach(button => {
        // Проверяем, что кнопка не находится внутри формы с уже установленным обработчиком
        const parentForm = button.closest('form');
        if (parentForm && (parentForm.hasAttribute('data-confirm-handler-set') || parentForm.hasAttribute('data-custom-handler'))) {
            return;
        }
        
        const buttonText = button.textContent.toLowerCase();
        if ((buttonText.includes('измен') || buttonText.includes('редакт') || buttonText.includes('edit')) && 
            !button.hasAttribute('data-confirm-handler-set')) {
            
            button.setAttribute('data-confirm-handler-set', 'true');
            
            button.addEventListener('click', function(e) {
                if (!confirm('Вы уверены, что хотите изменить этот элемент?')) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });
        }
    });
}

/**
 * Helper to add confirmation to specific elements
 * @param {string} selector - CSS selector for elements 
 * @param {string} message - Confirmation message
 */
function addConfirmationTo(selector, message) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        if (!element.hasAttribute('data-confirm-handler-set') && !element.hasAttribute('data-custom-handler')) {
            element.setAttribute('data-confirm-handler-set', 'true');
            
            element.addEventListener('click', function(e) {
                if (!confirm(message)) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });
        }
    });
} 

/**
 * Настраивает обработчики для форм удаления предметов
 */
function setupSubjectDeleteForms() {
    const deleteForms = document.querySelectorAll('.delete-subject-form');
    
    deleteForms.forEach(form => {
        // Пропускаем, если у формы уже есть обработчик 
        if (form.hasAttribute('data-custom-handler')) {
            return;
        }
        
        form.setAttribute('data-custom-handler', 'true');
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (confirm('Вы уверены, что хотите удалить этот предмет? Это действие нельзя отменить.')) {
                this.submit();
            }
        });
    });
} 