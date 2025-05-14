-- Удаляем существующее ограничение внешнего ключа
IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK__Questions__ID_Te__6383C8BA')
    ALTER TABLE QuestionsTests DROP CONSTRAINT FK__Questions__ID_Te__6383C8BA;

-- Добавляем новое ограничение с каскадным удалением
ALTER TABLE QuestionsTests
ADD CONSTRAINT FK_QuestionsTests_Tests
FOREIGN KEY (ID_Test) REFERENCES Tests(ID_Test)
ON DELETE CASCADE; 