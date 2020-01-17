"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app, db
from alayatodo.models import User, Todo


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


def _create_seed():
    user1 = User(username='user1')
    user1.set_password('user1')
    db.session.add(user1)

    user2 = User(username='user2')
    user2.set_password('user2')
    db.session.add(user2)

    user3 = User(username='user3')
    user3.set_password('user3')
    db.session.add(user3)
    print(User.query.count(), "Users added")

    db.session.add(Todo(user_id=1, description='Vivamus tempus'))
    db.session.add(Todo(user_id=1, description='lorem ac odio'))
    db.session.add(Todo(user_id=1, description='Ut congue odio'))
    db.session.add(Todo(user_id=1, description='Sodales finibus'))
    db.session.add(Todo(user_id=1, description='Accumsan nunc vitae'))
    db.session.add(Todo(user_id=2, description='Lorem ipsum'))
    db.session.add(Todo(user_id=2, description='In lacinia est'))
    db.session.add(Todo(user_id=2, description='Odio varius gravida'))
    print(Todo.query.count(), "Todos added")
    db.session.commit()


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/migration.sql')
        _create_seed()
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)


# flask shell setting
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Todo': Todo}