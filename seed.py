"""Script to seed database with labs."""

import os

import crud
import model
import server

os.system("dropdb lab-pairs")
os.system("createdb lab-pairs")

model.connect_to_db(server.app)
model.db.create_all()

labs = [
    'Blockly', 'Guessing Game', 'Calculator 1', 'Calculator 2', 'List Slicing',
    'Data Structures', 'Dictionaries: Word Count', 'Dictionaries: Restaurant',
    'Markov Chains', 'Markov Chains: Discord', 'Object-Oriented Drawing (in Replit)',
    'Practice with Object Oriented Melons', 'Object Oriented Melons',
    'HTML: Forms', 'CSS: Trials', 'Flask: Intro', 'Madlibs', 'Shopping Site',
    'APIs', 'Testing', 'JavaScript Trials: Part 1', 'JavaScript Trials: Part 2',
    'JavaScript Sharkwords', 'JavaScript: Coffee Shop App', 'AJAX',
    'React: Trading Cards', 'React: Trading Cards 2', 'Bootstrap', 'SQL Quiz',
    'Project Tracker', 'Project Tracker Python', 'Movie Ratings App', 'Testing Flask'
]

count = 1
for lab in labs:
    new_lab = crud.create_new_lab(lab)
    model.db.session.add(new_lab)
    model.db.session.commit()
    print(f'{count}. Added and committed {new_lab.title}!')
    count += 1
