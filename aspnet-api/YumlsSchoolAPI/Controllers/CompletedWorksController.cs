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
public class CompletedWorksController : ControllerBase
{
    private readonly YumlsschooldbContext _context;

    public CompletedWorksController(YumlsschooldbContext context)
    {
        _context = context;
    }

    // GET: api/CompletedWorks
    [HttpGet]
    public async Task<ActionResult<IEnumerable<CompletedWork>>> GetCompletedWorks()
    {
        return await _context.CompletedWorks.ToListAsync();
    }

    // GET: api/CompletedWorks/5
    [HttpGet("{id}")]
    public async Task<ActionResult<CompletedWork>> GetCompletedWork(int? id)
    {
        var completedWork = await _context.CompletedWorks.FindAsync(id);

        if (completedWork == null)
        {
            return NotFound();
        }

        return completedWork;
    }

    // PUT: api/CompletedWorks/5
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPut("{id}")]
    public async Task<IActionResult> PutCompletedWork(int? id, CompletedWork completedWork)
    {
        if (id != completedWork.IdCompletedWork)
        {
            return BadRequest();
        }

        _context.Entry(completedWork).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!CompletedWorkExists(id))
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

    // POST: api/CompletedWorks
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPost]
    public async Task<ActionResult<CompletedWork>> PostCompletedWork(CompletedWork completedWork)
    {
        _context.CompletedWorks.Add(completedWork);
        await _context.SaveChangesAsync();

        return CreatedAtAction("GetCompletedWork", new { id = completedWork.IdCompletedWork }, completedWork);
    }

    // DELETE: api/CompletedWorks/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteCompletedWork(int? id)
    {
        var completedWork = await _context.CompletedWorks.FindAsync(id);
        if (completedWork == null)
        {
            return NotFound();
        }

        _context.CompletedWorks.Remove(completedWork);
        await _context.SaveChangesAsync();

        return NoContent();
    }

    private bool CompletedWorkExists(int? id)
    {
        return _context.CompletedWorks.Any(e => e.IdCompletedWork == id);
    }
}
}
