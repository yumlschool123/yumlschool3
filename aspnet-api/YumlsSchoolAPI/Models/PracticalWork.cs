using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class PracticalWork
{
    public int? IdPracticalWork { get; set; }

    public string? NamePracticalWork { get; set; }

    public string? DescriptionPracticalWork { get; set; }

    public DateOnly? DateUploadPracticalWork { get; set; }

    public TimeOnly? TimeUploadPracticalWork { get; set; }

    public string? NameFilePracticalWork { get; set; }

    public string? UrlFilePracticalWork { get; set; }

    public int? UserId { get; set; }

    public int? SubjectId { get; set; }
}
