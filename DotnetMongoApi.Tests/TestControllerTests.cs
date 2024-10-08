using DotnetMongoApi.Controllers;
using DotnetMongoApi.Models;
using Xunit;
using Microsoft.AspNetCore.Mvc;

namespace DotnetMongoApi.Tests
{
    public class TestControllerTests
    {
        [Fact]
        public void GetAll_ShouldReturnOk()
        {
            var controller = new TestController();
            var result = controller.GetAll();
            Assert.IsType<OkObjectResult>(result);
        }

        [Fact]
        public void Create_ShouldReturnCreatedAtAction()
        {
            var controller = new TestController();
            var testModel = new TestModel { Name = "Test", Age = 25 };
            var result = controller.Create(testModel);
            Assert.IsType<CreatedAtActionResult>(result);
        }
    }
}