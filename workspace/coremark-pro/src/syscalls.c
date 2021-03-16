/* Includes */
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <errno.h>
#include <stdio.h>
#include <signal.h>
#include <time.h>
#include <sys/time.h>
#include <sys/times.h>

/* Forward prototypes */
int	_system		(const char *);
int	_rename		(const char *, const char *);
int	_isatty		(int);
clock_t _times		(struct tms *);
int	_gettimeofday	(struct timeval *, void *);
void	_raise		(void);
int	_unlink		(const char *);
int	_link		(const char *, const char *);
int	_stat		(const char *, struct stat *);
int	_fstat		(int, struct stat *);
void *	_sbrk		(ptrdiff_t);
pid_t	_getpid		(void);
int	_kill		(int, int);
void	_exit		(int);
int	_close		(int);
int	_open		(const char *, int, ...);
int	_write		(int, const void *, size_t);
off_t	_lseek		(int, off_t, int);
int	_read		(int, void *, size_t);
int	_wait		(int *);
int	_fork		(void);
int	_execve		(const char *, char *const *, char *const *);
void	initialise_monitor_handles (void);

/* Variables */
extern int errno;

register char * stack_ptr asm ("sp");

char *__env[1] = { 0 };
char **environ = __env;

/* Functions */
int __attribute__((weak))
_system(const char *s)
{
 	if (s == NULL)
		return 0;

	errno = ENOSYS;
	return -1;
}

int __attribute__((weak))
_rename(const char *oldpath, const char *newpath)
{
	errno = ENOSYS;
	return -1;
}

int __attribute__((weak))
_isatty(int file)
{
 	return (file <= 2) ? 1 : 0;  /* one of stdin, stdout, and stderr */
}

clock_t __attribute__((weak))
_times(struct tms *buf)
{
	return -1;
}

int __attribute__((weak))
_gettimeofday(struct timeval *tp, void *tzvp)
{
	return 0;
}

int __attribute__((weak))
_unlink(const char *name)
{
	errno = ENOENT;
	return -1;
}

int __attribute__((weak))
_link(const char *old, const char *new)
{
	errno = EMLINK;
	return -1;
}

int __attribute__((weak))
_stat(const char *file, struct stat *st)
{
	st->st_mode = S_IFCHR;
	return 0;
}

int __attribute__((weak))
_fstat(int file, struct stat *st)
{
	st->st_mode = S_IFCHR;
	return 0;
}

/* Heap limit returned from SYS_HEAPINFO Angel semihost call.  */
char *__heap_limit = (char *)0xcafedead;

void * __attribute__((weak))
_sbrk(ptrdiff_t incr)
{
	extern char end asm ("end"); /* Defined by the linker.  */
	static char * heap_end;
	char *        prev_heap_end;

	if (heap_end == NULL)
		heap_end = & end;

	prev_heap_end = heap_end;

	if ((heap_end + incr > stack_ptr) ||
	    /* Honour heap limit if it's valid.  */
	    (__heap_limit != 0xcafedead && heap_end + incr > __heap_limit)) {
	    /* Some of the libstdc++-v3 tests rely upon detecting
	       out of memory errors, so do not abort here.  */
#if 0
		extern void abort(void);

		_write(1, "_sbrk: Heap and stack collision\n", 32);

		abort();
#else
		errno = ENOMEM;
		return (void *)-1;
#endif
	}

	heap_end += incr;

	return (void *)prev_heap_end;
}

pid_t __attribute__((weak))
_getpid(void)
{
	return (pid_t)1;
}

int __attribute__((weak))
_kill(int pid, int sig)
{
	errno = EINVAL;
	return -1;
}

void __attribute__((weak))
_exit(int status)
{
	_kill(status, -1);
	while (1) {}		/* Make sure we hang here */
}

int __attribute__((weak))
_close(int file)
{
	return -1;
}

int __attribute__((weak))
_open(const char *path, int flags, ...)
{
	/* Pretend like we always fail */
	return -1;
}

#if 0 // Use the one in libmimxrt685s.a
extern int __io_putchar(int ch) __attribute__((weak));

int __attribute__((weak))
_write(int file, const void *data, size_t len)
{
	const char *ptr = (const char *)data;
	int DataIdx;

	for (DataIdx = 0; DataIdx < len; DataIdx++) {
		__io_putchar(*ptr++);
	}
	return len;
}
#endif

off_t __attribute__((weak))
_lseek(int file, off_t ptr, int dir)
{
	return 0;
}

#if 0 // Use the one in libmimxrt685s.a
extern int __io_getchar(void) __attribute__((weak));

int __attribute__((weak))
_read(int file, void *buf, size_t len)
{
	char *ptr = (char *)buf;
	int DataIdx;

	for (DataIdx = 0; DataIdx < len; DataIdx++) {
		*ptr++ = __io_getchar();
	}

	return len;
}
#endif

int __attribute__((weak))
_wait(int *status)
{
	errno = ECHILD;
	return -1;
}

int __attribute__((weak))
_fork(void)
{
	errno = EAGAIN;
	return -1;
}

int __attribute__((weak))
_execve(const char *name, char *const *argv, char *const *env)
{
	errno = ENOMEM;
	return -1;
}

void __attribute__((weak))
initialise_monitor_handles(void)
{
}
