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
    public class QuestionsTestsController : ControllerBase
    {
        private readonly YumlsschooldbContext _context;

        public QuestionsTestsController(YumlsschooldbContext context)
        {
            _context = context;
        }

        // GET: api/QuestionsTests
        [HttpGet]
        public async Task<ActionResult<IEnumerable<QuestionsTest>>> GetQuestionsTests()
        {
            return await _context.QuestionsTests.ToListAsync();
        }

        // GET: api/QuestionsTests/5
        [HttpGet("{id}")]
        public async Task<ActionResult<QuestionsTest>> GetQuestionsTest(int? id)
        {
            var questionsTest = await _context.QuestionsTests.FindAsync(id);

            if (questionsTest == null)
            {
                return NotFound();
            }

            return questionsTest;
        }

        // PUT: api/QuestionsTests/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutQuestionsTest(int? id, QuestionsTest questionsTest)
        {
            if (id != questionsTest.IdQuestion)
            {
                return BadRequest();
            }

            _context.Entry(questionsTest).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!QuestionsTestExists(id))
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

        // POST: api/QuestionsTests
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<QuestionsTest>> PostQuestionsTest(QuestionsTest questionsTest)
        {
            _context.QuestionsTests.Add(questionsTest);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetQuestionsTest", new { id = questionsTest.IdQuestion }, questionsTest);
        }

        // DELETE: api/QuestionsTests/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteQuestionsTest(int? id)
        {
            var questionsTest = await _context.QuestionsTests.FindAsync(id);
            if (questionsTest == null)
            {
                return NotFound();
            }

            _context.QuestionsTests.Remove(questionsTest);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool QuestionsTestExists(int? id)
        {
            return _context.QuestionsTests.Any(e => e.IdQuestion == id);
        }
    }
}
