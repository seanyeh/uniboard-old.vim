let s:script_directory = expand('<sfile>:p:h')
let s:py_file = s:script_directory.'/uniboard.py'
let s:uniboard_command = 'python3 '.s:py_file.' '

function! uniboard#IsRunning()
  call system(s:uniboard_command.'ping')
  return !v:shell_error
endfunction!

function! uniboard#Yank()
  if !uniboard#IsRunning()
    let daemon_command = 'nohup '.s:uniboard_command.' daemon&'
    call system(daemon_command)
  end

  call system(s:uniboard_command.'put '.shellescape(@").'')
endfunction!

function! uniboard#Paste(key)
  let value = system(s:uniboard_command.'get')
  if !v:shell_error && strlen(value) > 0
    let @" = value
  endif

  silent exe "normal! ".a:key
endfunction!

function! uniboard#StopDaemon()
  let pid = system(s:uniboard_command.'ping')

  if !v:shell_error
    call system('kill -15 '.pid)
  endif
endfunction!
