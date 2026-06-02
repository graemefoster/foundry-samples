# Multi-stage Docker build for HelloWorldAgent (.NET 10)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copy project file and restore first for better layer caching
COPY HelloWorldAgent.csproj ./
RUN dotnet restore HelloWorldAgent.csproj

# Copy source and publish
COPY . ./
RUN dotnet publish HelloWorldAgent.csproj -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=build /app/publish ./

# ASP.NET Core listens on port 8080 inside the container
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "HelloWorldAgent.dll"]
