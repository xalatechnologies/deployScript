using MongoDB.Driver;
using DotnetMongoApi.Models;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.OpenApi;

namespace DotnetMongoApi.Context
{
    public class MongoDbContext
    {
        private readonly IMongoDatabase _database;

        public MongoDbContext()
        {
            var client = new MongoClient("mongodb://localhost:27017");
            _database = client.GetDatabase("TestDb");
        }

        public IMongoCollection<TestModel> TestModels => _database.GetCollection<TestModel>("TestModels");
    }


public static class TestModelEndpoints
{
	public static void MapTestModelEndpoints (this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/TestModel").WithTags(nameof(TestModel));

        group.MapGet("/", () =>
        {
            return new [] { new TestModel() };
        })
        .WithName("GetAllTestModels")
        .WithOpenApi();

        group.MapGet("/{id}", (int id) =>
        {
            //return new TestModel { ID = id };
        })
        .WithName("GetTestModelById")
        .WithOpenApi();

        group.MapPut("/{id}", (int id, TestModel input) =>
        {
            return TypedResults.NoContent();
        })
        .WithName("UpdateTestModel")
        .WithOpenApi();

        group.MapPost("/", (TestModel model) =>
        {
            //return TypedResults.Created($"/api/TestModels/{model.ID}", model);
        })
        .WithName("CreateTestModel")
        .WithOpenApi();

        group.MapDelete("/{id}", (int id) =>
        {
            //return TypedResults.Ok(new TestModel { ID = id });
        })
        .WithName("DeleteTestModel")
        .WithOpenApi();
    }
}}