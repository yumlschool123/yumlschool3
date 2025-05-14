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
    public class UsersController : ControllerBase
    {
        private readonly YumlsschooldbContext _context;

        public UsersController(YumlsschooldbContext context)
        {
            _context = context;
        }

        // GET: api/Users
        [HttpGet]
        public async Task<ActionResult<IEnumerable<User>>> GetUsers()
        {
            return await _context.Users.ToListAsync();
        }

        // GET: api/Users/5
        [HttpGet("{id}")]
        public async Task<ActionResult<User>> GetUser(int? id)
        {
            var user = await _context.Users.FindAsync(id);

            if (user == null)
            {
                return NotFound();
            }

            return user;
        }

        // PUT: api/Users/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutUser(int? id, User user)
        {
            if (id != user.IdUser)
            {
                return BadRequest();
            }

            // Проверяем, существует ли пользователь
            var existingUser = await _context.Users.FindAsync(id);
            if (existingUser == null)
            {
                return NotFound();
            }

            // Обновляем поля существующего пользователя
            existingUser.FirstName = user.FirstName;
            existingUser.SecondName = user.SecondName;
            existingUser.MiddleName = user.MiddleName;
            existingUser.Email = user.Email;
            existingUser.IdRole = user.IdRole;
            existingUser.IdGroup = user.IdGroup;

            _context.Entry(existingUser).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!UserExists(id))
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


        // POST: api/Users
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<User>> PostUser(User user)
        {
            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetUser", new { id = user.IdUser }, user);
        }

        // DELETE: api/Users/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteUser(int? id)
        {
            var user = await _context.Users.FindAsync(id);
            if (user == null)
            {
                return NotFound();
            }

            _context.Users.Remove(user);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool UserExists(int? id)
        {
            return _context.Users.Any(e => e.IdUser == id);
        }

        // POST: api/Users/Authenticate
        [HttpPost("Authenticate")]
        public async Task<ActionResult<User>> Authenticate([FromBody] User user)
        {
            // Проверка на наличие логина и пароля
            if (string.IsNullOrEmpty(user.Login) || string.IsNullOrEmpty(user.Password))
            {
                return BadRequest("Логин и пароль обязательны.");
            }

            // Поиск пользователя по логину и паролю
            var foundUser = await _context.Users
                .FirstOrDefaultAsync(u => u.Login == user.Login && u.Password == user.Password);

            if (foundUser == null)
            {
                return Unauthorized("Неверный логин или пароль.");
            }

            // Возвращаем информацию о пользователе
            return Ok(new
            {
                idUser = foundUser.IdUser,
                idRole = foundUser.IdRole,
                firstName = foundUser.FirstName,
                secondName = foundUser.SecondName,
                middleName = foundUser.MiddleName
            });
        }





        // GET: api/Users/filter
        [HttpGet("filter")]
        public async Task<ActionResult<IEnumerable<User>>> GetUsersByGroupId(int groupId)
        {
            var students = await _context.Users
                .Where(u => u.IdGroup == groupId)
                .ToListAsync();

            return Ok(students);
        }

    }
}

