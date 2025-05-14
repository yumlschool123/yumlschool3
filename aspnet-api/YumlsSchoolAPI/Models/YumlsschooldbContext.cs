using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace YumlsSchoolAPI.Models;

public partial class YumlsschooldbContext : DbContext
{
    public YumlsschooldbContext()
    {
    }

    public YumlsschooldbContext(DbContextOptions<YumlsschooldbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<CompletedWork> CompletedWorks { get; set; }

    public virtual DbSet<GradingCriterion> GradingCriteria { get; set; }

    public virtual DbSet<Group> Groups { get; set; }

    public virtual DbSet<LectionMaterial> LectionMaterials { get; set; }

    public virtual DbSet<PracticalWork> PracticalWorks { get; set; }

    public virtual DbSet<QuestionsTest> QuestionsTests { get; set; }

    public virtual DbSet<Role> Roles { get; set; }

    public virtual DbSet<Status> Statuses { get; set; }

    public virtual DbSet<Subject> Subjects { get; set; }

    public virtual DbSet<Test> Tests { get; set; }

    public virtual DbSet<TestAttempt> TestAttempts { get; set; }

    public virtual DbSet<User> Users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<CompletedWork>(entity =>
        {
            entity.HasKey(e => e.IdCompletedWork).HasName("PK__Complete__CAC448AD090323A0");

            entity.ToTable("CompletedWork");

            entity.Property(e => e.IdCompletedWork).HasColumnName("ID_CompletedWork");
            entity.Property(e => e.DateUploadCompletedWork).HasColumnName("DateUpload_CompletedWork");
            entity.Property(e => e.Grade)
                .HasMaxLength(64)
                .IsUnicode(true);
            entity.Property(e => e.NameFileCompletedWork)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_FileCompletedWork");
            entity.Property(e => e.PracticalWorkId).HasColumnName("PracticalWork_ID");
            entity.Property(e => e.StatusId).HasColumnName("Status_ID");
            entity.Property(e => e.TimeUploadCompletedWork)
                .HasDefaultValueSql("(CONVERT([time],getdate()))")
                .HasColumnName("TimeUpload_CompletedWork");
            entity.Property(e => e.UrlFileCompletedWork)
                .HasMaxLength(3000)
                .IsUnicode(true)
                .HasColumnName("URL_FileCompletedWork");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

         
        });

        modelBuilder.Entity<GradingCriterion>(entity =>
        {
            entity.HasKey(e => e.IdCriteria).HasName("PK__GradingC__6D5D9FD960779EB1");

            entity.Property(e => e.IdCriteria).HasColumnName("ID_Criteria");
            entity.Property(e => e.IdTest).HasColumnName("ID_Test");
            entity.Property(e => e.MaxPoints).HasColumnName("Max_Points");
            entity.Property(e => e.MinPoints).HasColumnName("Min_Points");

           
        });

        modelBuilder.Entity<Group>(entity =>
        {
            entity.HasKey(e => e.IdGroup).HasName("PK__Group__96125DD8E6CEBF44");

            entity.ToTable("Group");

            entity.Property(e => e.IdGroup).HasColumnName("ID_Group");
            entity.Property(e => e.NameGroup)
                .HasMaxLength(50)
                .IsUnicode(true)
                .HasColumnName("Name_Group");
        });

        modelBuilder.Entity<LectionMaterial>(entity =>
        {
            entity.HasKey(e => e.IdLectionMaterial).HasName("PK__LectionM__2A1A1672B447D85C");

            entity.ToTable("LectionMaterial");

            entity.Property(e => e.IdLectionMaterial).HasColumnName("ID_LectionMaterial");
            entity.Property(e => e.DateUploadLectionMaterial)
                .HasDefaultValueSql("(CONVERT([date],getdate()))")
                .HasColumnName("DateUpload_LectionMaterial");
            entity.Property(e => e.DescriptionLectionMaterial)
                .HasMaxLength(1024)
                .IsUnicode(true)
                .HasColumnName("Description_LectionMaterial");
            entity.Property(e => e.NameFileLection)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_FileLection");
            entity.Property(e => e.NameLectionMaterial)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_LectionMaterial");
            entity.Property(e => e.SubjectId).HasColumnName("Subject_ID");
            entity.Property(e => e.TimeUploadLectionMaterial)
                .HasDefaultValueSql("(CONVERT([time],getdate()))")
                .HasColumnName("TimeUpload_LectionMaterial");
            entity.Property(e => e.UrlFileLection)
                .HasMaxLength(1024)
                .IsUnicode(true)
                .HasColumnName("URL_FileLection");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

        
        });

        modelBuilder.Entity<PracticalWork>(entity =>
        {
            entity.HasKey(e => e.IdPracticalWork).HasName("PK__Practica__67699CC80BEECBE1");

            entity.ToTable("PracticalWork");

            entity.Property(e => e.IdPracticalWork).HasColumnName("ID_PracticalWork");
            entity.Property(e => e.DateUploadPracticalWork)
                .HasDefaultValueSql("(CONVERT([date],getdate()))")
                .HasColumnName("DateUpload_PracticalWork");
            entity.Property(e => e.DescriptionPracticalWork)
                .HasMaxLength(3000)
                .IsUnicode(true)
                .HasColumnName("Description_PracticalWork");
            entity.Property(e => e.NameFilePracticalWork)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_FilePracticalWork");
            entity.Property(e => e.NamePracticalWork)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_PracticalWork");
            entity.Property(e => e.SubjectId).HasColumnName("Subject_ID");
            entity.Property(e => e.TimeUploadPracticalWork)
                .HasDefaultValueSql("(CONVERT([time],getdate()))")
                .HasColumnName("TimeUpload_PracticalWork");
            entity.Property(e => e.UrlFilePracticalWork)
                .HasMaxLength(3000)
                .IsUnicode(true)
                .HasColumnName("URL_FilePracticalWork");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

           
        });

        modelBuilder.Entity<QuestionsTest>(entity =>
        {
            entity.HasKey(e => e.IdQuestion).HasName("PK__Question__7F5FD85406B00643");

            entity.Property(e => e.IdQuestion).HasColumnName("ID_Question");
            entity.Property(e => e.AnswerVariants)
		.HasMaxLength(1024)
		.IsUnicode(true)
		.HasColumnName("AnswerVariants");
            entity.Property(e => e.CorrectAnswer)
		.HasMaxLength(1024)
		.IsUnicode(true)
		.HasColumnName("CorrectAnswer");
            entity.Property(e => e.IdTest).HasColumnName("ID_Test");
            entity.Property(e => e.Points).HasDefaultValue(1);
            entity.Property(e => e.QuestionText)
                .HasMaxLength(1000)
                .IsUnicode(true)
                .HasColumnName("Question_Text");

          
        });

        modelBuilder.Entity<Role>(entity =>
        {
            entity.HasKey(e => e.IdRole).HasName("PK__Role__43DCD32D0ABE227B");

            entity.ToTable("Role");

            entity.Property(e => e.IdRole).HasColumnName("ID_Role");
            entity.Property(e => e.RoleName)
                .HasMaxLength(30)
                .IsUnicode(true)
                .HasColumnName("Role_Name");
        });

        modelBuilder.Entity<Status>(entity =>
        {
            entity.HasKey(e => e.IdStatus).HasName("PK__Status__5AC2A7340699E02B");

            entity.ToTable("Status");

            entity.Property(e => e.IdStatus).HasColumnName("ID_Status");
            entity.Property(e => e.NameStatus)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_Status");
        });

        modelBuilder.Entity<Subject>(entity =>
        {
            entity.HasKey(e => e.IdSubject).HasName("PK__Subject__20028FF4D2C1EC0E");

            entity.ToTable("Subject");

            entity.Property(e => e.IdSubject).HasColumnName("ID_Subject");
            entity.Property(e => e.IdGroup).HasColumnName("ID_Group");
            entity.Property(e => e.NameSubject)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasColumnName("Name_Subject");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

        
        });

        modelBuilder.Entity<Test>(entity =>
        {
            entity.HasKey(e => e.IdTest).HasName("PK__Tests__D6560E251178E8D2");

            entity.Property(e => e.IdTest).HasColumnName("ID_Test");
            entity.Property(e => e.DateUploadTest)
                .HasDefaultValueSql("(CONVERT([date],getdate()))")
                .HasColumnName("DateUpload_Test");
            entity.Property(e => e.DescriptionTest)
                .HasMaxLength(1000)
                .IsUnicode(true)
                .HasColumnName("Description_Test");
            entity.Property(e => e.NameTest)
                .HasMaxLength(255)
                .IsUnicode(true)
                .HasColumnName("Name_Test");
            entity.Property(e => e.SubjectId).HasColumnName("Subject_ID");
            entity.Property(e => e.TimeUploadTest)
                .HasDefaultValueSql("(CONVERT([time],getdate()))")
                .HasColumnName("TimeUpload_Test");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

    
        });

        modelBuilder.Entity<TestAttempt>(entity =>
        {
            entity.HasKey(e => e.IdTestAttempt).HasName("PK__TestAtte__34F010C9167913E6");

            entity.ToTable("TestAttempt");

            entity.Property(e => e.IdTestAttempt).HasColumnName("ID_TestAttempt");
            entity.Property(e => e.EndTime)
                .HasColumnType("datetime")
                .HasColumnName("End_Time");
            entity.Property(e => e.Grade).HasColumnType("decimal(3, 1)");
            entity.Property(e => e.StartTime)
                .HasDefaultValueSql("(getdate())")
                .HasColumnType("datetime")
                .HasColumnName("Start_Time");
            entity.Property(e => e.Status)
                .HasMaxLength(20)
                .IsUnicode(true);
            entity.Property(e => e.TestId).HasColumnName("Test_ID");
            entity.Property(e => e.UserId).HasColumnName("User_ID");

  
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.IdUser).HasName("PK__User__ED4DE442B7850D56");

            entity.ToTable("User");

            entity.HasIndex(e => e.Email, "UQ__User__A9D10534514A39ED").IsUnique();

            entity.Property(e => e.IdUser).HasColumnName("ID_User");
            entity.Property(e => e.Email)
                .HasMaxLength(255)
                .IsUnicode(true);
            entity.Property(e => e.FirstName)
                .HasMaxLength(64)
                .IsUnicode(true);
            entity.Property(e => e.IdGroup).HasColumnName("ID_Group");
            entity.Property(e => e.IdRole).HasColumnName("ID_Role");
            entity.Property(e => e.Login)
                .HasMaxLength(150)
                .IsUnicode(true);
            entity.Property(e => e.MiddleName)
                .HasMaxLength(64)
                .IsUnicode(true)
                .HasDefaultValue("Отсутствует");
            entity.Property(e => e.Password)
                .HasMaxLength(150)
                .IsUnicode(true);
            entity.Property(e => e.SecondName)
                .HasMaxLength(64)
                .IsUnicode(true);

     
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
