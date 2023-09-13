import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#this line of code will select from database
# data = supabase.table("test").select("*").execute()
# print(data)
#
#this line of code will insert to database
# data = supabase.table("test").insert({"name":"Wanda"}).execute()
# print(data)
#
#this line of code will update to database
#
# data = supabase.table("table").update({"name":"Maximoff"}).eq("id", 1).execute()
# print(data)
