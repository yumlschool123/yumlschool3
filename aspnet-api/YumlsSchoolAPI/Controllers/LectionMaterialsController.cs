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
public class LectionMaterialsController : ControllerBase
{
    private readonly YumlsschooldbContext _context;

    public LectionMaterialsController(YumlsschooldbContext context)
    {
        _context = context;
    }

    // GET: api/LectionMaterials
    [HttpGet]
    public async Task<ActionResult<IEnumerable<LectionMaterial>>> GetLectionMaterials()
    {
        return await _context.LectionMaterials.ToListAsync();
    }

    // GET: api/LectionMaterials/5
    [HttpGet("{id}")]
    public async Task<ActionResult<LectionMaterial>> GetLectionMaterial(int? id)
    {
        var lectionMaterial = await _context.LectionMaterials.FindAsync(id);

        if (lectionMaterial == null)
        {
            return NotFound();
        }

        return lectionMaterial;
    }

    // PUT: api/LectionMaterials/5
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPut("{id}")]
    public async Task<IActionResult> PutLectionMaterial(int? id, LectionMaterial lectionMaterial)
    {
        if (id != lectionMaterial.IdLectionMaterial)
        {
            return BadRequest();
        }

        _context.Entry(lectionMaterial).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!LectionMaterialExists(id))
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

    // POST: api/LectionMaterials
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPost]
    public async Task<ActionResult<LectionMaterial>> PostLectionMaterial(LectionMaterial lectionMaterial)
    {
        _context.LectionMaterials.Add(lectionMaterial);
        await _context.SaveChangesAsync();

        return CreatedAtAction("GetLectionMaterial", new { id = lectionMaterial.IdLectionMaterial }, lectionMaterial);
    }

    // DELETE: api/LectionMaterials/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteLectionMaterial(int? id)
    {
        var lectionMaterial = await _context.LectionMaterials.FindAsync(id);
        if (lectionMaterial == null)
        {
            return NotFound();
        }

        _context.LectionMaterials.Remove(lectionMaterial);
        await _context.SaveChangesAsync();

        return NoContent();
    }

    private bool LectionMaterialExists(int? id)
    {
        return _context.LectionMaterials.Any(e => e.IdLectionMaterial == id);
    }
}
}
