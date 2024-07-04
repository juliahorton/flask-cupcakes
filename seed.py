from app import app
from models import db, Cupcake

# Create all tables within application context
app.app_context().push()
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Cupcake.query.delete()

# Cupcakes
c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

db.session.add_all([c1, c2])
db.session.commit()