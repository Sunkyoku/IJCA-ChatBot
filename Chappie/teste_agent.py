from Chappie.agent import consultar_sqlite

print(consultar_sqlite("SELECT name FROM sqlite_master WHERE type='table'"))