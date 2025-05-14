using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class Subject
{
    public int? IdSubject { get; set; }

    public string? NameSubject { get; set; } = null!;

    public int? IdGroup { get; set; }

    public int? UserId { get; set; }
}
