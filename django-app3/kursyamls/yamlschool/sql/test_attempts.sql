-- Добавление столбца gradingCriteria в таблицу Tests
ALTER TABLE Tests
ADD COLUMN gradingCriteria NVARCHAR(MAX);

-- Добавление столбца Grading_Criteria в таблицу Tests
ALTER TABLE Tests
ADD Grading_Criteria VARCHAR(1000) NULL;

-- Создание таблицы Test
CREATE TABLE Test
(
    ID_Test INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name_Test VARCHAR(64) NOT NULL,
    Description_Test VARCHAR(3000) NOT NULL,
    DateUpload_Test DATE NULL DEFAULT(CONVERT(DATE,GETDATE()),
    TimeLimit INT NOT NULL,
    Grading_Criteria VARCHAR(1000) NULL,
    User_ID INT NULL FOREIGN KEY REFERENCES [User](ID_User),
    Subject_ID INT NULL FOREIGN KEY REFERENCES Subject(ID_Subject)
);

-- Создание таблицы TestAttempt
CREATE TABLE TestAttempt
(
    ID_TestAttempt INT PRIMARY KEY IDENTITY(1,1),
    Test_ID INT NOT NULL FOREIGN KEY REFERENCES Tests(ID_Test),
    User_ID INT NOT NULL FOREIGN KEY REFERENCES [User](ID_User),
    Start_Time DATETIME NOT NULL DEFAULT(GETDATE()),
    End_Time DATETIME NULL,
    Status VARCHAR(20) NOT NULL CHECK (Status IN ('in_progress', 'completed')),
    Score INT NOT NULL DEFAULT 0,
    Grade DECIMAL(3,1) NOT NULL DEFAULT 0
);

-- Создание индексов для оптимизации запросов
CREATE INDEX IX_TestAttempt_Test_ID ON TestAttempt(Test_ID);
CREATE INDEX IX_TestAttempt_User_ID ON TestAttempt(User_ID);
CREATE INDEX IX_TestAttempt_Status ON TestAttempt(Status);

-- Добавление комментариев к таблице и столбцам
EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Таблица для хранения попыток прохождения тестов студентами',
    @level0type = N'SCHEMA',
    @level0name = N'dbo',
    @level1type = N'TABLE',
    @level1name = N'TestAttempts';

EXEC sp_addextendedproperty 
    @name = N'MS_Description',
    @value = N'Критерии оценивания теста',
    @level0type = N'SCHEMA',
    @level0name = N'dbo',
    @level1type = N'TABLE',
    @level1name = N'Tests',
    @level2type = N'COLUMN',
    @level2name = N'gradingCriteria';

-- Удаляем старый столбец с критериями оценивания
ALTER TABLE Tests
DROP COLUMN Grading_Criteria;

-- Создаем таблицу для критериев оценивания
CREATE TABLE GradingCriteria (
    ID_Criteria INT PRIMARY KEY IDENTITY(1,1),
    ID_Test INT NOT NULL,
    Grade INT NOT NULL,  -- Оценка (3, 4 или 5)
    Min_Points INT NOT NULL,  -- Минимальное количество баллов
    Max_Points INT NOT NULL,  -- Максимальное количество баллов
    CONSTRAINT FK_GradingCriteria_Tests FOREIGN KEY (ID_Test) REFERENCES Tests(ID_Test) ON DELETE CASCADE,
    CONSTRAINT CK_Grade CHECK (Grade IN (3, 4, 5)),
    CONSTRAINT CK_Points CHECK (Min_Points <= Max_Points)
);

-- Создаем индекс для быстрого поиска критериев по тесту
CREATE INDEX IX_GradingCriteria_Test_ID ON GradingCriteria(ID_Test); 