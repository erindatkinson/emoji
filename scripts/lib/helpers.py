from sqlite3 import connect

debug = False

def setup_db(db):
  conn = connect(db)

  with conn:
    conn.execute("CREATE TABLE IF NOT EXISTS downloads (emoji text, namespace text)")
  
  conn.close()

def debug_print(msg):
  if debug:
    print(msg)

def get_surrounding(pages_list, i):
  if i == len(pages_list)-1:
      z_next = ""
      f_next = ""
      z_prev = f"{pages_list[i-1][1]:04d}"
      f_prev = pages_list[i-1][0]

  elif i == 0:
    z_next = f"{pages_list[i+1][1]:04d}"
    f_next = pages_list[i+1][0]
    z_prev = ""
    f_prev = ""
  else:
    z_next = f"{pages_list[i+1][1]:04d}"
    f_next = pages_list[i+1][0]
    z_prev = f"{pages_list[i-1][1]:04d}"
    f_prev = pages_list[i-1][0]
  
  return (z_next, f_next, z_prev, f_prev)

