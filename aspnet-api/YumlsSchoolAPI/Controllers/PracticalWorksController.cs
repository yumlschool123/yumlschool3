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
    public class PracticalWorksController : ControllerBase
    {
        private readonly YumlsschooldbContext _context;

        public PracticalWorksController(YumlsschooldbContext context)
        {
            _context = context;
        }

        // GET: api/PracticalWorks
        [HttpGet]
        public async Task<ActionResult<IEnumerable<PracticalWork>>> GetPracticalWorks()
        {
            return await _context.PracticalWorks.ToListAsync();
        }

        // GET: api/PracticalWorks/5
        [HttpGet("{id}")]
        public async Task<ActionResult<PracticalWork>> GetPracticalWork(int? id)
        {
            var practicalWork = await _context.PracticalWorks.FindAsync(id);

            if (practicalWork == null)
            {
                return NotFound();
            }

            return practicalWork;
        }

        // PUT: api/PracticalWorks/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPracticalWork(int? id, PracticalWork practicalWork)
        {
            if (id != practicalWork.IdPracticalWork)
            {
                return BadRequest();
            }

            _context.Entry(practicalWork).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!PracticalWorkExists(id))
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

        // POST: api/PracticalWorks
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<PracticalWork>> PostPracticalWork(PracticalWork practicalWork)
        {
            _context.PracticalWorks.Add(practicalWork);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetPracticalWork", new { id = practicalWork.IdPracticalWork }, practicalWork);
        }

        // DELETE: api/PracticalWorks/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePracticalWork(int? id)
        {
            var practicalWork = await _context.PracticalWorks.FindAsync(id);
            if (practicalWork == null)
            {
                return NotFound();
            }

            _context.PracticalWorks.Remove(practicalWork);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool PracticalWorkExists(int? id)
        {
            return _context.PracticalWorks.Any(e => e.IdPracticalWork == id);
        }

        // GET: api/PracticalWorks/{id}/completed
        [HttpGet("{id}/completed")]
        public async Task<ActionResult<IEnumerable<CompletedWork>>> GetCompletedWorksByPracticalWork(int id)
        {
            var completedWorks = await _context.CompletedWorks
                .Where(cw => cw.PracticalWorkId == id)
                .ToListAsync();

            if (completedWorks == null || !completedWorks.Any())
            {
                return NotFound();
            }

            return completedWorks;
        }
    }
}
