using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using YumlsSchoolAPI.Models;

namespace YumlsSchoolAPI.Models
{
    [Route("api/[controller]")]
    [ApiController]
    public class TestsController : ControllerBase
    {
        private readonly YumlsschooldbContext _context;

        public TestsController(YumlsschooldbContext context)
        {
            _context = context;
        }

        // GET: api/Tests
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Test>>> GetTests()
        {
            return await _context.Tests.ToListAsync();
        }

        // GET: api/Tests/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Test>> GetTest(int? id)
        {
            var test = await _context.Tests.FindAsync(id);

            if (test == null)
            {
                return NotFound();
            }

            return test;
        }

        // PUT: api/Tests/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutTest(int? id, Test test)
        {
            if (id != test.IdTest)
            {
                return BadRequest();
            }

            _context.Entry(test).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!TestExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Tests
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Test>> PostTest(Test test)
        {
            _context.Tests.Add(test);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetTest", new { id = test.IdTest }, test);
        }

        // DELETE: api/Tests/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTest(int? id)
        {
            var test = await _context.Tests.FindAsync(id);
            if (test == null)
            {
                return NotFound();
            }

            try
            {
                // Удаляем все попытки прохождения теста
                var attempts = await _context.TestAttempts.Where(a => a.TestId == id).ToListAsync();
                _context.TestAttempts.RemoveRange(attempts);

                // Удаляем все вопросы теста
                var questions = await _context.QuestionsTests.Where(q => q.IdTest == id).ToListAsync();
                _context.QuestionsTests.RemoveRange(questions);

                // Удаляем критерии оценивания
                var grading = await _context.GradingCriteria.Where(g => g.IdTest == id).ToListAsync();
                _context.GradingCriteria.RemoveRange(grading);

                // Удаляем сам тест
                _context.Tests.Remove(test);

                // Сохраняем все изменения
                await _context.SaveChangesAsync();

                return NoContent();
            }

            catch (Exception ex)
            {
                // Логируем ошибку
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

            private bool TestExists(int? id)
            {
                return _context.Tests.Any(e => e.IdTest == id);
            }
    }
}

