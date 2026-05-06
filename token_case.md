Problem był w tym, że GitHub blokował push, bo ostatni commit nadal zawierał sekret w lesson7new.py.

Co zrobiłem
poprawiłem aktualny commit (git commit --amend --no-edit)
usunąłem sekret z historii tego commita
wypchnąłem branch main z powrotem na GitHub (git push --force-with-lease origin main)
