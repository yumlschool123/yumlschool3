using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class TestAttempt
{
    public int? IdTestAttempt { get; set; }

    public int? TestId { get; set; }

    public int? UserId { get; set; }

    public DateTime StartTime { get; set; }

    public DateTime? EndTime { get; set; }

    public string? Status { get; set; } = null!;

    public int? Score { get; set; }

    public decimal? Grade { get; set; }
}
