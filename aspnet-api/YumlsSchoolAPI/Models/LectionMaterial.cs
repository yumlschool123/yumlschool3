using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class LectionMaterial
{
    public int? IdLectionMaterial { get; set; }

    public string? NameLectionMaterial { get; set; }

    public string? DescriptionLectionMaterial { get; set; }

    public DateOnly? DateUploadLectionMaterial { get; set; }

    public TimeOnly? TimeUploadLectionMaterial { get; set; }

    public string? NameFileLection { get; set; }

    public string? UrlFileLection { get; set; }

    public int? UserId { get; set; }

    public int? SubjectId { get; set; }
}
