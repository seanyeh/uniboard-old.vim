com! UniboardYank call uniboard#Yank()
com! -nargs=1 UniboardPaste call uniboard#Paste(<f-args>)
com! UniboardIsRunning call uniboard#IsRunning()
com! UniboardStopDaemon call uniboard#StopDaemon()

autocmd TextYankPost * call uniboard#Yank()

noremap p :call uniboard#Paste('p')<CR>
noremap P :call uniboard#Paste('P')<CR>
