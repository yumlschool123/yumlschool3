
USE [yumlsschooldb]
GO
/****** Object:  Table [dbo].[CompletedWork]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CompletedWork](
  [ID_CompletedWork] [int] IDENTITY(1,1) NOT NULL,
  [DateUpload_CompletedWork] [date] NULL,
  [TimeUpload_CompletedWork] [time](7) NULL,
  [Name_FileCompletedWork] [nvarchar](64) NOT NULL,
  [URL_FileCompletedWork] [nvarchar](3000) NOT NULL,
  [Grade] [nvarchar](64) NOT NULL,
  [User_ID] [int] NULL,
  [PracticalWork_ID] [int] NULL,
  [Status_ID] [int] NULL,
  [AttemptCount] [int] NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_CompletedWork] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[GradingCriteria]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[GradingCriteria](
  [ID_Criteria] [int] IDENTITY(1,1) NOT NULL,
  [ID_Test] [int] NOT NULL,
  [Grade] [int] NOT NULL,
  [Min_Points] [int] NOT NULL,
  [Max_Points] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Criteria] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Group]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Group](
  [ID_Group] [int] IDENTITY(1,1) NOT NULL,
  [Name_Group] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Group] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LectionMaterial]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LectionMaterial](
  [ID_LectionMaterial] [int] IDENTITY(1,1) NOT NULL,
  [Name_LectionMaterial] [nvarchar](64) NOT NULL,
  [Description_LectionMaterial] [nvarchar](1024) NOT NULL,
  [DateUpload_LectionMaterial] [date] NULL,
  [TimeUpload_LectionMaterial] [time](7) NULL,
  [Name_FileLection] [nvarchar](64) NOT NULL,
  [URL_FileLection] [nvarchar](1024) NOT NULL,
  [User_ID] [int] NULL,
  [Subject_ID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_LectionMaterial] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PracticalWork]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PracticalWork](
  [ID_PracticalWork] [int] IDENTITY(1,1) NOT NULL,
  [Name_PracticalWork] [nvarchar](64) NOT NULL,
  [Description_PracticalWork] [nvarchar](3000) NOT NULL,
  [DateUpload_PracticalWork] [date] NULL,
  [TimeUpload_PracticalWork] [time](7) NULL,
  [Name_FilePracticalWork] [nvarchar](64) NOT NULL,
  [URL_FilePracticalWork] [nvarchar](3000) NOT NULL,
  [User_ID] [int] NULL,
  [Subject_ID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_PracticalWork] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[QuestionsTests]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[QuestionsTests](
  [ID_Question] [int] IDENTITY(1,1) NOT NULL,
  [Question_Text] [nvarchar](1000) NOT NULL,
  [QuestionType] [int] NOT NULL,
  [AnswerVariants] [nvarchar](max) NOT NULL,
  [CorrectAnswer] [nvarchar](max) NOT NULL,
  [Points] [int] NULL,
  [ID_Test] [int] NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Question] ASC

)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Role]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Role](
  [ID_Role] [int] IDENTITY(1,1) NOT NULL,
  [Role_Name] [nvarchar](30) NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Role] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Status]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Status](
  [ID_Status] [int] IDENTITY(1,1) NOT NULL,
  [Name_Status] [nvarchar](64) NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Status] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Subject]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Subject](
  [ID_Subject] [int] IDENTITY(1,1) NOT NULL,
  [Name_Subject] [nvarchar](64) NOT NULL,
  [ID_Group] [int] NOT NULL,
  [User_ID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Subject] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TestAttempt]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TestAttempt](
  [ID_TestAttempt] [int] IDENTITY(1,1) NOT NULL,
  [Test_ID] [int] NOT NULL,
  [User_ID] [int] NOT NULL,
  [Start_Time] [datetime] NOT NULL,
  [End_Time] [datetime] NULL,
  [Status] [nvarchar](20) NOT NULL,
  [Score] [int] NOT NULL,
  [Grade] [decimal](3, 1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_TestAttempt] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tests]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tests](
  [ID_Test] [int] IDENTITY(1,1) NOT NULL,
  [Name_Test] [nvarchar](255) NOT NULL,
  [Description_Test] [nvarchar](1000) NULL,
  [DateUpload_Test] [date] NULL,
  [TimeUpload_Test] [time](7) NULL,
  [TimeLimit] [int] NULL,
  [Subject_ID] [int] NULL,
  [User_ID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_Test] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[User]    Script Date: 20.03.2025 19:12:47 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[User](
  [ID_User] [int] IDENTITY(1,1) NOT NULL,
  [FirstName] [nvarchar](64) NOT NULL,
  [SecondName] [nvarchar](64) NOT NULL,
  [MiddleName] [nvarchar](64) NULL,
  [Email] [nvarchar](255) NOT NULL,
  [ID_Role] [int] NOT NULL,
  [ID_Group] [int] NOT NULL,
  [Login] [nvarchar](150) NOT NULL,
  [Password] [nvarchar](150) NOT NULL,
PRIMARY KEY CLUSTERED 
(
  [ID_User] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
  [Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

GO

ALTER TABLE [dbo].[CompletedWork] ADD  DEFAULT (CONVERT([time],getdate())) FOR [TimeUpload_CompletedWork]
GO
ALTER TABLE [dbo].[LectionMaterial] ADD  DEFAULT (CONVERT([date],getdate())) FOR [DateUpload_LectionMaterial]
GO
ALTER TABLE [dbo].[LectionMaterial] ADD  DEFAULT (CONVERT([time],getdate())) FOR [TimeUpload_LectionMaterial]
GO
ALTER TABLE [dbo].[PracticalWork] ADD  DEFAULT (CONVERT([date],getdate())) FOR [DateUpload_PracticalWork]
GO
ALTER TABLE [dbo].[PracticalWork] ADD  DEFAULT (CONVERT([time],getdate())) FOR [TimeUpload_PracticalWork]
GO
ALTER TABLE [dbo].[QuestionsTests] ADD  DEFAULT ((1)) FOR [Points]
GO
ALTER TABLE [dbo].[TestAttempt] ADD  DEFAULT (getdate()) FOR [Start_Time]
GO
ALTER TABLE [dbo].[TestAttempt] ADD  DEFAULT ((0)) FOR [Score]
GO
ALTER TABLE [dbo].[TestAttempt] ADD  DEFAULT ((0)) FOR [Grade]
GO
ALTER TABLE [dbo].[Tests] ADD  DEFAULT (CONVERT([date],getdate())) FOR [DateUpload_Test]
GO
ALTER TABLE [dbo].[Tests] ADD  DEFAULT (CONVERT([time],getdate())) FOR [TimeUpload_Test]
GO
ALTER TABLE [dbo].[User] ADD  DEFAULT ('Отсутствует') FOR [MiddleName]
GO
ALTER TABLE [dbo].[CompletedWork]  WITH CHECK ADD FOREIGN KEY([PracticalWork_ID])
REFERENCES [dbo].[PracticalWork] ([ID_PracticalWork])
GO
ALTER TABLE [dbo].[CompletedWork]  WITH CHECK ADD FOREIGN KEY([Status_ID])
REFERENCES [dbo].[Status] ([ID_Status])
GO
ALTER TABLE [dbo].[CompletedWork]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[GradingCriteria]  WITH CHECK ADD  CONSTRAINT [FK_GradingCriteria_Tests] FOREIGN KEY([ID_Test])
REFERENCES [dbo].[Tests] ([ID_Test])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[GradingCriteria] CHECK CONSTRAINT [FK_GradingCriteria_Tests]
GO
ALTER TABLE [dbo].[LectionMaterial]  WITH CHECK ADD FOREIGN KEY([Subject_ID])
REFERENCES [dbo].[Subject] ([ID_Subject])
GO
ALTER TABLE [dbo].[LectionMaterial]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[PracticalWork]  WITH CHECK ADD FOREIGN KEY([Subject_ID])
REFERENCES [dbo].[Subject] ([ID_Subject])
GO
ALTER TABLE [dbo].[PracticalWork]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[QuestionsTests]  WITH CHECK ADD FOREIGN KEY([ID_Test])
REFERENCES [dbo].[Tests] ([ID_Test])
GO
ALTER TABLE [dbo].[Subject]  WITH CHECK ADD FOREIGN KEY([ID_Group])
REFERENCES [dbo].[Group] ([ID_Group])
GO
ALTER TABLE [dbo].[Subject]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[TestAttempt]  WITH CHECK ADD FOREIGN KEY([Test_ID])
REFERENCES [dbo].[Tests] ([ID_Test])
GO
ALTER TABLE [dbo].[TestAttempt]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[Tests]  WITH CHECK ADD FOREIGN KEY([Subject_ID])
REFERENCES [dbo].[Subject] ([ID_Subject])
GO
ALTER TABLE [dbo].[Tests]  WITH CHECK ADD FOREIGN KEY([User_ID])
REFERENCES [dbo].[User] ([ID_User])
GO
ALTER TABLE [dbo].[User]  WITH CHECK ADD FOREIGN KEY([ID_Group])
REFERENCES [dbo].[Group] ([ID_Group])
GO
ALTER TABLE [dbo].[User]  WITH CHECK ADD FOREIGN KEY([ID_Role])
REFERENCES [dbo].[Role] ([ID_Role])
GO
ALTER TABLE [dbo].[GradingCriteria]  WITH CHECK ADD  CONSTRAINT [CK_Grade] CHECK  (([Grade]=(5) OR [Grade]=(4) OR [Grade]=(3)))
GO
ALTER TABLE [dbo].[GradingCriteria] CHECK CONSTRAINT [CK_Grade]
GO
ALTER TABLE [dbo].[GradingCriteria]  WITH CHECK ADD  CONSTRAINT [CK_Points] CHECK  (([Min_Points]<=[Max_Points]))
GO
ALTER TABLE [dbo].[GradingCriteria] CHECK CONSTRAINT [CK_Points]
GO
ALTER TABLE [dbo].[TestAttempt]  WITH CHECK ADD CHECK  (([Status]='completed' OR [Status]='in_progress'))
GO
ALTER TABLE [dbo].[User]  WITH CHECK ADD CHECK  (([Email] like '%@%.%'))
GO



IF NOT EXISTS (SELECT 1 FROM [Group])
BEGIN
    INSERT INTO [Group] (Name_Group)
    VALUES 
        (N'Администрация'), 
        (N'Преподавательский состав'), 
        (N'ПИ-14-09'),
	(N'ПИ-14-10'),
	(N'ПИ-14-11'),
	(N'Пользователь без группы');
END;

IF NOT EXISTS (SELECT 1 FROM [Role])
BEGIN
    INSERT INTO [Role] (Role_Name)
    VALUES 
        (N'Администратор'), 
        (N'Преподаватель'), 
        (N'Студент'), 
        (N'Пользователь без роли'),
        (N'Заблокированный пользователь');
END;




