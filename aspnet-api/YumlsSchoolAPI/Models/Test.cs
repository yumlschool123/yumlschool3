using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class Test
{
    public int? IdTest { get; set; }

    public string? NameTest { get; set; } = null!;

    public string? DescriptionTest { get; set; }

    public DateOnly? DateUploadTest { get; set; }

    public TimeOnly? TimeUploadTest { get; set; }

    public int? TimeLimit { get; set; }

    public int? SubjectId { get; set; }

    public int? UserId { get; set; }

}
