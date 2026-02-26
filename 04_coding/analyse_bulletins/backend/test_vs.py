import json
from database import SessionLocal
from models import Teacher
from services.crypto import decrypt
from services.ecoledirecte_client import EcoleDirecteClient

db = SessionLocal()
t = db.query(Teacher).first()
c = EcoleDirecteClient()
info = c.login(t.ecoledirecte_login, decrypt(t.encrypted_password))
token = info['token']
db.close()

vs = c.get_student_vie_scolaire(token, 946)
print("=== Clés top-level ===")
for k, v in vs.items():
    if isinstance(v, list):
        print(f"  {k}: liste de {len(v)} éléments")
        if v:
            print(f"    1er élément: {json.dumps(v[0], ensure_ascii=False, indent=4)}")
    else:
        print(f"  {k}: {str(v)[:100]}")

c.close()
