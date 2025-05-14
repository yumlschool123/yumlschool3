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
    public class GradingCriterionsController : ControllerBase
    {
        private readonly YumlsschooldbContext _context;

        public GradingCriterionsController(YumlsschooldbContext context)
        {
            _context = context;
        }

        // GET: api/GradingCriterions
        [HttpGet]
        public async Task<ActionResult<IEnumerable<GradingCriterion>>> GetGradingCriteria()
        {
            return await _context.GradingCriteria.ToListAsync();
        }

        // GET: api/GradingCriterions/5
        [HttpGet("{id}")]
        public async Task<ActionResult<GradingCriterion>> GetGradingCriterion(int? id)
        {
            var gradingCriterion = await _context.GradingCriteria.FindAsync(id);

            if (gradingCriterion == null)
            {
                return NotFound();
            }

            return gradingCriterion;
        }

        // PUT: api/GradingCriterions/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutGradingCriterion(int? id, GradingCriterion gradingCriterion)
        {
            if (id != gradingCriterion.IdCriteria)
            {
                return BadRequest();
            }

            _context.Entry(gradingCriterion).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!GradingCriterionExists(id))
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

        // POST: api/GradingCriterions
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<GradingCriterion>> PostGradingCriterion(GradingCriterion gradingCriterion)
        {
            _context.GradingCriteria.Add(gradingCriterion);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetGradingCriterion", new { id = gradingCriterion.IdCriteria }, gradingCriterion);
        }

        // DELETE: api/GradingCriterions/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteGradingCriterion(int? id)
        {
            var gradingCriterion = await _context.GradingCriteria.FindAsync(id);
            if (gradingCriterion == null)
            {
                return NotFound();
            }

            _context.GradingCriteria.Remove(gradingCriterion);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool GradingCriterionExists(int? id)
        {
            return _context.GradingCriteria.Any(e => e.IdCriteria == id);
        }
    }
}
