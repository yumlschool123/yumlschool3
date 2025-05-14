using System;
using System.Collections.Generic;

namespace YumlsSchoolAPI.Models;

public partial class User
{
    public int? IdUser { get; set; }

    public string? FirstName { get; set; }

    public string? SecondName { get; set; }

    public string? MiddleName { get; set; }

    public string? Email { get; set; }

    public int? IdRole { get; set; }

    public int? IdGroup { get; set; }

    public string? Login { get; set; }

    public string? Password { get; set; }

}
