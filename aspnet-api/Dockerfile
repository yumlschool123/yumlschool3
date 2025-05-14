# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ./YumlsSchoolAPI/YumlsSchoolAPI.csproj ./YumlsSchoolAPI/
RUN dotnet restore ./YumlsSchoolAPI/YumlsSchoolAPI.csproj

COPY ./YumlsSchoolAPI ./YumlsSchoolAPI
WORKDIR /src/YumlsSchoolAPI
RUN dotnet publish YumlsSchoolAPI.csproj -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .

# ?? Добавляем строку:
EXPOSE 80

ENTRYPOINT ["dotnet", "YumlsSchoolAPI.dll"]
