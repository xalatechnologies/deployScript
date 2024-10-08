using DotnetMongoApi.Context;
using DotnetMongoApi.Models;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;

namespace DotnetMongoApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TestController : ControllerBase
    {
        private readonly MongoDbContext _context;

        public TestController()
        {
            _context = new MongoDbContext();
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            var models = _context.TestModels.Find(_ => true).ToList();
            return Ok(models);
        }

        [HttpPost]
        public IActionResult Create([FromBody] TestModel model)
        {
            _context.TestModels.InsertOne(model);
            return CreatedAtAction(nameof(GetAll), new { id = model.Id }, model);
        }
    }
}