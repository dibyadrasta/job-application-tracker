from database import initialize_database
from ui import create_application


initialize_database()

root = create_application()

root.mainloop()