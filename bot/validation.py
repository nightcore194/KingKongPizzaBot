from models import db, Employee


def isAdmin(tg_id: int) -> bool:
    return db.query(Employee).filter(Employee.telegram_id == tg_id,
                                     Employee.role == 'admin').first() is not None
