using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class GradingCriterion
{
    public int? IdCriteria { get; set; }

    public int? IdTest { get; set; }

    public int? Grade { get; set; }

    public int? MinPoints { get; set; }

    public int? MaxPoints { get; set; }
}
