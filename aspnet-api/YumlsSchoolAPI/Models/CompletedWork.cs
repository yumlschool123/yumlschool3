using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class CompletedWork
{
    public int? IdCompletedWork { get; set; }

    public DateOnly? DateUploadCompletedWork { get; set; }

    public TimeOnly? TimeUploadCompletedWork { get; set; }

    public string? NameFileCompletedWork { get; set; }

    public string? UrlFileCompletedWork { get; set; }

    public string? Grade { get; set; }

    public int? UserId { get; set; }

    public int? PracticalWorkId { get; set; }

    public int? StatusId { get; set; }

    public int? AttemptCount { get; set; }
}
