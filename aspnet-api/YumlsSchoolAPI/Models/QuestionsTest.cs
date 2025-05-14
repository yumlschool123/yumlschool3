using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class QuestionsTest
{
    public int? IdQuestion { get; set; }

    public string? QuestionText { get; set; }

    public int? QuestionType { get; set; }

    public string? AnswerVariants { get; set; }

    public string? CorrectAnswer { get; set; }

    public int? Points { get; set; }

    public int? IdTest { get; set; }

}
