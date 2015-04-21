__author__ = 'jmagady'

import os
import sys
from app import app
from app.models import Post as Model
from flask_whooshalchemy import whoosh_index

"""
from app.models import <table to index> as Model. change <table to index> to the table you want indexed
atatime - the number of records to pull from the database at once
limitmb - "max" megabytes to use
procs - cores to use in parallel
"""

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
atatime = 512

with app.app_context():
    index = whoosh_index(app, Model)  # Create a Whoosh index object
    searchable = Model.__searchable__  # Import the fields we want indexed
    print 'counting rows...'
    total = int(Model.query.order_by(None).count())  # Count the number of rows
    done = 0  # initialize the done variable
    print 'total rows: {}'.format(total)
    writer = index.writer(limitmb=10000, procs=16, multisegment=True)  # Create the writer object
    for p in Model.query.yield_per(atatime):  # to batch results in sub-collections and yield them out partially (Save memory)
        record = dict([(s, p.__dict__[s]) for s in searchable])
        record.update({'id': unicode(p.id)})  # id is mandatory, or whoosh won't work
        writer.add_document(**record)
        done += 1  # update done variable
        if done % atatime == 0:
            print 'c {}/{} ({}%)'.format(done, total, round((float(done)/total)*100, 2)),

    print '{}/{} ({}%)'.format(done, total, round((float(done)/total)*100, 2))
    writer.commit()
